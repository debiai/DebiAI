<template>
  <div
    class="configuration item selectable"
    @click="$emit('selected')"
  >
    <div class="header">
      <!-- Configuration name -->
      <h4 style="display: flex; align-items: center">
        {{ configuration.name }}
      </h4>

      <div class="right">
        <!-- Configuration details -->
        <DocumentationBlock>
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

        <!-- Delete btn -->
        <button
          class="red"
          @click="deleteConf"
        >
          Delete
        </button>
      </div>
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
    configuration: { type: Object, required: true }, // { id, name, description, configuration, projectId, dataProviderId, creationDate }
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

<style lang="scss" scoped>
.configuration {
  display: flex;
  flex-direction: column;
  align-items: stretch;

  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    .right {
      display: flex;
      align-items: center;
    }
  }

  .body {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    .creationDate {
      text-align: right;
      font-size: 0.7em;
      opacity: 0.7;
    }
    .description {
      flex: 1;
      text-align: left;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      max-width: 300px;
      color: var(--fontColorLight);
    }
    .confDetails {
      border-spacing: 0px;
      align-self: flex-start;
      padding: 10px;
      .confProject {
        font-weight: lighter;
        font-size: 0.8em;
      }
      .confDetails th {
        opacity: 0.8;
        font-weight: lighter;
        padding-right: 10px;
      }
      .key {
        text-align: right;
      }
      .value {
        text-align: left;
      }
    }
  }
}
</style>
