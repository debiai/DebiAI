<template>
  <div id="dataProviders">
    <!-- Title -->
    <div id="title" class="aligned spaced">
      <h2>Data providers</h2>
      <div id="controls">
        <button class="warning" @click="getDataProviders">
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
        <button class="red" @click="$emit('cancel')">Cancel</button>
      </div>
    </div>
    <!-- Data provider list -->
    <transition name="fade">
      <div v-if="dataProviders" class="itemList marged">
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
              <div class="type">{{ dataProvider.type }}</div>
              <div>{{ dataProvider.url }}</div>
            </div>
          </div>
          <!-- Status -->
          <div v-if="dataProvider.type === 'Web'">
            <div class="status available" v-if="dataProvider.status">
              ✓ Available
            </div>
            <div class="status notavailable" v-else>❌ Not available</div>
          </div>
          <div v-if="dataProvider.type === 'Python module Data Provider'">
            <div class="status available">✓ Available</div>
          </div>

          <!-- Actions -->
          <div class="controls" v-if="dataProvider.type === 'Web'">
            <!-- <button @click="getDataProviders">Retry</button> -->
            <button class="red" @click="deleteDataProvider(dataProvider.name)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </transition>
    <div v-if="!dataProviders">Loading...</div>
    <div v-else-if="dataProviders.length === 0">No data providers</div>

    <!-- new dataprovider modal -->
    <modal v-if="newDataProviderModal">
      <NewDataProvider
        @cancel="newDataProviderModal = false"
        @done="
          newDataProviderModal = false;
          getDataProviders();
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
    getDataProviders() {
      this.dataProviders = null;
      this.$backendDialog.getDataProviders().then((dataProviders) => {
        this.dataProviders = dataProviders;
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
          this.getDataProviders();
        })
        .catch((error) => {
          console.log(error);
          if (
            error.response &&
            error.response.status !== 500 &&
            error.response.data
          ) {
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
.dataProvider .data .type {
  text-align: left;
  font-size: 0.9em;
  color: #666;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  padding: 3px;
}

.dataProvider .controls {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.3rem;
}

/* Status */
.dataProvider .status {
  padding: 0.2rem 0.5rem;
  font-size: 0.9em;
  font-weight: bold;
  border-radius: 0.5rem;
  border: 2px solid;
}
.dataProvider .status.available {
  color: var(--success);
  border-color: var(--success);
}
.dataProvider .status.notavailable {
  color: var(--danger);
  border-color: var(--danger);
}
</style>