<template>
  <div id="dataProviders">
    <!-- Title -->
    <div
      id="title"
      class="aligned spaced"
    >
      <h2>Data providers</h2>
      <div id="controls">
        <button
          class="warning"
          @click="getDataProviders(true)"
        >
          <inline-svg
            :src="require('@/assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>
        <button
          id="newDataProvider"
          @click="newDataProviderModal = !newDataProviderModal"
        >
          New data provider
        </button>
        <button
          class="red"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
      </div>
    </div>
    <!-- Data provider list -->
    <transition name="fade">
      <div
        v-if="dataProviders"
        class="itemList marged"
      >
        <div
          v-for="dataProvider in dataProviders"
          :key="dataProvider.id"
          class="dataProvider item"
        >
          <!-- Info (name, url, type)-->
          <div class="info">
            <div class="head">
              <b>{{ dataProvider.name }}</b>
            </div>
            <div class="data">
              <div class="type tag">{{ dataProvider.type }}</div>
              <div>{{ dataProvider.url }}</div>
            </div>
          </div>
          <!-- Status -->
          <AvailableTag
            v-if="dataProvider.type === 'Web'"
            :available="dataProvider.status"
          />
          <AvailableTag
            v-if="dataProvider.type === 'Python module Data Provider'"
            available
          />

          <!-- Actions -->
          <div
            class="controls"
            v-if="dataProvider.type === 'Web'"
          >
            <button
              class="red"
              @click="deleteDataProvider(dataProvider.name)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </transition>
    <div v-if="!dataProviders">Loading...</div>
    <div v-else-if="dataProviders.length === 0">No data providers</div>

    <!-- new dataprovider modal -->
    <modal
      v-if="newDataProviderModal"
      @close="newDataProviderModal = false"
    >
      <NewDataProvider
        @cancel="newDataProviderModal = false"
        @done="
          newDataProviderModal = false;
          getDataProviders(true);
        "
      />
    </modal>
  </div>
</template>

<script>
import NewDataProvider from "./NewDataProvider.vue";
export default {
  name: "DataProviders",
  components: {
    NewDataProvider,
  },
  data() {
    return {
      dataProviders: null,
      newDataProviderModal: false,
    };
  },
  created() {
    this.getDataProviders();
  },
  methods: {
    getDataProviders(refresh = false) {
      this.dataProviders = null;
      this.$backendDialog.getDataProviders().then((dataProviders) => {
        this.dataProviders = dataProviders;
        if (refresh) this.$emit("refresh");
      });
    },
    deleteDataProvider(name) {
      this.$backendDialog
        .deleteDataProvider(name)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Data provider deleted",
          });
          this.getDataProviders(true);
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status !== 500 && error.response.data) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: error.response.data,
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Error deleting data provider",
            });
          }
        });
    },
  },
};
</script>

<style scoped>
#title h2 {
  text-align: left;
  width: 300px;
}
#controls {
  display: flex;
  gap: 0.5rem;
}

.dataProvider {
  min-width: 400px;
  display: flex;
  padding: 0.5rem;
  margin: 0.5rem 0;
  justify-content: space-between;
}
.dataProvider .info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.dataProvider .data {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 0.5rem;
}

.dataProvider .controls {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.3rem;
}
</style>
