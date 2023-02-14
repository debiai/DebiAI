<template>
  <div
    class="configuration item selectable"
    @click="$emit('selected')"
  >
    <div class="header">
      <h4 style="display: flex; align-items: center">
        {{ configuration.name }}
        <!-- Display conf details and project: -->
        <DocumentationBlock :followCursor="true">
          <h4>Configuration details</h4>
          <table class="confDetails">
            <tr
              v-for="key in Object.keys(configuration.configuration)"
              :key="key"
            >
              <th class="key">{{ key }}</th>
              <th class="value">{{ configuration.configuration[key] }}</th>
            </tr>
          </table>

          <b>Created with project: </b>
          <span class="confProject">
            <br />
            {{ configuration.projectId }}
            <br />
            {{ configuration.dataProviderId }}
          </span>
        </DocumentationBlock>
      </h4>

      <button
        class="red"
        @click="deleteConf"
      >
        Delete
      </button>
    </div>
    <div class="body">
      <span
        class="creationDate"
        :title="$services.timeStampToDate(configuration.creationDate)"
      >
        Created {{ $services.prettyTimeStamp(configuration.creationDate) }}
      </span>
      <div class="description">{{ configuration.description }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    configuration: { type: Object, required: true }, // { id, name, description, configuration, projectId, dataProviderId, creatinDate }
    widgetKey: { type: String, required: true },
  },
  methods: {
    deleteConf(event) {
      this.$backendDialog
        .deleteWidgetConfiguration(this.widgetKey, this.configuration.id)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Configuration deleted",
          });
          this.$emit("deleted");
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the configuration",
          });
        });

      event.stopPropagation();
    },
  },
};
</script>

<style scoped>
.configuration {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.configuration .header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.configuration .body {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}
.configuration .creationDate {
  text-align: right;
  font-size: 0.7em;
  opacity: 0.7;
}
.configuration .description {
  flex: 1;
  text-align: left;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-width: 300px;
  opacity: 0.7;
  font-size: 0.8em;
}
.configuration .confDetails {
  border-spacing: 0px;
  align-self: flex-start;
  padding: 10px;
}
.configuration .confProject {
  font-weight: lighter;
  font-size: 0.8em;
}
.configuration .confDetails th {
  opacity: 0.8;
  font-weight: lighter;
  padding-right: 10px;
}
.configuration .key {
  text-align: right;
}
.configuration .value {
  text-align: left;
}
</style>
