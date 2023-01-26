<template>
  <div>
    <div
      id="Widget"
      class="unselectable"
      @click="clicked"
      @dblclick="$emit('add', widget)"
    >
      <!-- Widget icon image -->
      <progressive-img
        :src="
          require(`@/components/debiai/statistics/dataAnalysis/widgets/${widget.componentKey}/icon.png`)
        "
        class="icon"
      />

      <div id="title">
        <div class="name">{{ widget.name }}</div>
        <div class="description">{{ widget.description }}</div>
      </div>
      <div class="control">
        <button class="green" @click="$emit('add', widget)">Add</button>
        <!-- configurations -->
        <transition name="fade">
          <span
            v-if="nbConfigurations && nbConfigurations > 0"
            style="display: flex; align-items: center; padding: 5px"
            title="Custom settings"
          >
            {{ nbConfigurations }}
            <inline-svg
              :src="require('../../../../../../assets/svg/preset.svg')"
              width="18"
              height="18"
            />
          </span>
        </transition>
      </div>
    </div>
    <transition name="scale">
      <div id="configurations" class="itemList" v-if="displayConfigurations">
        <WidgetConfList
          :widgetKey="widget.componentKey"
          :configurations="configurations"
          v-on:selected="
            (configuration) => {
              $emit('addWithConf', { widget, configuration });
            }
          "
          v-on:deleted="confDeleted()"
        />
      </div>
    </transition>
    <hr />
  </div>
</template>

<script>
import WidgetConfList from "../widgetConfiguration/WidgetConfList.vue";
import Vue from "vue";
import VueProgressiveImage from "vue-progressive-image";

Vue.use(VueProgressiveImage);

export default {
  components: { WidgetConfList },
  props: {
    widget: { requiered: true, type: Object },
    nbConfigurations: { type: Number, default: 0 },
  },
  data() {
    return {
      description: "",
      configurations: [], // [{ id, name, description, configuration, projectId, dataProviderId, creatinDate }]
      displayConfigurations: false,
    };
  },
  methods: {
    clicked() {
      this.$emit("selected");
      this.getConfigurations().then(() => {
        if (this.configurations.length > 0)
          this.displayConfigurations = !this.displayConfigurations;
      });
    },
    async getConfigurations() {
      this.configurations = [];

      // Load widget configurations
      this.configurations = await this.$backendDialog.getWidgetConfigurations(
        this.widget.componentKey
      );
    },
    confDeleted() {
      this.getConfigurations();
      this.$emit("confDeleted");
    },
  },
};
</script>

<style scoped>
#Widget {
  display: grid;
  grid-template-columns: min-content 1.4fr 0.3fr;
  grid-template-rows: 1fr;
  grid-template-areas: "icon title control";

  cursor: pointer;
  padding: 10px;
  transition: background-color ease-out 0.1s;
  background-color: white;
}
#Widget:hover {
  background-color: rgba(0, 0, 0, 0.076);
}

.icon {
  grid-area: icon;
  margin: 4px;
  width: 50px;
}

#title {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0px 0px;
  grid-template-areas:
    "name"
    "description";
  grid-area: title;
}
#title .name {
  grid-area: name;
  font-weight: bold;
  font-size: 1.2em;
  text-align: left;
  padding: 2px;
  padding-top: 4px;
}
#title .description {
  grid-area: description;
  text-align: left;
  opacity: 0.6;
}
.control {
  grid-area: control;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

hr {
  opacity: 0.2;
  margin: 0;
}
</style>