<template>
  <div
    class="algorithm item selectable"
    @click="$emit('selected')"
  >
    <div class="top">
      <h4 class="title">
        {{
          algorithm.name !== null && algorithm.name !== undefined ? algorithm.name : algorithm.id
        }}
      </h4>
      <p
        class="version"
        v-if="algorithm.version !== null && algorithm.version !== undefined"
      >
        {{ algorithm.version }}
      </p>
      <p class="description">
        {{ algorithm.description }}
      </p>
      <p class="version">Created by {{ algorithm.author }}</p>
    </div>
    <div class="content">
      <div class="details"></div>
      <div class="section">
        <h4 class="section-title">Inputs</h4>
        <ul class="parameter-list">
          <li
            v-for="(input, index) in algorithm.inputs"
            :key="index"
          >
            <p><strong>Name:</strong> {{ input.name }}</p>
            <p><strong>Type:</strong> {{ input.type }}</p>
            <p class="description"><strong>Description:</strong> {{ input.description }}</p>
          </li>
        </ul>
      </div>
      <div class="section">
        <h4 class="section-title">Outputs</h4>
        <ul class="parameter-list">
          <li
            v-for="(output, index) in algorithm.outputs"
            :key="index"
          >
            <p><strong>Name:</strong> {{ output.name }}</p>
            <p><strong>Type:</strong> {{ output.type }}</p>
            <p class="description"><strong>Description:</strong> {{ output.description }}</p>
          </li>
        </ul>
      </div>
      <div class="section">
        <h4 class="section-title">Parameters</h4>
        <ul class="parameter-list">
          <li
            v-for="(parameter, index) in algorithm.parameters"
            :key="index"
          >
            <p><strong>Name:</strong> {{ parameter.name }}</p>
            <p><strong>Type:</strong> {{ parameter.type }}</p>
            <p class="description"><strong>Description:</strong> {{ parameter.description }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Algorithm",
  props: {
    algorithm: { type: Object, required: true },
  },
};
</script>

<style scoped>
.algorithm {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.content {
  display: flex;
  align-items: flex-start;
}

.top {
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding-bottom: 30px;
}
.top .version {
  font-size: 0.8em;
  color: #999;
  border: 1px solid #999;
  border-radius: 4px;
  padding: 2px 4px;
  margin: 0;
}
.top .description {
  max-width: 500px;
  flex: 3;
  margin: 0;
}
.description {
  color: #909090;
}

.details {
  margin-bottom: 10px;
  padding: 20px;
}

.parameter-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.parameter-list li {
  margin-bottom: 10px;
}
</style>
