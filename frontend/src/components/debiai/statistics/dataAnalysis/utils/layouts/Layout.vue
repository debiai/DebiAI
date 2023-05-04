<template>
  <div
    class="layout item selectable"
    @click="(event) => click(event)"
  >
    <div class="left">
      <div
        class="tag"
        v-if="layout.lastLayoutSaved"
      >
        Last layout used
      </div>
      <h4 style="display: flex; align-items: center">
        {{ layout.name }}
        <!-- Display layout : -->
      </h4>

      <span
        class="creationDate"
        :title="$services.timeStampToDate(layout.creationDate)"
      >
        Created {{ $services.prettyTimeStamp(layout.creationDate) }}
      </span>
    </div>

    <div class="center">
      <div class="description">{{ layout.description }}</div>
      <LayoutViewer :layout="layout.layout" />
    </div>

    <div class="right">
      <button
        class="red"
        @click="(event) => deleteLayout(event)"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import LayoutViewer from "./LayoutViewer.vue";

export default {
  name: "Layout",
  components: {
    LayoutViewer,
  },
  props: {
    layout: { type: Object, required: true },
  },
  methods: {
    deleteLayout(event) {
      event.stopPropagation();
      this.$backendDialog
        .deleteLayout(this.layout.id)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Layout deleted",
          });
          this.$emit("deleted");
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the layout",
          });
        });
    },
    click(event) {
      event.stopPropagation();
      this.$emit("selected");
    },
  },
};
</script>

<style scoped>
.layout {
  display: flex;
  align-items: stretch;
  gap: 30px;
  padding: 5px;
}

.layout .left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 100px;
  padding: 10px;
  text-align: left;
}
.layout .left .tag {
  border: 2px solid rgb(70, 70, 70);
  padding: 3px;
  border-radius: 5px;
  font-size: 0.8em;
  margin-bottom: 5px;
  opacity: 0.3;
  font-weight: bold;
}
.layout .center {
  flex: 1;
  display: flex;
  justify-content: space-evenly;
  gap: 20px;
}
.layout .center .description {
  padding: 10px;
}
.layout .right {
  display: flex;
  align-items: center;
}
.layout .creationDate {
  text-align: right;
  font-size: 0.7em;
  opacity: 0.7;
}
.layout .description {
  flex: 1;
  text-align: left;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-width: 300px;
  opacity: 0.7;
  font-size: 0.8em;
}
.layout .value {
  text-align: left;
}
</style>
