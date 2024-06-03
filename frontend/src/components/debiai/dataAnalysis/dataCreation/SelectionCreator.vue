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
          <div class="data">
            <div class="name">Selected samples</div>
            <div class="value">{{ selectedData.length }} / {{ data.nbLines }}</div>
          </div>
          <!-- saveRequestAsWell -->
          <!-- TODO : Revert for the requests update -->
          <!-- <div class="data">
          <div class="name">Save the request as well</div>
          <div class="value">
            No
            <input
              type="checkbox"
              id="selectionSaveRequest"
              class="customCbx"
              style="display: none"
              v-model="saveRequestAsWell"
            />
            <label for="selectionSaveRequest" class="toggle">
              <span></span>
            </label>
            Yes
          </div>
        </div> -->
          <!-- nb filters:  -->
          <!-- <div :class="saveRequestAsWell ? 'data ' : 'data date'">
          <div class="name">Number of filters</div>
          <div class="value">
            {{ filters.length }}
          </div>
        </div> -->
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
      saveRequestAsWell: false,
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
      if (this.saveRequestAsWell) {
        this.saveRequest();
      } else {
        this.saveSelection();
      }
    },

    saveRequest() {
      // Save the request first
      this.$backendDialog
        .addRequest(this.selectionName, "", this.filters)
        .then((request) => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Request saved successfully",
          });
          this.saveSelection(request.id);
        })
        .catch(() => {
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't save the request",
          });
        });
    },

    saveSelection(requestId = null) {
      let selectedIds = this.data.selectedData.map(
        (selectedIndex) => this.data.sampleIdList[selectedIndex]
      );
      this.$backendDialog
        .addSelection(selectedIds, this.selectionName, requestId)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection saved successfully",
          });
          this.$emit("cancel");

          // this.$backendDialog.getSelections().then((selections) => {
          //   this.createdSelections = selections;
          //   this.$store.commit("setProjectSelections", selections);
          // });
        })
        .catch(() => {
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't save the selection",
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
