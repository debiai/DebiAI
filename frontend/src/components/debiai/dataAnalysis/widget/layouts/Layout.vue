<template>
  <div
    class="layout item selectable"
    @click="layoutSelected"
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

      <div
        class="coloredColumn"
        v-if="layout.selectedColorColumn"
      >
        Colored column:
        <u>
          {{ layout.selectedColorColumn }}
        </u>
      </div>

      <p class="description">
        {{ layout.description }}
      </p>
    </div>

    <div class="right">
      <LayoutViewer :layout="layout.layout" />

      <button
        class="red"
        @click="deleteLayout"
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
    layoutSelected(event) {
      event.stopPropagation();
      this.$emit("selected");
    },
  },
};
</script>

<style scoped lang="scss">
.layout {
  display: flex;
  align-items: stretch;
  gap: 30px;
  padding: 5px;

  .left {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
    text-align: left;

    .tag {
      margin-bottom: 5px;
      font-size: 0.8em;
    }
  }

  .center {
    flex: 1;
    display: flex;
    justify-content: space-evenly;
    gap: 20px;

    .description {
      padding: 10px;
    }
  }

  .right {
    display: flex;
    align-items: center;
  }

  .creationDate {
    color: var(--fontColorLight);
  }

  .coloredColumn {
    color: var(--fontColorLight);
  }

  .description {
    max-width: 300px;
    color: var(--fontColorLight);
    margin-top: 10px;
  }

  .value {
    text-align: left;
  }
}
</style>
