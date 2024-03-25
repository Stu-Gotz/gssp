<script setup>
import { ref, onMounted } from 'vue';
import { Koffing } from 'koffing';
import { useTeamStore } from '../stores/teamStore';
import { useStatStore } from '../stores/usageStore';
import { storeToRefs } from 'pinia';
import Pokedex from 'pokedex-promise-v2';

const P = new Pokedex();

const tiers = [
  "ou",
  "ubers",
  "pu",
  "nu",
  "lc",
  "uu",
  "ru",
  "2v2doubles",
  "doubles",
  "anythinggoes",
  "almostanyability",
  "balancedhackmons",
  "battlefactory",
  "battlespotsingles",
  "battlespotdoubles",
  "battlespotspecial",
  "bssfactory",
  "budoubles",
  "busingles",
  "camomons",
  "challengecup",
  "challengecup1v1",
  "doublescustomgame",
  "doublesou",
  "doublesubers",
  "doublesuu",
  "hackmonscup",
  "inversebattle",
  "lcuu",
  "linked",
  "monotype",
  "natureswap",
  "nfe",
  "ounomega",
  "randombattle",
  "randomdoublesbattle",
  "randomtriplesbattle",
  "stabmons",
  "smogontriples",
  "tiershift",
  "ultrakalosclassic",
  "vcg2018",
  "vgc2014",
  "vgc2015",
  "vgc2016",
  "vgc2017",
  "vgc2019",
  "vgc2020",
  "zu",
  "doubleslc"
];

const gens = ["gen1", "gen2", "gen3", "gen4", "gen5", "gen6", "gen7", "gen8", "gen9"];


// Reactive variables from the form, which will be used to query the database to populate
// the other half of the page
const userInput = ref(null);
const tier = ref("");
const gen = ref("");
const teamName = ref("");
const fullname = `=== ${gen.value}${tier.value} ${teamName.value}===`;

// stores
const teamStore = useTeamStore();
const statStore = useStatStore();

onMounted(() => {
  userInput.value = "";
  tier.value = "";
  gen.value = "";
});

const errors = ref([]);


async function submitForm() {
  console.log(errors.value);
  errors.value = [];
  console.log(errors.value);
  if (userInput.value === null) {
    errors.value.push("Please paste a team into the area below.");
    console.log(errors.value);
  } else if (gen.value === "") {
    errors.value.push("Please select a generation from the dropdown below.");
    console.log(errors.value);
  } else if (tier.value === "") {
    errors.value.push("Please select a tier from the dropdown below.");
    console.log(errors.value);
  } else {

    const team = await teamStore.parseInput(userInput.value);

    const tranche = gen.value + tier.value;
    // await statStore.setCurrent(tranche);
    // await statStore.setPrevious(tranche);
    // await statStore.setOlder(tranche);
    teamStore.updateTeam(team);

    /**
     * 
     * This is old code, but is kept here because I needed to make it better and abstract it away
     * i realise having a huge chunk of old code is very untidy, but such is life
     
    // console.log(team)
    // const teamIn = Koffing.parse(userInput.value);
    // const team = teamIn.teams[0].pokemon;

    // // console.log(team)

    // create tasks variable from team object to easily pass to a promsie.all()
    // this *should* significantly increase the speed of processing for the 
    // team submission part of the application which currently takes
    // bloody ages to finish (like 8 to 10s)
    // const tasks = team.map(pokemon => pokemon.name.toLowerCase())

    // const pokemon = await P.getPokemonByName(tasks)

    // console.log(pokemon)


    // for (var i in team) {
    // const pokemon = await P.getPokemonByName(team[i].name.toLowerCase()); //fetch(`https://pokeapi.co/api/v2/pokemon/${team[i].name.toLowerCase()}`);
    // team[i].dex = pokemon.id;
    // team[i].spriteUrl = pokemon.sprites.front_default;
    // team[i].type = [];
    // team[i].itemUrl = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/${team[i].item.toLowerCase().replace(' ', '-')}.png`;

    // for (var j in team[i].moves) {
    //   const moves = await P.getMoveByName(team[i].moves[j].toLowerCase().replace(' ', '-'));//fetch(`https://pokeapi.co/api/v2/move/${team[i].moves[j].toLowerCase().replace(' ', '-')}/`)

    //   team[i].moves[j] = {
    //     name: team[i].moves[j],
    //     type: moves.type.name,
    //     priority: moves.priority
    //   }
    // }

    // for (var t in pokemon.types) {

    //   team[i].type.push(pokemon.types[t].type.name);
    // }

    // };

   
     * END OLD CODE
     */

  }
}

function clearForm() {
  userInput.value = "";
  teamStore.$reset();
}
</script>

<template>
  <!-- left half  -->
  <form @submit.prevent class="d-flex flex-column flex-1">
    <ul v-if="errors.value">
      <li v-for="{ idx, err } in errors.value">{{ idx }} - {{ err }}</li>
    </ul>
    <label class="team-name" for="genInput">Please select the generation:</label>
    <input class="form-control ps-2 pt-0 mx-2 mb-2 mt-0" type="text" id="team-name" placeholder="Team Name (optional)">
    <label class="form-label" for="genInput">Please select the generation:</label>
    <select v-model="gen" class="form-select ps-2 pt-0 mx-2 mb-2 mt-0" name="genInput" id="genInput">
      <option v-for="gen in gens">{{ gen }}</option>
    </select>
    <label class="form-label" for="tierInput">Please select the tier your team is in:</label>
    <select v-model="tier" class="form-select ps-2 pt-0 mx-2 mb-2 mt-0" name="tierInput" id="tierInput">
      <option v-for="tier in tiers">{{ tier }}</option>
    </select>
    <label class="form-label" for="teamPasteArea">Please paste your Showdown output below: </label>
    <textarea class="form-control pastearea d-flex flex-column h-100 flex-grow-1" placeholder="" name="teamPasteArea"
      id="teamPasteArea" v-model="userInput">
    </textarea>
    <div class="d-flex align-items-center justify-content-around">
      <button @click="submitForm()" type="button" class="btn btn-success form-control w-25">Submit</button>
      <button @click="clearForm()" type="button" class="btn btn-danger form-control w-25">Clear</button>
    </div>
  </form>
</template>

<style lang="scss">
form {
  font-size: .8rem;
}

.pastearea {
  outline: 0 none;
  padding: 10px;
  resize: none;

  box-sizing: border-box;
  // background-color:#a79bbc;
  border: none;
  border-radius: 10px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, .3);

  // height: calc(100% - 300px);
  &::-webkit-scrollbar {
    // width: 12px;
    background: #5c4780;
    border-radius: 20px;

    &-button {
      background: #432e68;
      border-radius: 20px;
    }

    &-thumb {
      background: #7d6b9b;
      border: 1px solid #192650;
      cursor: pointer;
      border-radius: 20px;
    }
  }
}

.form-select:focus,
.form-control:focus {
  outline: none !important;
  border: 2px solid darkorchid;
  box-shadow: 0 0 10px mediumorchid;
}
</style>