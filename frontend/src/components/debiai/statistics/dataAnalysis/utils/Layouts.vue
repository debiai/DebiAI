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
    <div class="aligned">
      <!-- Form -->
      <div>
        <h3 class="padded">Save the current layout</h3>
        <form
          id="saveLayout"
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
      id="layouts"
      class="itemList"
    >
      <div
        class="layout item selectable"
        v-for="layout in savedLayouts"
        :key="layout.id"
      >
        <div class="header">
          <h4 style="display: flex; align-items: center">
            {{ layout.name }}
            <!-- Display layout : -->
            <DocumentationBlock>
              <LayoutViewer :layout="layout.layout" />
            </DocumentationBlock>
          </h4>

          <button
            class="red"
            @click="deleteLayout(layout.id)"
          >
            Delete
          </button>
        </div>
        <div class="body">
          <span
            class="creationDate"
            :title="$services.timeStampToDate(layout.creationDate)"
          >
            Created {{ $services.prettyTimeStamp(layout.creationDate) }}
          </span>
          <div class="description">{{ layout.description }}</div>
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
          console.log(layouts);
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
}
h3 {
  text-align: left;
  padding: 5px;
}
#saveLayout {
  flex-direction: column;
}
#saveLayout .name {
  width: 100px;
}
#saveLayout .value {
  flex: 1;
}

.layout {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.layout .header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.layout .body {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
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
