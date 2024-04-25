<template>
  <div id="models">
    <div id="modelsPanel">
      <div id="title">
        <h2>
          <inline-svg
            :src="require('../../../assets/svg/gear.svg')"
            width="25"
            height="25"
            style="margin-right: 10px"
          />
          Models
        </h2>

        <span style="display: flex; align-items: center">
          <button @click="selectAll">All</button>
          <button
            style="margin-right: 5px"
            @click="selectNone"
          >
            None
          </button>
          <input
            type="text"
            placeholder="Search a model"
            class="search"
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
            <!-- Model name -->
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
          <!-- Model Metadata -->
          <DocumentationBlock v-if="model.metadata && Object.keys(model.metadata).length > 0">
            <h4>Model Metadata</h4>
            <br />
            <div style="white-space: pre-wrap">
              <span v-html="$services.prettifyJSON(model.metadata)"></span>
            </div>
          </DocumentationBlock>

          <!-- sample number -->
          <div
            class="sampleNumber"
            title="Number of samples for which we have model results "
          >
            <inline-svg
              :src="require('../../../assets/svg/data.svg')"
              width="20"
              height="20"
            />{{ "nbResults" in model && model.nbResults !== null ? model.nbResults : "?" }}
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
        class="card"
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
                id="commonModelResultsToggle"
                class="customCbx"
                style="display: none"
                v-model="commonModelResults"
              />
              <label
                for="commonModelResultsToggle"
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
    project: { type: Object, required: true },
    nbEvaluatedSamples: { type: Number },
    nbResults: { type: Number },
    nbSelectedSamples: { type: Number },
  },
  data: () => {
    return {
      searchBar: "",
      selectedModelIds: [],
      commonModelResults: true,
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
    selectNone() {
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
    commonModelResults() {
      this.$emit("setCommonModelResults", this.commonModelResults);
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

#modelsPanel {
  flex: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
  background-color: white;
  margin: 5px;
  background-color: white;
  border: solid 1px var(--greyDark);
  transition: height 0.2s;
  height: 0%;
  /* Do not remove, very important for some reason */
}

#title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px;
  font-size: 1.4em;
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
  gap: 10px;
}

/* modelsControls */
#modelsControls {
  margin: 5px;
  padding: 0 5px 0 5px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  font-size: 0.9em;
}

#modelsControls .dataGroup {
  padding: 5px 6px 5px 6px;
  margin-left: 10px;
  align-items: center;
  justify-content: space-evenly;
  font-weight: bold;
  color: var(--fontColor);
}

#modelsControls #commonModelResults {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
}

#modelsControls #nbEvaluatedSamples {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 40px;
  padding-left: 20px;
}

#modelsControls #commonModelResults label {
  margin: 0 10px 0 10px;
}
</style>
