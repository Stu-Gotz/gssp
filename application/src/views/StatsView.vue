<script setup>
/* need to load current stats as soon as page loads
   routing calls on form submit, reload stats to object.
   cache results ?10min?
   selectable rows, filtered columns (might be builtin to boostrap?)
   highlight team members 

*/
import { useTeamStore } from '../stores/teamStore';
import { useStatStore } from '../stores/usageStore';
import { storeToRefs } from 'pinia';

const rootGen = "gen9ou";
const statStore = useStatStore();

const { current, previous, tma } = storeToRefs(statStore);


</script>

<template>
  <!-- 
  navbar etc up here (already taken care of)
  +==========================================+
  | gen tier | date picker | submit | clear #toggle for monotype
  +==========================================+
  | table with headers, search function if easy to implement
  |
  |
  |
  ...
  footer down below (i think also taken care of)
   -->
  <form action="POST" class="statSelectForm">
    <div class="input-group mb-3 col-md-12" id="selectorWrapper">
      <input class="form-control col-md-2" type="text" name="tier-input" id="selectorWrapper-tier-input">
      <input class="form-control col-md-2" type="date" name="date-picker" id="selectorWrapper-date-input">
      <div class="col-md-4">
        <!-- This button should trigger a fetch from the DB or cache, reminds me,
        set up some sort of caching system. -->
        <button class="btn btn-success" type="submit">Submit</button>
        <!-- This button should reset the entire page -->
        <button class="btn btn-danger" type="submit">Clear</button>
      </div>
      <div class="col-md-4 space-between">
        <input class="form-check-input" type="checkbox" name="mono-toggle" id="selectorWrapper-mono-toggle">
        <label for="selectorWrapper-mono-toggle" class="form-check-label">Monotype?</label>
      </div>
    </div>
  </form>

  <table class="table table-striped-columns table-hover table-bordered">
    <caption>List of usage stats from [TIER] on [DATE] as of [CURRENT DATE]</caption>
    <thead>
      <tr>
        <th class="table-info" scope="col">col1</th>
        <th scope="col">col2</th>
        <th scope="col">col3</th>
        <th scope="col">col4</th>
        <th scope="col">col5</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr>
        <th scope="row">1</th>
        <td>Mark</td>
        <td>Otto</td>
        <td>@mdo</td>
        <td>filler</td>
      </tr>
      <tr class="table-danger">
        <th scope="row">1</th>
        <td>Mark</td>
        <td>Otto</td>
        <td>@mdo</td>
        <td>filler</td>
      </tr>
      <tr>
        <td colspan="4">
          <table class="table mb-0">
          <!-- THIS TABLE SHOULd COLLAPSE AND EXPAND ON PARENT CLICKop -->
            <caption>[TREND SUMMARY (CURRENT / PREVIOUS / OLDEST)]</caption>
            <thead>
              <tr>
                <th>Curr Month</th>
                <th colspan="2">Month Before</th>
                <th>Month Before That</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Rank: 2(+3)</td>
                <!-- BOTH TR AND TH NEED CORRESPONDING COLSPAN PROPERTIES -->
                <td colspan="2">Rank: 5 (-2)</td>
                <td>Rank: 3 (-)</td>
              </tr>
              
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <th class="table-primary" scope="row">1</th>
        <td>Mark</td>
        <td>Otto</td>
        <td>@mdo</td>
        <td>filler</td>
      </tr>
    </tbody>
  </table>
   
</template>