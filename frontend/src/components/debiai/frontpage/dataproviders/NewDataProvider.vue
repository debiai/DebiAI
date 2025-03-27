<template>
  <div id="newDataProviders">
    <!-- Title -->
    <div
      id="title"
      class="aligned spaced"
    >
      <h2>Add a data provider</h2>
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
      <form
        class="dataProvider item"
        @submit.prevent="createWebDataProvider"
      >
        <b> Web data provider </b>
        <div class="fields">
          <div class="field">
            Name:
            <input
              type="text"
              v-model="dpName"
            />
          </div>
          <div class="field">
            URL:
            <input
              type="text"
              v-model="dpUrl"
            />
          </div>
        </div>
        <div class="controls">
          <button
            type="submit"
            :disabled="!canCreate"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewDataProvider",
  props: {
    suggestedName: {
      type: String,
      default: "Data Provider",
    },
  },
  data() {
    return {
      dpName: this.suggestedName,
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

<style lang="scss" scoped>
#title {
  h2 {
    text-align: left;
    width: 300px;
  }
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

  .data {
    display: flex;
    width: 100%;
    align-items: center;
    gap: 0.5rem;
  }

  .controls {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.3rem;
  }
}
</style>
