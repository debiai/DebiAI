<template>
  <div id="WidgetConfPannel">
    <!-- Pannel title & cancel button -->
    <div id="heading" class="aligned spaced">
      <h3 id="title">Widget Configuration</h3>
      <span>
        <button class="warning" @click="loadWidgetConfigurations">
          <inline-svg
            :src="require('../../../../../../assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>
        <button class="red" @click="$emit('cancel')">Cancel</button>
      </span>
    </div>
    <div id="content">
      <!-- Widget name form & conf creator -->
      <div id="left">
        <!-- Change widget name form -->
        <form id="widgetNameForm" class="card">
          <span class="aligned spaced">
            <h4>Change the widget name</h4>
            <input
              type="text"
              v-model="newWidgetName"
              placeholder="New widget name"
            />
            <button
              @click="$emit('setWidgetName', newWidgetName)"
              :disabled="newWidgetName.length < 1"
            >
              Change
            </button>
          </span>
        </form>
        <!-- Widget conf creator -->
        <WidgetConfCreator
          :widgetConf="confToSave"
          :widgetTitle="widgetTitle"
          :createdConf="configurations"
          :widgetKey="widgetKey"
          :suggestedConfName="suggestedConfName"
          @saved="(confName) => $emit('saved', confName)"
          class="card"
        />
      </div>
      <!-- Widget conf selector -->
      <div id="WidgetConfSelector" class="card">
        <h3>Select a widget configuration</h3>
        <transition name="fade">
          <div id="configurations">
            <WidgetConfiguration
              v-for="(conf, i) in configurations"
              :key="i"
              :conf="conf"
              v-on:selected="$emit('confSelected', conf)"
              v-on:delete="deleteConf(conf.name)"
            />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import WidgetConfCreator from "./WidgetConfCreator";
import WidgetConfiguration from "./WidgetConfiguration";

export default {
  components: { WidgetConfCreator, WidgetConfiguration },
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
      configurations: [], // [{ id, name, description, configuration, projectId, dataProviderId, creatinDate }]
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
    deleteConf(name) {
      let projectId = this.$store.state.ProjectPage.projectId;

      this.$backendDialog
        .deleteWidgetConfiguration(projectId, {
          widgetKey: this.widgetKey,
          name,
        })
        .then((confList) => {
          this.$backendDialog;
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Configuration deleted",
          });

          this.configurations = confList[this.widgetKey];
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the configuration",
          });
        });
    },
  },
};
</script>

<style scoped>
#WidgetConfPannel {
  min-width: 65vw;
  display: flex;
  flex-direction: column;
  text-align: left;
}
#widgetNameForm {
  display: flex;
  padding: 10px;
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
  text-align: left;
}
#WidgetConfSelector #configurations {
  height: 70vh;
  overflow-y: auto;
}
</style>