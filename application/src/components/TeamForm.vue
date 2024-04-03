<script setup>
import { ref, onMounted } from 'vue';
import { useTeamStore } from '../stores/teamStore';
import { useStatStore } from '../stores/usageStore';
import { useUserStore } from '../stores/userStore';
import { gens, tiers } from '../utils/utils.js';

// stores
const teamStore = useTeamStore();
const statStore = useStatStore();
const userStore = useUserStore();





// Reactive variables from the form, which will be used to query the database to populate
// the other half of the page
const userInput = ref(null);
const tier = ref("");
const gen = ref("");
const name = ref("")
const teamName = ref("");

let teamObj = teamStore.team || {
  name: null,
  gen: null,
  tier: null,
  members: null,
}



onMounted(() => {
  userInput.value = "";
  tier.value = teamStore.team ? teamStore.getTier : "";
  gen.value = teamStore.team ? teamStore.getGen : "";
  name.value = teamStore.team.name;
});

const errors = ref([]);

async function submitForm() {
  const defaultName = `=== ${gen.value}${tier.value} ${teamName.value}===`;
  errors.value = [];
  // console.log(errors.value);

  /** This just checks that users have input values into required fields */
  if (userInput.value === null) {
    errors.value.push("Please paste a team into the area below.");
    // console.log(errors.value);
  } else if (gen.value === "") {
    errors.value.push("Please select a generation from the dropdown below.");
    // console.log(errors.value);
  } else if (tier.value === "") {
    errors.value.push("Please select a tier from the dropdown below.");
    // console.log(errors.value);
  } else {
    teamObj = {
        name: name.value || defaultName,
        gen: gen.value,
        tier: tier.value,
        members: null,
      }
    teamObj.members = await teamStore.parseInput(userInput.value);
    
    const tranche = gen.value + tier.value;
    
    await statStore.setCurrent(tranche);
    await statStore.setPrevious(tranche);
    await statStore.setOlder(tranche);

    teamStore.updateTeam(teamObj);

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
  window.location.reload()
}

async function saveTeam() {
  console.log(teamObj)
  await userStore.saveTeam(teamObj);
}
</script>

<template>
  <!-- left half  -->
  <form @submit.prevent class="d-flex flex-column flex-1">
    <ul v-if="errors.value">
      <li v-for="{ idx, err } in errors.value">{{ idx }} - {{ err }}</li>
    </ul>
    <label class="team-name" for="teamName">Provide a team name (optional):</label>
    <input v-model="name" class="form-control ps-2 pt-0 mx-2 mb-2 mt-0" type="text" id="teamName" placeholder="Team Name">
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
      <button v-if="userStore.getLoginStatus" @click="saveTeam()" type="button" class="btn btn-primary form-control w-25">Save</button>
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