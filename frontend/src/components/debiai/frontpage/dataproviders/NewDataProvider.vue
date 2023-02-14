<template>
  <div id="newDataProviders">
    <!-- Title -->
    <div
      id="title"
      class="aligned spaced"
    >
      <h2>Creating a new data provider</h2>
      <div id="controls">
        <button
          class="red"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
      </div>
    </div>

    <!-- Data provider list -->
    <div class="itemList marged">
      <!-- Web data provider -->
      <div class="dataProvider item">
        <b> Web data provider </b>
        <div class="info">
          <div class="head">
            Data provider name
            <input
              type="text"
              v-model="dpName"
            />
          </div>
          <div class="data">
            <div>
              Data provider URL
              <input
                type="text"
                v-model="dpUrl"
              />
            </div>
          </div>
        </div>
        <!-- actions -->
        <div class="controls">
          <button
            @click="createWebDataProvider"
            :disabled="!canCreate"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewDataProvider",
  data() {
    return {
      dpName: "New data provider",
      dpUrl: "http://",
    };
  },
  methods: {
    createWebDataProvider() {
      this.$backendDialog
        .postDataProvider("Web", this.dpName, this.dpUrl)
        .then(() => {
          this.$emit("done");
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Data provider created",
          });
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
              msg: "Error creating data provider",
            });
          }
        });
    },
  },
  computed: {
    canCreate() {
      return this.dpName && this.dpUrl;
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
  gap: 1rem;
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
