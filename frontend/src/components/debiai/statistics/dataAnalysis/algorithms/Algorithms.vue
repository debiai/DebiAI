<template>
  <div id="AlgorithmsSelection">
    <!-- New algo provider -->
    <modal
      v-if="newAlgoProviderModal"
      @close="newAlgoProviderModal = false"
    >
      <div>
        <h3 class="padded aligned">
          Add a new Algo Provider
          <!-- <DocumentationBlock>TODO</DocumentationBlock> -->
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
            <span class="name"> URL </span>
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
            Save the Algo Provider
          </button>
        </form>
      </div>
    </modal>

    <!-- Title & cancel btn -->
    <h2 class="aligned spaced padded-bot">
      Algorithms

      <span>
        <button
          @click="newAlgoProviderModal = true"
          class="green"
        >
          + Add a new Algo Provider
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
    <h3>
      Use an algorithm
      <!-- <DocumentationBlock>TODO</DocumentationBlock> -->
    </h3>
    <div
      id="algoProviders"
      class="itemList"
    >
      <h4 v-if="algoProviders.length === 0">No Algo Providers set</h4>
      <!-- List algo providers -->
      <AlgoProvider
        v-for="algoProvider in algoProviders"
        :key="algoProvider.name"
        :algoProvider="algoProvider"
        @deleteAlgoProvider="deleteAlgoProvider(algoProvider.name)"
      />
    </div>
  </div>
</template>

<script>
import AlgoProvider from "./AlgoProvider";

export default {
  name: "Algorithms",
  components: {
    AlgoProvider,
  },
  props: {},
  data: () => {
    return {
      newAlgoProviderModal: false,
      algoProviderName: "New algoProvider",
      algoProviderURL: "http://localhost:3020/algoProvider",
      algoProviders: [],
    };
  },
  mounted() {
    // Load the saved Algorithms
    this.loadAlgoProviders();
  },
  methods: {
    loadAlgoProviders() {
      this.algoProviders = [];
      this.$backendDialog
        .getAlgoProviders()
        .then((algoProviders) => {
          this.algoProviders = algoProviders;
        })
        .catch((e) => {
          console.log(e);
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
          this.loadAlgoProviders();
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't remove the algoProvider",
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
  min-height: 900px;
  min-width: 800px;
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
  max-height: 400px;
  text-align: left;
}

#algoProviders h4 {
  padding: 15px;
}
</style>
