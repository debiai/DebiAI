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
    <!-- TODO -->
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
    };
  },
  mounted() {
    // Get the current layout from the gridstack
    let gsPos = this.gridstack.save();
    this.layout = [];
    gsPos.forEach((gsComp) => {
      const gridComponent = this.components.find((c) => gsComp.id == c.id);
      if (!gridComponent) return;

      // Add the key and config to the layout
      gsComp.key = gridComponent.key;
      gsComp.config = gridComponent.config;
      this.layout.push(gsComp);
    });
  },
  methods: {
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
          w: component.width,
          h: component.height,
          widgetKey: component.key,
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
#saveLayout {
  flex-direction: column;
}
#saveLayout .name {
  width: 100px;
}
#saveLayout .value {
  flex: 1;
}
</style>
