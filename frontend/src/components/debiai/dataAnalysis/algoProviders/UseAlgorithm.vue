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
        <span style="padding: 0 10px"> from </span>
        <span>{{ algoProvider.name }}</span>
      </div>

      <button
        class="red"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
    </div>

    <div id="description">
      {{ algorithm.description }}
    </div>
    <!-- Algorithm inputs-->
    <div id="content">
      <h5>{{ "Input" + (algorithm.inputs.length > 1 ? "s" : "") }}:</h5>
      <div id="inputs">
        <UseAlgorithmInput
          v-for="(input, index) in algorithm.inputs"
          :key="index"
          :input="input"
          :data="data"
          :selectedData="selectedData"
          v-on:inputValueUpdate="
            (val) => {
              input.value = val;
              updateBody();
            }
          "
        />
      </div>
      <div v-if="algorithm.inputs.length === 0">
        <p>No inputs</p>
      </div>
    </div>
    <div id="bottom">
      <fieldset id="requestBody">
        <legend>Provided inputs</legend>
        {{ requestBody }}
      </fieldset>

      <button
        class="green"
        @click="$emit('use')"
      >
        Run the algorithm
      </button>
    </div>
  </div>
</template>

<script>
import UseAlgorithmInput from "./UseAlgorithmInput.vue";

export default {
  components: { UseAlgorithmInput },
  name: "UseAlgo",
  props: {
    algorithm: { type: Object, required: true },
    algoProvider: { type: Object, required: true },
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  data: () => {
    return {
      requestBody: "",
    };
  },
  mounted() {},
  methods: {
    updateBody() {
      let body = "";
      this.algorithm.inputs.forEach((input) => {
        body += input.name + ": ";
        if (input.value === null || input.value === undefined) body += "null,\n";
        else {
          if (input.type === "array") body += "[";
          body += input.value.toString().slice(0, 100);
          if (input.value.toString().length > 100) body += "...";
          if (input.type === "array") body += "]";
          body += ",\n";
        }
      });
      body = body.slice(0, body.length - 2);
      this.requestBody = body;
    },
  },
  computed: {},
};
</script>

<style scoped>
#UseAlgo {
  width: 75vw;
  height: 75vh;
  display: flex;
  flex-direction: column;
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
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 2px 5px;
}
#description {
  margin: 10px 0 10px 0;
  text-align: left;
  color: #898989;
}

/* Content */
#content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

#content h5 {
  align-self: flex-start;
}

#inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#bottom {
  display: flex;
  gap: 10px;
  align-items: stretch;
}
#bottom #requestBody {
  flex: 1;
  height: 50px;
  overflow: auto;
}
#bottom fieldset {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding-left: 20px;
  white-space: pre-line;
  text-align: start;
}
#bottom legend {
  color: #636363;
}
#bottom button {
  margin: 10px 0 5px 0;
}
</style>
