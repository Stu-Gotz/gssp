<script setup>
import { useUserStore } from '../stores/userStore';

const userStore = useUserStore();

const savedTeams = userStore.getUserTeams;

console.log(savedTeams)

// const savedTeams = [
//   {
//     id: 1,
//     teamName: "savedTeam1",
//     preview: "this should be a list of tiny sprites of each pokemon",
//     summary: "A sun-based offensive weather team."
//   },
//   {
//     id: 2,
//     teamName: "savedTeam2",
//     preview: "this should be a list of tiny sprites of each pokemon",
//     summary: "A Gen4 stall team based on SkarmBliss + Nidoqueen core."
//   }
// ]

</script>

<template>

  <div class="col">
    <div class="profile-header card row row-cols-2" style="width: 20rem;">
      <div class="pfp col">
        <!-- profile image, probably default to 300x300 -->
        <img src="/assets/default.jpg" alt="" srcset="" width="300" height="300">
      </div>
      <div class="pfd col">
        <!-- Profile data (username, join date, etc here) -->
        <!-- something like -->
        <div style="width: 20rem;">
          <div class="card-body">
            <h5 class="card-title">{{ userStore.getUsername }}</h5>
            <!-- <h6 class="card-subtitle">Location {{ userStore.getLocation }}</h6> need to make this first -->
            <h6 class="card-subtitle">Join Date: Today</h6>
            <!-- this will obviously have to change and annoyingly i will have to redo the users table because i forgot to include join dates-->

          </div>
        </div>
      </div>
    </div>
    <div class="bio row">
      <!-- Any voluntary bio information such as age, gender, location etc -->
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsum reiciendis, id asperiores sequi, modi laboriosam
      autem neque laudantium laborum ex voluptatibus nostrum repudiandae amet. Cum voluptatem omnis magni ratione
      nostrum, quis, assumenda aliquid fugiat unde, odit ipsum facere aspernatur molestias quo cumque qui quidem quae
      beatae blanditiis suscipit! Iure, non provident eaque, at mollitia minima pariatur officiis numquam impedit
      nostrum esse ullam culpa eligendi illo quibusdam recusandae quos ut consequuntur. Repellat nemo, optio facere,
      asperiores est, ab beatae fugiat tenetur dolorum vel voluptatem sed praesentium iure quos. Pariatur et officia
      enim? Explicabo, consectetur officiis culpa quam fugiat ab! Laudantium, minus!
    </div>
    <div class="saved-teams col">
      <!-- display saved teams (up to 5 per account just to start) -->
      <table class="table">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Team Name</th>
            <th scope="col">Preview</th>
            <th scope="col">Summary</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, i) in savedTeams" :key="i">
            <td>{{ i+1 }}</td>
            <td>{{ data.name }}</td>
            <td>{{ data.members.map(a => a.name).join(", ") }}</td>
            <td>Something should go here.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style lang="scss"></style>