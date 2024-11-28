<template>
  <div id="layouts">
    <!-- New layout modal -->
    <Modal
      v-if="showNewLayoutModal"
      @close="showNewLayoutModal = false"
      :errorMessages="[!layoutNameOk ? 'The layout name can\'t be empty' : '']"
    >
      <div id="newLayoutModal">
        <!-- Title -->
        <span class="aligned spaced padded-bot">
          <h3 class="aligned">
            Save the current layout
            <DocumentationBlock>
              Saving the current layout will save the position of the widgets on the dashboard.
              <br />
              The current configuration of the widgets will also be saved, it will be used when
              loading the layout back.
              <br />
              <a
                href="https://debiai.irt-systemx.fr/dashboard/layouts/"
                target="_blank"
                >Layouts documentation</a
              >.
            </DocumentationBlock>
          </h3>

          <button
            @click="showNewLayoutModal = false"
            class="red"
          >
            Cancel
          </button>
        </span>

        <!-- Form -->
        <form id="formNewLayout">
          <!-- Left -->
          <div id="left">
            <!-- Layout name -->
            <span class="name"> Layout name </span>
            <span class="value">
              <input
                type="text"
                v-model="layoutName"
                style="flex: 1"
              />
            </span>
            <!-- Layout description -->
            <span class="name"> Description </span>
            <span class="value">
              <textarea
                v-model="layoutDescription"
                style="height: 50px; flex: 1"
                placeholder="Optional layout description"
              />
            </span>

            <!-- Save btn -->
            <button
              type="submit"
              @click="save"
              :disabled="!layoutNameOk"
            >
              Save the layout
            </button>
          </div>

          <!-- Right -->
          <div id="right">
            <!-- LayoutVisualization -->
            <LayoutViewer
              :layout="currentLayout"
              bigger
            />
          </div>
        </form>
      </div>
    </Modal>

    <!-- Title & cancel btn -->
    <span class="aligned spaced padded-bot">
      <h2 class="aligned">Dashboard layouts</h2>

      <span class="aligned">
        <button
          @click="showNewLayoutModal = true"
          class="green"
        >
          Save the current layout
        </button>
        <button
          @click="$emit('cancel')"
          class="red"
        >
          Close
        </button>
      </span>
    </span>

    <!-- Layout list -->
    <div
      id="savedLayouts"
      v-if="savedLayouts !== null"
    >
      <!-- Project layouts -->
      <div>
        <h4 class="layoutList">Project layouts:</h4>
        <div class="itemList">
          <Layout
            v-for="layout in sameProjectLayouts"
            :key="layout.id"
            :layout="layout"
            v-on:selected="$emit('selected', layout)"
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
      <!-- Rest of the layouts -->
      <div>
        <h4 class="layoutList">Other layouts:</h4>
        <div class="itemList">
          <Layout
            v-for="layout in otherLayouts"
            :key="layout.id"
            :layout="layout"
            v-on:selected="$emit('selected', layout)"
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

    <div
      v-else
      style="flex: 1; display: flex; justify-content: center; align-items: center"
    >
      <LoadingAnimation />
    </div>
  </div>
</template>

<script>
import LayoutViewer from "./LayoutViewer.vue";
import Layout from "./Layout";

export default {
  name: "Layouts",
  components: {
    LayoutViewer,
    Layout,
  },
  props: {
    data: { type: Object, required: true },
    components: { type: Array, required: true },
    gridstack: { type: Object, required: true },
  },
  data: () => {
    return {
      currentLayout: [],
      savedLayouts: null,

      showNewLayoutModal: false,
      layoutName: "New layout",
      layoutDescription: "",
    };
  },
  mounted() {
    // Load the saved layouts
    this.loadLayouts();

    // Get the current layout from the gridstack
    let gsPos = this.gridstack.save();
    this.currentLayout = [];
    gsPos.forEach((gsComp) => {
      const gridComponent = this.components.find((c) => gsComp.id == c.id);
      if (!gridComponent) return;

      // Add the widgetKey and config to the layout
      gsComp.widgetKey = gridComponent.widgetKey;
      gsComp.config = gridComponent.config;

      this.currentLayout.push(gsComp);
    });
  },
  methods: {
    loadLayouts() {
      this.$backendDialog
        .getLayouts()
        .then((layouts) => {
          this.savedLayouts = layouts;

          // Sort the layouts by creation date
          this.savedLayouts.sort((a, b) => {
            return new Date(b.creationDate) - new Date(a.creationDate);
          });
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't load the layouts",
          });
          this.savedLayouts = [];
        });
    },
    save(e) {
      e.preventDefault();
      this.$emit("save", {
        name: this.layoutName,
        description: this.layoutDescription,
      });
      this.showNewLayoutModal = false;
      this.layoutName = "New layout";
      this.layoutDescription = "";
      this.savedLayouts = null;
      // The layout is saved in the parent component,
      // the parent will call this.loadLayouts() when the layout is saved
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
      if (!this.savedLayouts) return [];

      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      const projectId = this.$store.state.ProjectPage.projectId;

      return this.savedLayouts.filter(
        (layout) => layout.projectId === projectId && layout.dataProviderId === dataProviderId
      );
    },
    otherLayouts() {
      if (!this.savedLayouts) return [];

      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      const projectId = this.$store.state.ProjectPage.projectId;

      return this.savedLayouts.filter(
        (layout) => layout.dataProviderId !== dataProviderId || layout.projectId !== projectId
      );
    },
  },
};
</script>

<style scoped lang="scss">
#layouts {
  min-width: 800px;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
h3 {
  text-align: left;
  padding: 5px;
}

/* Layout save */
#newLayoutModal {
  min-width: 700px;

  #formNewLayout {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    align-items: stretch;
    padding-left: 20px;

    input,
    textarea {
      flex: 1;
      margin: 10px;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid var(--greyDark);
      transition: border-color 0.2s;
      width: 350px;
    }

    #left {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;

      button {
        align-self: flex-end;
      }
    }
  }
}

/* Layout load */
#savedLayouts {
  overflow: auto;
  max-height: 65vh;
  text-align: left;
}
#savedLayouts h4 {
  padding: 15px;
}
</style>
