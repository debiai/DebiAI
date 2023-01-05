<template>
  <div id="dataProviders">
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
          <!-- Status and actions -->
          <div class="controls" v-if="dataProvider.type === 'Web'">
            <div class="status available" v-if="dataProvider.status">
              ✓ Available
            </div>
            <div class="status notavailable" v-else>❌ Not available</div>
            <button @click="getDataProviders">Retry</button>
          </div>
          <div
            class="controls"
            v-if="dataProvider.type === 'Python module Data Provider'"
          >
            <div class="status available">✓ Available</div>
          </div>
        </div>
      </div>
    </transition>
    <div v-if="!dataProviders">Loading...</div>
  </div>
</template>

<script>
export default {
  name: "DataProviders",
  data() {
    return {
      dataProviders: null,
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
  },
};
</script>

<style scoped>
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
.dataProvider .controls .status {
  padding: 0.2rem 0.5rem;
  font-size: 0.8em;
}
.dataProvider .controls .status.available {
  color: rgb(43, 134, 43);
  border: 1px solid rgb(43, 134, 43);
  border-radius: 0.5rem;
}
.dataProvider .controls .status.notavailable {
  color: #f00;
  border: 1px solid #f00;
  border-radius: 0.5rem;
}
</style>