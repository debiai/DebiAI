<template>
  <div id="models">
    <div id="modelsPannel">
      <div id="title">
        <h2>
          <inline-svg
            :src="require('../../../assets/svg/gear.svg')"
            width="20"
            height="20"
          />
          Models
        </h2>
        <span style="display: flex; align-items: center">
          <button
            class="info"
            @click="selectAll"
          >
            All
          </button>
          <button
            class="warning"
            style="margin-right: 5px"
            @click="selecNone"
          >
            None
          </button>
          <input
            type="text"
            placeholder="Search a model"
            v-model="searchBar"
          />
        </span>
      </div>

      <div
        id="modelList"
        class="itemList"
        v-if="project.models.length > 0"
      >
        <div
          v-for="model in filteredModels"
          :key="model.id"
          :class="
            'model item selectable ' + (selectedModelIds.includes(model.id) ? 'selected' : '')
          "
          @click="selectModel(model.id)"
        >
          <div class="title">
            <h3 class="name">{{ model.name }}</h3>
            <!-- date -->
            <span
              class="date"
              :title="$services.timeStampToDate(model.creationDate)"
              v-if="model.creationDate"
            >
              Created {{ $services.prettyTimeStamp(model.creationDate) }}
            </span>
            <span
              v-else
              class="date"
            >
              No creation date
            </span>
          </div>

          <!-- sample number -->
          <div
            class="sampleNumber"
            title="Number of samples for which we have model results "
          >
            <inline-svg
              :src="require('../../../assets/svg/data.svg')"
              width="20"
              height="20"
            />{{ "nbResults" in model ? (model.nbResults === null ? "?" : model.nbResults) : "?" }}
          </div>

          <!-- options -->
          <button
            class="red"
            @click="(event) => deleteModel(model.id, event)"
            v-if="
              $store.state.ProjectPage.dataProviderInfo &&
              $store.state.ProjectPage.dataProviderInfo.canDelete &&
              $store.state.ProjectPage.dataProviderInfo.canDelete.models
            "
          >
            Delete
          </button>
        </div>
      </div>
      <div
        id="Model"
        v-else
        style="text-align: center; padding-top: 20px"
      >
        No models
      </div>
    </div>
    <!-- Controls -->
    <transition name="fade">
      <div
        id="modelsControls"
        v-if="selectedModelIds.length > 0"
      >
        <!-- Common results -->
        <transition name="fade">
          <div
            id="commonModelResults"
            v-if="selectedModelIds.length > 1"
          >
            Multiple model results selected :
            <div class="dataGroup">
              Union
              <input
                type="checkbox"
                id="commomModelResultsToggle"
                class="customCbx"
                style="display: none"
                v-model="commomModelResults"
              />
              <label
                for="commomModelResultsToggle"
                class="toggle"
              >
                <span></span>
              </label>
              Intersection
            </div>
          </div>
        </transition>

        <!-- nb evaluated and results -->
        <div id="nbEvaluatedSamples">
          Evaluated samples :
          <div
            class="dataGroup"
            v-if="selectedModelIds.length"
          >
            <!-- Nb evaluated samples -->
            <span style="padding-right: 5px">
              {{ nbEvaluatedSamples }}
            </span>
            <inline-svg
              :src="require('../../../assets/svg/data.svg')"
              width="20"
              height="20"
              fill="white"
            />
            <span
              v-if="nbSelectedSamples"
              style="padding-left: 5px"
              :title="(nbEvaluatedSamples * 100) / nbSelectedSamples + '%'"
            >
              ({{ Math.ceil((nbEvaluatedSamples * 100) / nbSelectedSamples) }}%)
            </span>
          </div>
          Number of results :
          <div class="dataGroup">
            {{ nbResults === null ? "?" : nbResults }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    project: { type: Object },
    nbEvaluatedSamples: { type: Number },
    nbResults: { type: Number },
    nbSelectedSamples: { type: Number },
  },
  data: () => {
    return {
      searchBar: "",
      selectedModelIds: [],
      commomModelResults: true,
    };
  },
  mounted() {},
  methods: {
    selectModel(modelId) {
      if (this.selectedModelIds.includes(modelId))
        this.selectedModelIds = this.selectedModelIds.filter((mId) => mId !== modelId);
      else this.selectedModelIds.push(modelId);

      this.$emit("modelSelected", this.selectedModelIds);
    },
    selectAll() {
      this.selectedModelIds = this.project.models.map((m) => m.id);
      this.$emit("modelSelected", this.selectedModelIds);
    },
    selecNone() {
      this.selectedModelIds = [];
      this.$emit("modelSelected", this.selectedModelIds);
    },
    deleteModel(modelId, event) {
      this.$backendDialog
        .delModel(modelId)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Model deleted",
          });

          // Remove the model from the selected models
          this.selectedModelIds = this.selectedModelIds.filter((mId) => mId !== modelId);
          this.$emit("modelSelected", this.selectedModelIds);
          this.$emit("modelDeleted", modelId);
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the model",
          });
        });
      event.stopPropagation();
    },
  },
  computed: {
    filteredModels() {
      if (this.project === null) return [];
      if (this.searchBar === "") return this.project.models;
      return this.project.models.filter((m) =>
        m.name.toLowerCase().includes(this.searchBar.toLowerCase())
      );
    },
  },
  watch: {
    commomModelResults() {
      this.$emit("setCommomModelResults", this.commomModelResults);
    },
  },
};
</script>

<style scoped>
#models {
  flex: 1;
  display: flex;
  flex-direction: column;
}

#modelsPannel {
  flex: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.2);
  background-color: white;
  border-radius: 10px;
  margin: 5px;
  transition: height 0.2s;
  height: 0%;
  /* Do not remove, very important for some reason */
}

#title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#modelList {
  flex: 1;
  overflow-y: auto;
}

/* Model  */

.model .title {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.model .date {
  opacity: 0.7;
}

.model .sampleNumber {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* modelsControls */
#modelsControls {
  display: flex;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.2);
  background-color: white;
  border-radius: 10px;
  margin: 5px;
  padding: 0 5px 0 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9em;
}

#modelsControls .dataGroup {
  padding: 5px 6px 5px 6px;
  margin-left: 10px;
  align-items: center;
  justify-content: space-evenly;
  font-weight: bold;
  background: #707070;
}

#modelsControls #commonModelResults {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

#modelsControls #nbEvaluatedSamples {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
}

#modelsControls #commonModelResults label {
  margin: 0 10px 0 10px;
}
</style>
