<template>
  <div id="layouts">
    <!-- Title & cancel btn -->
    <h2 class="aligned spaced padded-bot">
      Dashboard layouts

      <button
        @click="$emit('cancel')"
        class="red"
      >
        Close
      </button>
    </h2>

    <!-- Layout save -->
    <div
      id="layoutSave"
      class="aligned"
    >
      <!-- Form -->
      <div>
        <h3 class="padded">Save the current layout</h3>
        <form
          id="formNewLayout"
          class="dataGroup"
        >
          <!-- Layout name -->
          <div class="data">
            <span class="name"> Name </span>
            <span class="value">
              <input
                type="text"
                v-model="layoutName"
                style="flex: 1"
              />
            </span>
          </div>
          <!-- Layout description -->
          <div class="data">
            <span class="name"> Description </span>
            <span class="value">
              <textarea
                v-model="layoutDescription"
                style="height: 50px; flex: 1"
                placeholder="Optional layout description"
              />
            </span>
          </div>
          <!-- Save btn -->
          <button
            type="submit"
            @click="save"
            :disabled="!layoutNameOk"
          >
            Save the layout
          </button>
        </form>
      </div>

      <!-- LayoutVisualisation -->
      <LayoutViewer :layout="layout" />
    </div>

    <!-- Layout loads -->
    <h3>Load a saved layout</h3>

    <div
      id="savedLayouts"
      class="itemList"
    >
      <div v-if="savedLayouts.length == 0">
        No saved layout
      </div>
      <div
        class="layout item selectable"
        v-for="layout in savedLayouts"
        :key="layout.id"
      >
        <div class="left">
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
            @click="deleteLayout(layout.id)"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LayoutViewer from "@/components/utils/LayoutViewer.vue";

export default {
  name: "Layouts",
  components: {
    LayoutViewer,
  },
  props: {
    components: { type: Array, required: true },
    gridstack: { type: Object, required: true },
  },
  data: () => {
    return {
      layout: [],
      layoutName: "New layout",
      layoutDescription: "",
      savedLayouts: [],
    };
  },
  mounted() {
    // Get the current layout from the gridstack
    let gsPos = this.gridstack.save();
    this.layout = [];
    gsPos.forEach((gsComp) => {
      const gridComponent = this.components.find((c) => gsComp.id == c.id);
      if (!gridComponent) return;

      // Add the widgetKey and config to the layout
      gsComp.widgetKey = gridComponent.widgetKey;
      gsComp.config = gridComponent.config;

      this.layout.push(gsComp);
    });
    console.log(this.layout);

    // Load the saved layouts
    this.loadLayouts();
  },
  methods: {
    loadLayouts() {
      this.layouts = [];
      this.$backendDialog
        .getLayouts()
        .then((layouts) => {
          this.savedLayouts = layouts;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    save(e) {
      e.preventDefault();

      console.log(this.components);
      const requestBody = {
        name: this.layoutName,
        description: this.layoutDescription,
        layout: [],
      };

      // Expected layout:
      // [{ x, y, w, h, widgetKey, config }];

      this.layout.forEach((component) => {
        requestBody.layout.push({
          x: component.x,
          y: component.y,
          width: component.width,
          height: component.height,
          widgetKey: component.widgetKey,
          config: component.config,
        });
      });

      // Send the request
      this.$backendDialog
        .saveLayout(requestBody)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Layout saved",
          });
          this.$emit("cancel");
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't save the layout",
          });
        });
    },
    deleteLayout(layoutId) {
      this.$backendDialog
        .deleteLayout(layoutId)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Layout deleted",
          });
          this.loadLayouts();
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the layout",
          });
        });
    },
  },
  computed: {
    layoutNameOk() {
      return this.layoutName.length > 0;
    },
  },
};
</script>

<style scoped>
#layouts {
  /* text-align: left; */
  max-height: 900px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 40px;
}
h3 {
  text-align: left;
  padding: 5px;
}

#layoutSave {
  display: flex;
  justify-content: center;
}
#formNewLayout {
  flex-direction: column;
}
#formNewLayout .name {
  width: 100px;
}
#formNewLayout .value {
  flex: 1;
}

#savedLayouts {
  overflow: auto;
  max-height: 400px;
}
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
}
.layout .center {
  flex: 1;
  display: flex;
  justify-content: space-evenly;
  gap: 20px;
}
.layout .center .description{
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
