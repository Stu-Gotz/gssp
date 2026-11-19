import { defineStore } from "pinia";
import { Koffing } from "koffing";
import Pokedex from "pokedex-promise-v2";
import { apiGet, normaliseNames } from "../utils/utils";

const P = new Pokedex();

function lowerCaseKeys(obj) {
  Object.keys(obj).forEach((k) => {
    if (typeof obj[k] == "string") {
      obj[k] = obj[k].toLowerCase();
    } else if (typeof obj[k] == "object") {
      obj[k] = lowerCaseKeys(obj[k]);
    }
  });
  return obj;
}

async function mapMoves(movesArray) {
  // 
  const moveObject = await P.getMoveByName(
    movesArray.map((i) => normaliseNames(i, "-", " "))
  ).then((response) => {
    let moves = [];
    for (var i in response) {
      var move = new Object();
      move = {
        name: response[i].name,
        type: response[i].type.name,
        priority: response[i].priority,
        power: response[i].power,
        genre: response[i].damage_class.name,
      };
      moves.push(move);
    }
    return moves;
  });
  return moveObject;
}

export const useTeamStore = defineStore("teamStore", {
  state: () => ({
    team: {
      name: null,
      gen: null,
      tier: null,
      members: null,
    },

  }),
  getters: {
    getTeam: (state) => {
      return state.team || null;
    },
    getGen: (state) => {
      return state.team.gen || null;
    },
    getTier: (state) => {
      return state.team.tier || null;
    },
  },
  actions: {
    async parseInput(teamInput) { //big string paste. 
      const that = this; //to pass the `this` variable around

      const parsedTeam = Koffing.parse(teamInput);
      const members = parsedTeam.teams[0].pokemon;
      if (!members?.length) throw new Error("Couldn't find a team in that text.");

      const pokemon = members.map(function (el) {
        const formatted = lowerCaseKeys(el);
        formatted["name"] = normaliseNames(formatted["name"], "-", " ")

        return formatted;
      });

      const tasks = pokemon.map((mon) => mon.name);
      const res = (await Promise.all(tasks.map((n) => apiGet(`/dex/${encodeURIComponent(n)}`)))).map((r) => r.data);

      pokemon.forEach(async (el) => {
        el["moves"] = await mapMoves(el["moves"], that);
      });

      //extracting fields of interest from the things I want from the res variable
      for (var i = 0; i < pokemon.length; i++) {
        res.filter(
          (obj) => obj["name"] === pokemon[i].name
        )[0];
        pokemon[i]["type"] = res[i]["types"]
        pokemon[i]["dex"] = res[i]["num"];
        pokemon[i]["spriteUrl"] = await P.getPokemonByName(pokemon[i].name).then((res) => {
          return res["sprites"]["front_default"]
        })
        pokemon[i]["itemUrl"] = await P.getItemByName(
          normaliseNames(pokemon[i].item, "-", " ")
        )
          .then((response) => {
            return response["sprites"]["default"];
          })
          .catch(() => {
            return null;
          });
      }
      return pokemon;
    },
    updateTeam(teamObj) {
      this.team.members = teamObj.members;
      this.team.gen = teamObj.gen;
      this.team.tier = teamObj.tier;
      this.team.name = teamObj.name;
      /* 
        a good enough random generator, since i am capping at 5 teams, 
        and i dont honestly forsee this getting over 10thousand users, 
        it should suffice 
      */
      this.team.id = Math.random().toString(36).substring(2);
    },
  },
  persist: true,
});
