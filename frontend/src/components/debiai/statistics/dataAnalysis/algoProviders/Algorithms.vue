<template>
  <div id="AlgorithmsSelection">
    <!-- New algo provider -->
    <modal
      v-if="newAlgoProviderModal"
      @close="newAlgoProviderModal = false"
    >
      <div>
        <h3 class="padded aligned spaced">
          Add a new Algo Provider
          <!-- <DocumentationBlock>TODO</DocumentationBlock> -->

          <button
            class="red"
            @click="newAlgoProviderModal = false"
          >
            Cancel
          </button>
        </h3>
        <form
          id="formNewAlgoProvider"
          class="dataGroup"
        >
          <!-- Algo Provider name -->
          <div class="data">
            <span class="name"> Name </span>
            <span class="value">
              <input
                type="text"
                v-model="algoProviderName"
                style="width: 300px"
              />
            </span>
          </div>
          <!-- Algo Provider description -->
          <div class="data">
            <span class="name">
              URL
              <DocumentationBlock>
                Must be a valid URL, with the protocol (http:// or https://)
                <br />
                Make sure the Algo Provider is running and accessible by the DebiAI instance.
              </DocumentationBlock>
            </span>
            <span class="value">
              <input
                type="text"
                v-model="algoProviderURL"
                style="width: 300px"
              />
            </span>
          </div>
          <!-- Save btn -->
          <button
            type="submit"
            @click="save"
            :disabled="!algoProviderNameOk"
          >
            Add
          </button>
        </form>
      </div>
    </modal>

    <!-- Use algo -->
    <modal
      v-if="algoToUse"
      @close="algoToUse = null"
    >
      <UseAlgorithm
        :algoProvider="algoProviderToUse"
        :algorithm="algoToUse"
        @cancel="algoToUse = null"
        @use="useAlgo(algoProviderToUse, algoToUse)"
      />
    </modal>

    <!-- Title & cancel btn -->
    <h2 class="aligned spaced padded-bot">
      Use an algorithm
      <!-- <DocumentationBlock>TODO</DocumentationBlock> -->

      <span>
        <button
          @click="newAlgoProviderModal = true"
          class="green"
        >
          + Add a new Algo Provider
        </button>
        <button
          class="warning"
          @click="loadAlgoProviders"
        >
          <inline-svg
            :src="require('../../../../../assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>

        <button
          @click="$emit('cancel')"
          class="red"
        >
          Close
        </button>
      </span>
    </h2>

    <!-- Algo Provider list -->
    <div
      id="algoProviders"
      class="itemList"
    >
      <!-- List algo providers -->
      <transition-group name="fade">
        <AlgoProvider
          v-for="algoProvider in algoProviders"
          :key="algoProvider.name"
          :algoProvider="algoProvider"
          @deleteAlgoProvider="deleteAlgoProvider(algoProvider.name)"
          @useAlgo="(algo) => selectAlgo(algoProvider, algo)"
        />
      </transition-group>

      <h4 v-if="algoProviders !== null && algoProviders.length === 0">No Algo Providers set</h4>
    </div>
  </div>
</template>

<script>
import AlgoProvider from "./AlgoProvider";
import UseAlgorithm from "./UseAlgorithm";

export default {
  name: "Algorithms",
  components: {
    AlgoProvider,
    UseAlgorithm,
  },
  props: {},
  data: () => {
    return {
      newAlgoProviderModal: false,
      algoProviderName: "New algoProvider",
      algoProviderURL: "http://localhost:3020/algoProvider",
      algoProviders: null, // null = loading, [] = empty, [algoProvider] = loaded

      algoToUse: null,
      algoProviderToUse: null,
    };
  },
  mounted() {
    // Load the saved Algorithms
    this.loadAlgoProviders();
  },
  methods: {
    loadAlgoProviders() {
      // this.algoProviders = null;
      this.$backendDialog
        .getAlgoProviders()
        .then((algoProviders) => {
          this.algoProviders = algoProviders;
          this.algoProviders.forEach((algoProvider) => {
            if (!algoProvider.algorithms) algoProvider.algorithms = [];
            algoProvider.algorithms.forEach((algo) => {
              // Add an empty experiments array to each algorithm
              algo.experiments = [];

              // Add an empty value array to each input
              if (!algo.inputs) algo.inputs = [];
              algo.inputs.forEach((input) => {
                input.value = null;
              });
            });
          });
        })
        .catch((e) => {
          console.log(e);
          this.algoProviders = [];
        });
    },
    save(e) {
      e.preventDefault();

      // Send the request
      this.$backendDialog
        .addAlgoProvider(this.algoProviderName, this.algoProviderURL)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Algo Provider added",
          });
          this.newAlgoProviderModal = false;
          this.algoProviderName = "New algoProvider";
          this.algoProviderURL = "http://localhost:3020/algoProvider";
          // this.$emit("cancel");
          this.loadAlgoProviders();
        })
        .catch((e) => {
          console.log(e);
          console.log(e.response);
          const resp = e.response?.data;
          this.$store.commit("sendMessage", {
            title: "error",
            msg: resp ? resp : "Couldn't add the algoProvider",
          });
        });
    },
    deleteAlgoProvider(algoProviderName) {
      this.$backendDialog
        .deleteAlgoProvider(algoProviderName)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Algo Provider removed",
          });
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't remove the algoProvider",
          });
        })
        .finally(() => {
          this.loadAlgoProviders();
        });
    },
    selectAlgo(algoProvider, algo) {
      this.algoToUse = algo;
      this.algoProviderToUse = algoProvider;
    },
    useAlgo(algoProvider, algo) {
      const inputs = algo.inputs.map((input) => {
        return {
          name: input.name,
          value: input.value,
        };
      });
      this.$backendDialog
        .useAlgorithm(algoProvider.name, algo.id, inputs)
        .then((results) => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "The algorithm has run successfully",
          });
          this.algoToUse = null;
          console.log(results);
          algo.experiments.push(results);
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't run the algorithm",
          });
        });
    },
  },
  computed: {
    algoProviderNameOk() {
      return this.algoProviderName.length > 0;
    },
  },
};
</script>

<style scoped>
#AlgorithmsSelection {
  /* text-align: left; */
  height: 80vh;
  width: 80vw;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 20px;
}

h3 {
  text-align: left;
  padding: 5px;
}

#newAlgoProvider {
  display: flex;
  justify-content: center;
}

#formNewAlgoProvider {
  flex-direction: column;
}

#formNewAlgoProvider .name {
  width: 100px;
}

#formNewAlgoProvider .value {
  flex: 1;
}

#algoProviders {
  overflow: auto;
  text-align: left;
  overscroll-behavior: contain;
}

#algoProviders h4 {
  padding: 15px;
}
</style>
