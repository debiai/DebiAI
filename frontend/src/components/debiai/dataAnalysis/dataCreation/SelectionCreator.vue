<template>
  <modal
    @close="$emit('cancel')"
    :errorMessages="[selectionNameNull ? 'The selection name can\'t be empty' : '']"
    :warningMessages="[selectionExists ? 'A selection with this name already exists' : '']"
  >
    <div id="SelectionCreator">
      <!-- Title -->
      <b class="aligned centered">
        <h3
          style="padding-right: 40px"
          class="aligned centered"
          v-if="data.mode === 'exploration'"
        >
          Create a new selection from the combinations
          <documentation-block>
            A selection is a named list of samples ID. <br />
            <br />
            By creating a selection, you can extract, from the currently selected combinations, the
            samples they contain and analyze them afterward.
            <br />
          </documentation-block>
        </h3>

        <h3
          style="padding-right: 40px"
          class="aligned centered"
          v-else
        >
          Create a new selection from the selected data
          <documentation-block>
            A selection is a named list of samples ID. <br />
            <br />
            By creating a selection, you can save the currently selected samples <br />
            and open them later.
            <br />
          </documentation-block>
        </h3>
        <button
          @click="$emit('cancel')"
          class="red"
        >
          Cancel
        </button>
      </b>

      <!-- Form -->
      <form v-on:submit.prevent>
        <div class="dataGroup">
          <!-- selection name -->
          <div class="data">
            <div class="name">Selection name</div>
            <div class="value">
              <input
                type="text"
                v-model="selectionName"
                style="flex: 1"
              />
            </div>
          </div>
          <!-- nb samples -->
          <div
            class="data"
            v-if="data.mode === 'exploration'"
          >
            <div class="name">Selected samples</div>
            <div class="value">
              {{ data.nbExplorationSelectedSamples }} / {{ data.projectNbSamples }}
            </div>
          </div>
          <div
            class="data"
            v-else
          >
            <div class="name">Selected samples</div>
            <div class="value">{{ data.nbOriginalSelectedData }} / {{ data.nbLinesOriginal }}</div>
          </div>
        </div>
        <div style="display: flex; justify-content: flex-end">
          <button
            type="submit"
            @click="save"
            :disabled="!selectionNameOk"
          >
            Create
          </button>
        </div>
      </form>
    </div>
  </modal>
</template>

<script>
export default {
  name: "SelectionCreator",
  data() {
    return {
      selectionName: "New selection",
      createdSelections: null,
    };
  },
  props: {
    data: { type: Object, required: true },
  },
  created() {
    this.$backendDialog.getSelections().then((selections) => {
      this.createdSelections = selections;
      // this.$store.commit("setProjectSelections", selections);
    });
  },
  methods: {
    save() {
      if (this.data.mode === "exploration") {
        this.saveExplorationSelection();
      } else {
        this.saveSelection();
      }
    },

    saveSelection() {
      // Get the selected data positions
      const selectedDataNumbers = this.data.getOriginalSelectedData();

      // Get the ids of the selected data
      const selectedIds = selectedDataNumbers.map(
        (selectedIndex) => this.data.sampleIdList[selectedIndex]
      );

      // Save the selection
      this.$backendDialog
        .addSelection(selectedIds, this.selectionName)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection saved successfully",
          });
          this.$emit("cancel");
        })
        .catch(() => {
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't save the selection",
          });
        });
    },

    saveExplorationSelection() {
      // Get the ids of the selected combinations
      const selectedCombinationsIds = this.data.getSelectedCombinations();

      // Save the selection from the exploration data
      this.$explorationDialog
        .createSelection(
          this.$store.state.ProjectPage.projectId,
          this.data.explorationId,
          selectedCombinationsIds,
          this.selectionName
        )
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection created successfully",
          });
          this.$emit("cancel");
        })
        .catch(() => {
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't create the selection",
          });
        });
    },
  },
  computed: {
    selectionNameNull() {
      return this.selectionName === null || this.selectionName === "";
    },
    selectionExists() {
      if (this.createdSelections === null) return false;

      const selectionNames = this.createdSelections.map((s) => s.name);
      return selectionNames.includes(this.selectionName);
    },
    selectionNameOk() {
      return !this.selectionNameNull; // && !this.selectionExists;
    },
    filters() {
      return this.$store.state.StatisticalAnalysis.filters.map((f) => {
        f.columnLabel = f.column.label;
        return f;
      });
    },
  },
};
</script>

<style scoped>
.errorMsg {
  color: red;
}

form {
  display: flex;
  flex-direction: column;
}

.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 4px;
}
.dataGroup .value {
  flex: 1;
}
</style>
