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
        <h3 class="padded aligned">
          Save the current layout
          <DocumentationBlock>
            Saving the current layout will save the position of the widgets on the dashboard. <br />
            The current configuration of the widgets will also be saved, it will be used when
            loading the layout back.
          </DocumentationBlock>
        </h3>
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

    <!-- Layout list -->
    <h3>Load a saved layout</h3>
    <div id="savedLayouts">
      <div>
        <h4 class="layoutList">Project layouts:</h4>
        <div class="itemList">
          <Layout
            v-for="layout in sameProjectLayouts"
            :key="layout.id"
            :layout="layout"
            v-on:selected="$emit('selected', layout.layout)"
            v-on:deleted="loadLayouts"
          />
          <div
            class="item"
            style="color: brown"
            v-if="sameProjectLayouts.length === 0"
          >
            No layout saved for this project
          </div>
        </div>
      </div>
      <div>
        <h4 class="layoutList">Other layouts:</h4>
        <div class="itemList">
          <Layout
            v-for="layout in otherLayouts"
            :key="layout.id"
            :layout="layout"
            v-on:selected="$emit('selected', layout.layout)"
            v-on:deleted="loadLayouts"
          />
          <div
            class="item"
            style="color: brown"
            v-if="otherLayouts.length === 0"
          >
            No layout saved for other projects
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LayoutViewer from "./LayoutViewer.vue";
import Layout from "./Layout"

export default {
  name: "Layouts",
  components: {
    LayoutViewer,
    Layout,
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
          // this.$emit("cancel");
          this.loadLayouts();
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
    sameProjectLayouts() {
      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      const projectId = this.$store.state.ProjectPage.projectId;

      return this.savedLayouts.filter(
        (layout) => layout.projectId === projectId && layout.dataProviderId === dataProviderId
      );
    },

    otherLayouts() {
      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      const projectId = this.$store.state.ProjectPage.projectId;

      return this.savedLayouts.filter(
        (layout) => layout.dataProviderId !== dataProviderId || layout.projectId !== projectId
      );
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
  gap: 20px;
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
  text-align: left;
}
#savedLayouts h4 {
  padding: 15px;
}
</style>
