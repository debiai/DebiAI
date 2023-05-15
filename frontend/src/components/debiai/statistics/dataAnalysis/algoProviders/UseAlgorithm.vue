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
          v-on:inputValueUpdate="(val) => (input.value = val)"
        />
      </div>
      <div v-if="algorithm.inputs.length === 0">
        <p>No inputs</p>
      </div>
    </div>

    <button
      class="green"
      @click="$emit('use')"
    >
      Run the algorithm
    </button>
  </div>
</template>

<script>
import UseAlgorithmInput from "./UseAlgorithmInput.vue";

export default {
  components: { UseAlgorithmInput },
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
  methods: {},
  computed: {},
};
</script>

<style scoped>
#UseAlgo {
  width: 1000px;
  height: 800px;
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
button {
  align-self: flex-end;
}
</style>
