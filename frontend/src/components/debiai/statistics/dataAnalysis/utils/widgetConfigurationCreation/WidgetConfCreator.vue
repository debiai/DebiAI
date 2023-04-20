<template>
  <form
    v-on:submit.prevent
    id="confCreator"
  >
    <!-- title -->
    <h4>
      Save a
      <u>{{ widgetTitle }}</u>
      configuration
    </h4>

    <!-- form -->
    <div class="dataGroup">
      <!-- Name -->
      <div class="data">
        <div class="name">Name</div>
        <div class="value">
          <textarea
            id="confNameArea"
            type="text"
            v-model="confName"
            style="flex: 2"
            placeholder="Configuration name"
          />
          <!-- <select v-model="confName">
            <option v-for="configuration in createdConf" :key="configuration.id">
              {{ configuration.name }}
            </option>
          </select> -->
          <button
            title="Reset the configuration name to the one suggested by the widget"
            @click="confName = suggestedConfName"
            v-if="confName !== suggestedConfName"
          >
            <inline-svg
              :src="require('@/assets/svg/update.svg')"
              width="10"
              height="10"
              fill="white"
              style="transform: scale(1.2)"
            />
          </button>
        </div>
      </div>

      <!-- Description -->
      <div class="data">
        <div class="name">Description</div>
        <div class="value">
          <textarea
            id="story"
            name="story"
            rows="3"
            cols="15"
            v-model="confDescription"
            placeholder="Widget configuration description"
          />
        </div>
      </div>

      <!-- widget configuration -->
      <div
        class="data"
        id="widgetConf"
      >
        <div class="name">Configuration</div>
        <div class="value">
          <table id="keyList">
            <tr
              v-for="key in Object.keys(widgetConf)"
              :key="key"
            >
              <td class="key">{{ key }}</td>
              <td class="val">{{ widgetConf[key] }}</td>
            </tr>
          </table>
        </div>
      </div>
      <!-- Controls -->
      <div id="controls">
        <!-- <button
          v-if="confNameAlreadyExists"
          class="warning"
          type="submit"
          @click="save"
          :disabled="!confName"
        >
          <inline-svg
            :src="require('../../../../../../assets/svg/save.svg')"
            width="10"
            height="10"
            fill="black"
          />
          Update the configuration
        </button> -->
        <button
          type="submit"
          @click="save"
          :disabled="!confName"
        >
          <inline-svg
            :src="require('../../../../../../assets/svg/save.svg')"
            width="10"
            height="10"
            fill="white"
          />
          Save the configuration
        </button>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  name: "ConfCreator",
  data() {
    return {
      confName: "",
      confDescription: "",
    };
  },
  props: {
    widgetConf: { type: Object, required: true },
    widgetTitle: { type: String, required: true },
    widgetKey: { type: String, required: true },
    // createdConf: { type: Array, required: true },
    suggestedConfName: { type: String, default: "" },
  },
  mounted() {
    this.confName = this.suggestedConfName;
  },
  methods: {
    save() {
      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      const projectId = this.$store.state.ProjectPage.projectId;

      this.$backendDialog
        .saveWidgetConfiguration(this.widgetKey, {
          projectId: projectId,
          dataProviderId: dataProviderId,
          configuration: this.widgetConf,
          name: this.confName,
          description: this.confDescription,
        })
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Widget configuration saved",
          });
          this.$emit("saved", this.confName);
        })
        .catch((e) => {
          if (e.response && e.response.data?.detail) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: e.response.data.detail,
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Couldn't save the widget configuration",
            });
          }
        });
    },
  },
  computed: {
    // confNameAlreadyExists() {
    //   const confWithSameName = this.createdConf.find(
    //     (configuration) => configuration.name === this.confName
    //   );
    //   return confWithSameName !== undefined;
    // },
  },
};
</script>

<style scoped>
#confCreator {
  text-align: left;
  display: flex;
}
#confCreator .dataGroup {
  flex: 1;
  margin: 20px;
  padding: 10px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#confCreator .dataGroup .data + .data {
  padding-top: 5px;
}

#widgetConf #keyList .key {
  text-align: right;
  font-size: 0.6em;
  padding: 0 5px 0 5px;
}
#widgetConf #keyList .val {
  text-align: left;
  font-size: 0.6em;
}
#controls {
  padding: 5px;
}
#confNameArea {
}
</style>
