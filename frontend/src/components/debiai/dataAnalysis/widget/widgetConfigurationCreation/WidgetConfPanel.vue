<template>
  <div id="WidgetConfPanel">
    <!-- Panel title & cancel button -->
    <div
      id="heading"
      class="aligned spaced"
    >
      <h3 id="title">Widget Configuration</h3>
      <span class="aligned">
        <button
          class="warning"
          @click="loadWidgetConfigurations"
        >
          <inline-svg
            :src="require('@/assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>
        <button
          class="red"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
      </span>
    </div>
    <div id="content">
      <!-- Widget name form & configuration creator -->
      <div id="left">
        <!-- Widget configuration creator -->
        <WidgetConfCreator
          :widgetConf="confToSave"
          :widgetTitle="widgetTitle"
          :widgetKey="widgetKey"
          :suggestedConfName="suggestedConfName"
          @saved="(confName) => $emit('saved', confName)"
          class="card"
        />
      </div>
      <!-- Widget configuration selector -->
      <div
        id="WidgetConfSelector"
        class="card"
      >
        <h3>Saved widget configuration</h3>
        <transition name="fade">
          <WidgetConfList
            :configurations="configurations"
            :widgetKey="widgetKey"
            v-on:selected="
              (configuration) => {
                $emit('confSelected', configuration);
              }
            "
            v-on:deleted="loadWidgetConfigurations()"
          />
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import WidgetConfCreator from "./WidgetConfCreator";
import WidgetConfList from "../widgetConfiguration/WidgetConfList";

export default {
  components: { WidgetConfCreator, WidgetConfList },
  props: {
    confToSave: { type: Object, required: true },
    widgetKey: { type: String, required: true },
    widgetTitle: { type: String, required: true },
    widgetName: { type: String, default: "" },
    suggestedConfName: { type: String, default: "" },
  },
  data() {
    return {
      newWidgetName: "",
      configurations: [], // [{ id, name, description, configuration, projectId, dataProviderId, creationDate }]
    };
  },
  created() {
    this.loadWidgetConfigurations();
    this.newWidgetName = this.widgetName;
  },
  methods: {
    loadWidgetConfigurations() {
      this.configurations = [];

      this.$backendDialog
        .getWidgetConfigurations(this.widgetKey)
        .then((confList) => {
          this.configurations = confList;
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
};
</script>

<style scoped>
#WidgetConfPanel {
  min-width: 65vw;
  display: flex;
  flex-direction: column;
  text-align: left;
}
#content {
  flex: 1;
  display: flex;
}
#content .card {
  padding: 10px;
  flex: 1;
}
#WidgetConfSelector {
  min-width: 400px;
  text-align: left;
}
#WidgetConfSelector #configurations {
  height: 70vh;
  overflow-y: auto;
}
</style>
