<template>
  <div class="configuration">
    <div class="left">
      <div class="name">
        <h4>{{ conf.name }}</h4>
        <span
          class="creationDate"
          :title="$services.timeStampToDate(conf.creationDate)"
        >
          Created {{ $services.prettyTimeStamp(conf.creationDate) }}
        </span>
      </div>
      <div class="description">{{ conf.description }}</div>
    </div>
    <table class="confDetails">
      <tr v-for="key in Object.keys(conf.conf)" :key="key">
        <th class="key">{{ key }}</th>
        <th class="value">{{ conf.conf[key] }}</th>
      </tr>
    </table>
    <div class="controls">
      <button class="red" @click="$emit('delete')">Delete</button>
      <button class="green" @click="$emit('selected')">Select</button>
    </div>
  </div>
</template>

<script>
export default {
  props: { conf: { type: Object, required: true } },
};
</script>

<style scoped>
/* Configurations */
.configuration {
  padding: 5px 0 2px 20px;
  background-color: rgb(245, 245, 245);
  transition: background-color ease-out 0.1s;
  display: flex;
}
.configuration + .configuration {
  margin-top: 5px;
}
.configuration .left {
  flex: 1;
}
.configuration .name {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.configuration .creationDate {
  text-align: left;
  font-size: 0.7em;
  opacity: 0.7;
}
.configuration .description {
  text-align: left;
  padding-top: 10px;
  white-space: pre-wrap;
  opacity: 0.6;
  font-size: 0.8em;
}
.configuration .confDetails {
  font-size: 0.5em;
  padding-right: 10px;
  border-spacing: 0px;
  opacity: 0.6;
  align-self: flex-start;
}
.configuration .key {
  text-align: right;
}
.configuration .value {
  text-align: left;
}
.configuration .controls {
  display: flex;
  align-items: center;
}
.configuration .controls button {
  font-size: 0.6em;
  margin: 5px;
  padding-top: 6px;
  padding-bottom: 6px
}
</style>
