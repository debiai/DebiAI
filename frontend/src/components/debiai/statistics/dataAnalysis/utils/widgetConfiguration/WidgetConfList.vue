<template>
  <div id="configurations">
    <div v-if="sameProjectConfigurations.length > 0">
      <h4 class="configurationType">Project configurations:</h4>
      <div class="itemList">
        <WidgetConf
          v-for="configuration in sameProjectConfigurations"
          :key="configuration.id"
          :configuration="configuration"
          :widgetKey="widgetKey"
          v-on:selected="$emit('selected', configuration)"
          v-on:deleted="$emit('deleted')"
        />
      </div>
    </div>
    <div v-if="sameDataProviderConfigurations.length > 0">
      <h4 class="configurationType">Data provider configurations:</h4>
      <div class="itemList">
        <WidgetConf
          v-for="configuration in sameDataProviderConfigurations"
          :key="configuration.id"
          :configuration="configuration"
          :widgetKey="widgetKey"
          v-on:selected="$emit('selected', configuration)"
          v-on:deleted="$emit('deleted')"
        />
      </div>
    </div>
    <div v-if="otherConfigurations.length > 0">
      <h4 class="configurationType">Other configurations:</h4>
      <div class="itemList">
        <WidgetConf
          v-for="configuration in otherConfigurations"
          :key="configuration.id"
          :configuration="configuration"
          :widgetKey="widgetKey"
          v-on:selected="$emit('selected', configuration)"
          v-on:deleted="$emit('deleted')"
        />
      </div>
    </div>
  </div>
</template>

<script>
import WidgetConf from "./WidgetConf";

export default {
  components: { WidgetConf },
  props: {
    configurations: { type: Array, required: true }, // [{ id, name, description, configuration, projectId, dataProviderId, creatinDate }]
    widgetKey: { type: String, required: true },
  },
  computed: {
    sameProjectConfigurations() {
      // TODO : update when fixed
      let projectIdWithDpId = this.$store.state.ProjectPage.projectId;
      const dataProviderId = projectIdWithDpId.split("|")[0];
      const projectId = projectIdWithDpId.split("|")[1];

      return this.configurations.filter(
        (conf) =>
          conf.projectId === projectId && conf.dataProviderId === dataProviderId
      );
    },

    sameDataProviderConfigurations() {
      // TODO : update when fixed
      let projectIdWithDpId = this.$store.state.ProjectPage.projectId;
      const dataProviderId = projectIdWithDpId.split("|")[0];
      const projectId = projectIdWithDpId.split("|")[1];

      return this.configurations.filter(
        (conf) =>
          conf.dataProviderId === dataProviderId && conf.projectId !== projectId
      );
    },

    otherConfigurations() {
      // TODO : update when fixed
      let projectIdWithDpId = this.$store.state.ProjectPage.projectId;
      const dataProviderId = projectIdWithDpId.split("|")[0];
      const projectId = projectIdWithDpId.split("|")[1];

      return this.configurations.filter(
        (conf) =>
          conf.projectId !== projectId && conf.dataProviderId !== dataProviderId
      );
    },
  },
};
</script>

<style scoped>
.configurationType {
  padding: 5px 0 5px 20px;
  opacity: 0.7;
  text-align: left;
}
</style>
