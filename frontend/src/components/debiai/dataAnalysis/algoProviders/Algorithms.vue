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
          <!-- addAlgoProvider btn -->
          <button
            type="submit"
            @click="addAlgoProvider"
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
        :algoProvider="selectedAlgoProvider"
        :algorithm="algoToUse"
        :data="data"
        @cancel="algoToUse = null"
        @use="useAlgo(selectedAlgoProvider, algoToUse)"
      />
    </modal>

    <!-- View experiments -->
    <modal
      v-if="algoToViewExperiments"
      @close="algoToViewExperiments = null"
    >
      <Experiments
        :algoProvider="selectedAlgoProvider"
        :algorithm="algoToViewExperiments"
        :data="data"
        @cancel="algoToViewExperiments = null"
      />
    </modal>

    <!-- Title & cancel btn -->
    <h2 class="aligned spaced padded-bot">
      <span class="aligned spaced">
        Use an algorithm
        <DocumentationBlock>
          DebiAI provides a way to use algorithms from other services as long as they respect the
          <b>algo-providers</b> API.
          <br />
          To demonstrate this, DebiAI provide an <b>integrated Algo-provider</b> that can be used to
          run algorithms on your data to generate metrics.
          <br />
          <br />
          <a
            href="https://debiai.irt-systemx.fr/dashboard/algoProviders/"
            target="_blank"
            >More information on our documentation.</a
          >
        </DocumentationBlock>
      </span>

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
            :src="require('@/assets/svg/update.svg')"
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
          @viewExperiments="(algo) => viewExperiments(algoProvider, algo)"
        />
      </transition-group>

      <h4 v-if="algoProviders !== null && algoProviders.length === 0">No Algo Providers set</h4>
    </div>
  </div>
</template>

<script>
import AlgoProvider from "./AlgoProvider";
import UseAlgorithm from "./UseAlgorithm";
import Experiments from "./Experiments";

export default {
  name: "Algorithms",
  components: {
    AlgoProvider,
    UseAlgorithm,
    Experiments,
  },
  props: {
    data: { type: Object, required: true },
  },
  data: () => {
    return {
      newAlgoProviderModal: false,
      algoProviderName: "New algoProvider",
      algoProviderURL: "http://localhost:3020/algoProvider",
      algoProviders: null, // null = loading, [] = empty, [algoProvider] = loaded

      algoToUse: null,
      algoToViewExperiments: null,
      selectedAlgoProvider: null,
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
    addAlgoProvider(e) {
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
      this.selectedAlgoProvider = algoProvider;
    },
    viewExperiments(algoProvider, algo) {
      this.algoToViewExperiments = algo;
      this.selectedAlgoProvider = algoProvider;
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

          const experiment = {
            results,
            inputs,
          };

          // Add the selected data to the experiment
          if (
            this.data.selectedData.length > 0 &&
            this.data.selectedData.length < this.data.nbLines
          ) {
            experiment.selectedData = this.data.selectedData;
          }

          this.$store.commit("addExperiment", {
            algoProviderName: algoProvider.name,
            algoId: algo.id,
            experiment: experiment,
          });
          this.loadAlgoProviders();
        })
        .catch((e) => {
          console.log(e);
          if (e.response?.data) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: e.response?.data,
            });
          }
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Error running the algorithm.",
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
