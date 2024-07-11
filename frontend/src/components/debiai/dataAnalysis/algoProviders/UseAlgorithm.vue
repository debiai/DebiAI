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
        <span>{{ algoProvider.name }}</span>
        <span style="padding: 0 5px 0 10px"> / </span>
        <inline-svg
          :src="require('@/assets/svg/algorithm.svg')"
          width="20"
          height="20"
          style="margin: 0 5px 1px 5px"
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

    <p id="description">{{ algorithm.description }}</p>
    <!-- Algorithm inputs-->
    <div id="content">
      <div id="inputs">
        <UseAlgorithmInput
          v-for="(input, index) in algorithm.inputs"
          :key="index"
          :input="input"
          :data="data"
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
      const nb_val_displayed = 10;
      this.algorithm.inputs.forEach((input) => {
        body += input.name + ": ";
        if (input.value === null || input.value === undefined) body += "null,\n";
        else {
          if (input.type === "array") body += "[";
          body += input.value.toString().slice(0, nb_val_displayed);
          if (input.value.toString().length > nb_val_displayed) body += "...";
          if (input.type === "array") body += "] (" + input.value.length + " values)";
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

<style scoped lang="scss">
#UseAlgo {
  width: 75vw;
  height: 75vh;
  display: flex;
  flex-direction: column;

  #info {
    font-size: 1.3em;

    #title {
      display: flex;
      align-items: center;
    }

    #algoName {
      font-weight: bold;
    }
  }

  #description {
    margin: 10px 0;
    text-align: left;
    color: var(--fontColorLight);
    white-space: pre-wrap;
  }

  /* Content */
  #content {
    flex: 1;
    display: flex;
    flex-direction: column;

    h5 {
      align-self: flex-start;
    }
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
    margin-top: 20px;
    margin-bottom: 20px;

    #requestBody {
      flex: 1;
      height: 70px;
      overflow: auto;
    }

    fieldset {
      color: var(--fontColorLight);
      border: 1px solid var(--greyDark);
      border-radius: 2px;
      padding-left: 20px;
      white-space: pre-line;
      text-align: start;
    }

    legend {
      color: var(--fontColor);
    }

    button {
      margin: 10px 0 5px 0;
    }
  }
}
</style>
