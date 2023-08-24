<template>
  <div
    class="algorithm item"
    @click="$emit('selected')"
  >
    <!-- Top: Tags, controls -->
    <div
      class="top"
      v-if="algorithm.tags"
    >
      <div class="tags">
        <div
          class="tag"
          v-for="(tag, i) in algorithm.tags"
          :key="i"
        >
          {{ tag }}
        </div>
      </div>

      <div class="controls">
        <button
          class="blue"
          @click="$emit('viewExperiments')"
          v-if="nbExperiments > 0"
        >
          <span class="badge">{{ nbExperiments }}</span>
          Experiments
        </button>
        <button
          @click="$emit('useAlgo')"
        >
          Use algorithm
        </button>
      </div>
    </div>

    <!-- Name, version, description, author -->
    <div class="header">
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
        class="version tag"
        v-if="algorithm.version !== null && algorithm.version !== undefined"
      >
        {{ algorithm.version }}
      </p>
      <p class="description">
        {{ algorithm.description }}
      </p>
      <div
        class="author"
        v-if="algorithm.author"
      >
        Created by {{ algorithm.author }}
      </div>
      <div
        class="author"
        v-else
      >
        No author
      </div>
    </div>

    <!-- Displays the different parameters and results -->
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
                class="parameterType tag"
                v-if="input.type == 'array'"
                >Array of {{ input.arrayType }}s</span
              >
              <span
                class="parameterType tag"
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
                class="parameterType tag"
                v-if="output.type == 'array'"
                >Array of {{ output.arrayType }}s</span
              >
              <span
                class="parameterType tag"
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
  </div>
</template>

<script>
export default {
  name: "Algorithm",
  props: {
    algoProvider: { type: Object, required: true },
    algorithm: { type: Object, required: true },
  },
  data() {
    return {};
  },
  mounted() {},
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
  computed: {
    nbExperiments() {
      // Use the store getter to get the experiments
      return this.$store.getters.getAlgoNbExperiments(this.algoProvider.name, this.algorithm.id);
    },
  },
};
</script>

<style scoped>
.algorithm {
  border: 1px solid var(--greyDark);
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

/* Top */
.top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.top .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}

/* Header */
.header {
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding-bottom: 30px;
  flex-wrap: wrap;
}
.header .title {
  margin-top: 1px;
}
.header .version {
  margin: 0;
}
.header .description {
  flex: 5;
  color: var(--fontColorLight);
  min-width: 200px;
  margin: 0;
}
.header .author {
  color: var(--fontColorLight);
  padding: 5px;
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
  color: var(--fontColorLight);
}

.parameter-list {
  display: flex;
  gap: 10px;
  overflow: auto;
  padding-bottom: 10px;
}
.parameter {
  border: 1px solid var(--greyDark);
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
</style>
