<template>
  <div id="UseAlgo">
    <!-- Info -->
    <div
      id="info"
      class="aligned spaced"
    >
      <div
        id="title"
        :title="'Id: ' + algorithm.id"
      >
        <span> Using the algorithm: </span>
        <inline-svg
          :src="require('@/assets/svg/algorithm.svg')"
          width="20"
          height="20"
          style="margin: 0 5px 0 15px"
        />
        <span id="algoName">
          {{
            algorithm.name !== null && algorithm.name !== undefined ? algorithm.name : algorithm.id
          }}
        </span>
      </div>

      <button
        class="red"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
    </div>

    <!-- Algorithm inputs-->
    <div class="content">
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
  </div>
</template>

<script>
export default {
  name: "UseAlgo",
  props: {
    algorithm: {
      type: Object,
      required: true,
    },
    algoProvider: {
      type: Object,
      required: true,
    },
  },
  data: () => {
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

      optionalFields.forEach((field) => {
        if (input[field.field] !== null && input[field.field] !== undefined) {
          details += field.name + ": " + input[field.field] + "<br/>";
        }
      });

      return details;
    },
  },
  computed: {},
};
</script>

<style scoped>
#UseAlgo {
  width: 1000px;
  height: 800px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

#info {
  font-size: 1.3em;
}
#info #title {
  display: flex;
  align-items: center;
}
#info #algoName {
  font-weight: bold;
  color: #636363;
  border-bottom: 1px solid #636363;
}

/* Content */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
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
</style>
