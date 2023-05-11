<template>
  <div
    class="algorithm item"
    @click="$emit('selected')"
  >
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
      <p class="version">Created by {{ algorithm.author }}</p>
      <button class="green">Use algorithm</button>
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

      optionalFields.forEach((field) => {
        if (input[field.field] !== null && input[field.field] !== undefined) {
          details += field.name + ": " + input[field.field] + "<br/>";
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

.top {
  margin: 0;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding-bottom: 30px;
}
.top .title {
  margin-top: 1px;
}
.top .version {
  font-size: 0.8em;
  color: #999;
  border: 1px solid #999;
  border-radius: 4px;
  padding: 2px 4px;
  margin: 0;
}
.top button {
  margin-top: -4px;
}
.top .description {
  max-width: 500px;
  flex: 3;
  color: #909090;
  margin: 0;
}

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
.content .section .description {
  color: #909090;
  font-size: 0.8em;
}

.parameter-list {
  display: flex;
  gap: 10px;
  overflow: auto;
  scrollbar-width: thin;
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
</style>
