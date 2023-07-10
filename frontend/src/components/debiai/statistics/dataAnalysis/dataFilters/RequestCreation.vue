<template>
  <div id="requestCreation">
    <form v-on:submit.prevent>
      <b
        >Create a request from the current filters
        <button
          @click="$emit('cancel')"
          class="red"
        >
          Cancel
        </button>
      </b>
      <div class="dataGroup">
        <!-- Request name -->
        <div class="data">
          <div class="name">Request name</div>
          <div class="value">
            <input
              type="text"
              v-model="requestName"
              style="flex: 1"
            />
          </div>
        </div>
        <!-- nb filters:  -->
        <div class="data">
          <div class="name">Number of filters</div>
          <div class="value">
            {{ filters.length }}
          </div>
        </div>
        <!-- request Description -->
        <div class="data">
          <div class="name">Description</div>
          <div class="value">
            <textarea
              cols="30"
              rows="5"
              v-model="requestDescription"
            ></textarea>
          </div>
        </div>
      </div>
      <div style="display: flex; justify-content: flex-end">
        <button
          type="submit"
          @click="save"
          :disabled="!requestNameOk"
        >
          Save
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "RequestCreator",
  data() {
    return {
      requestName: "New Request",
      requestDescription: "",
    };
  },
  props: {},
  methods: {
    save() {
      this.$backendDialog
        .addRequest(this.requestName, this.requestDescription, this.filters)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Request saved successfully",
          });
          this.$emit("cancel");
        })
        .catch(() => {
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't save the request",
          });
        });
    },
  },
  computed: {
    requestNameOk() {
      return this.requestName.length > 0;
    },
    filters() {
      return this.$store.state.StatisticalAnalysis.filters.map((f) => {
        f.columnLabel = f.column.label;
        return f;
      });
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
}

.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 4px;
}
.dataGroup .value {
  flex: 1;
}
</style>
