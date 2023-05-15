<template>
  <div
    class="algorithm item"
    @click="$emit('selected')"
  >
    <div
      class="tags"
      v-if="algorithm.tags"
    >
      <div
        class="tag"
        v-for="(tag, i) in algorithm.tags"
        :key="i"
      >
        {{ tag }}
      </div>
    </div>

    <div class="top">
      <inline-svg
        :src="require('@/assets/svg/algorithm.svg')"
        width="15"
        height="15"
      />
      <h4
        class="title"
        :title="'Id: ' + algorithm.id"
      >
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
      <p
        class="version"
        v-if="algorithm.author"
      >
        Created by {{ algorithm.author }}
      </p>
      <p
        class="version"
        v-else
      >
        No author
      </p>

      <button
        class="green"
        @click="$emit('useAlgo')"
      >
        Use algorithm
      </button>
    </div>

    <div class="content">
      <div class="section">
        <h5 class="section-title">{{ "Input" + (algorithm.inputs.length > 1 ? "s" : "") }}:</h5>
        <div class="parameter-list inputs">
          <div
            v-for="(input, index) in algorithm.inputs"
            :key="index"
            class="parameter input"
          >
            <div class="name">
              {{ input.name }}
              <span
                class="parameterType"
                v-if="input.type == 'array'"
                >Array of {{ input.arrayType }}s</span
              >
              <span
                class="parameterType"
                v-else
                >{{ input.type }}</span
              >
              <DocumentationBlock
                :followCursor="true"
                v-if="inputDetail(input)"
              >
                <div v-html="inputDetail(input)"></div>
              </DocumentationBlock>
            </div>
            <p class="description">{{ input.description }}</p>
          </div>
        </div>
        <div v-if="algorithm.inputs.length === 0">
          <p>No input</p>
        </div>
      </div>
      <div class="section">
        <h5 class="section-title">{{ "Output" + (algorithm.outputs.length > 1 ? "s" : "") }}:</h5>
        <div class="parameter-list">
          <div
            v-for="(output, index) in algorithm.outputs"
            :key="index"
            class="parameter output"
          >
            <p>
              {{ output.name }}
              <span
                class="parameterType"
                v-if="output.type == 'array'"
                >Array of {{ output.arrayType }}s</span
              >
              <span
                class="parameterType"
                v-else
                >{{ output.type }}</span
              >
            </p>
            <p class="description">{{ output.description }}</p>
          </div>
        </div>
        <div v-if="algorithm.outputs.length === 0">
          <p>No output</p>
        </div>
      </div>
    </div>
    <div
      class="bottom"
      v-if="algorithm.experiments.length > 0"
    >
      <!-- Displays the different results + the use btn -->
      <div class="experiments">
        <div
          v-for="(experiment, index) in algorithm.experiments"
          :key="index"
          class="experiment"
        >
          <h5 class="experiment-title">Experiment {{ index + 1 }}</h5>
          <div class="results">
            <div
              class="result"
              v-for="result in experiment"
              :key="result.name"
            >
              <div class="name">{{ result.name }}</div>
              <div class="value">{{ result.value.toString() }}</div>
            </div>
          </div>
        </div>
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
  methods: {
    inputDetail(input) {
      const optionalFields = [
        { field: "default", name: "Default value" },
        { field: "min", name: "Min number" },
        { field: "max", name: "Max number" },
        { field: "availableValues", name: "Suggested values" },
        { field: "lengthMin", name: "Minimum length" },
        { field: "lengthMax", name: "Maximum length" },
      ];
      let details = "";

      const maxValueLength = 30;
      optionalFields.forEach((field) => {
        if (input[field.field] !== null && input[field.field] !== undefined) {
          let fieldVal = input[field.field].toString().slice(0, maxValueLength);
          if (input[field.field].toString().length > maxValueLength) fieldVal += "...";

          details += field.name + ": <b>" + fieldVal + "</b><br/>";
        }
      });

      return details;
    },
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

/* Top */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}
.tags .tag {
  border: solid 1px var(--white);
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 0.9em;
  color: var(--white);
}
.top {
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding-bottom: 30px;
  flex-wrap: wrap;
}
.top .title {
  margin-top: 1px;
  font-size: 1.1em;
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
  flex: 5;
  color: #909090;
  min-width: 200px;
  margin: 0;
}

/* Content */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.content .section {
  display: flex;
  align-items: center;
  gap: 10px;
}
.content .section-title {
  width: 50px;
}
.content .section .description {
  color: #909090;
  font-size: 0.8em;
}

.parameter-list {
  display: flex;
  gap: 10px;
  overflow: auto;
  padding-bottom: 10px;
}
.parameter {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 6px;
  min-width: 150px;
}
.parameter .name {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 5px;
  padding: 5px;
}
.parameter .name #DocumentationBlock {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}
.parameter p {
  margin: 4px;
}
.parameterType {
  color: #909090;
  border: 1px solid #ccc;
  padding: 0 2px 0 2px;
  border-radius: 4px;
  font-size: 0.8em;
}

/* Bottom */
.bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding-top: 20px;
}
.bottom .experiments {
  display: flex;
  align-items: center;
  overflow: auto;
  flex: 1;
  border-radius: 4px;
  gap: 10px;
  padding-bottom: 15px;
}

.bottom .experiments .experiment {
  display: flex;
  padding: 10px;
  flex-direction: column;

  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 3px;
}
.bottom .experiments .experiment .experiment-title {
  margin: 0;
  padding: 0;
  margin-bottom: 5px;
  font-size: 0.8em;
  color: #909090;
}

.results {
  display: flex;
  gap: 10px;
}

.results .result {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 3px 7px 3px 7px;
  gap: 15px;
}
.results .result .name {
  white-space: nowrap;
}

.results .result .value {
  background-color: #fbfbfb;
  border: 1px solid #ccc;
  padding: 2px 7px 2px 7px;
  border-radius: 4px;
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
