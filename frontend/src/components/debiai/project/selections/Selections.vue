<template>
  <div id="selections">
    <div id="selectionsPanel">
      <!-- Panel header -->
      <div id="title">
        <span class="aligned gapped">
          <h2>
            <inline-svg
              :src="require('@/assets/svg/loop.svg')"
              width="25"
              height="25"
              style="margin-right: 10px"
            />
            Selections
          </h2>
          <!-- TODO: Add path to Documentation -->
          <DocumentationBlock>
            A <b> selection </b> is a list of samples, it can be created from the analysis
            dashboard.
            <br />
            Selections are used to start analysis on a specific subset of the data project, they can
            be extracted by the DebiAI python library.
          </DocumentationBlock>
        </span>

        <span class="aligned">
          <button @click="selectAll">All</button>
          <button
            style="margin-right: 5px"
            @click="selectNone"
          >
            None
          </button>
          <input
            class="search"
            type="text"
            placeholder="Search a selection"
            v-model="searchBar"
          />
        </span>
      </div>

      <!-- All selections -->
      <div
        id="selectionList"
        class="itemList"
      >
        <div
          id="allData"
          :class="
            'selection item selectable ' + (selectedSelectionIds.length == 0 ? 'selected' : '')
          "
          @click="selectNone"
        >
          <div class="title">
            <h3 class="name">All data</h3>
          </div>
          <div
            class="sampleNumber"
            title="Selection sample number"
          >
            <inline-svg
              :src="require('@/assets/svg/data.svg')"
              height="25"
            />{{ project.metrics.nbSamples !== null ? project.metrics.nbSamples : "?" }}
          </div>
        </div>

        <!-- Other selections -->
        <Selection
          v-for="selection in filteredSelections"
          :key="selection.id"
          :class="
            'item selectable ' + (selectedSelectionIds.includes(selection.id) ? 'selected' : '')
          "
          :selection="selection"
          @selected="selectSelection(selection.id)"
          @delete="deleteSelection(selection.id)"
          @selectRequest="selectRequest"
        />
        <!-- No selections msg -->
        <div
          v-if="project.selections.length == 0"
          style="text-align: center; padding-top: 20px"
        >
          No selections
        </div>
      </div>
    </div>

    <!-- setSelection Intersection and nb selected-->
    <transition name="fade">
      <div
        class="card"
        id="analysisControls"
      >
        <!-- selection Intersection -->
        <transition name="fade">
          <div
            id="selectionIntersection"
            v-if="selectedSelectionIds.length > 1"
          >
            Multiple selection selected :
            <div
              class="dataGroup"
              style="margin-right: 40px"
            >
              Union
              <input
                type="checkbox"
                id="selectionIntersectionToggle"
                class="customCbx"
                style="display: none"
                v-model="selectionIntersection"
              />
              <label
                for="selectionIntersectionToggle"
                class="toggle"
              >
                <span></span>
              </label>
              Intersection
            </div>
          </div>
        </transition>
        <!-- Nb samples -->
        <div id="nbSelectedSamples">
          <span style="padding: 0px 5px">
            {{ nbSelectedSamples }}
          </span>
          <inline-svg
            :src="require('@/assets/svg/data.svg')"
            width="20"
            height="20"
          />
          <span
            v-if="project.nbSamples"
            style="padding: 0 5px 0 2px; font-weight: normal"
            :title="(nbSelectedSamples * 100) / project.nbSamples + '%'"
          >
            ({{ Math.ceil((nbSelectedSamples * 100) / project.nbSamples) }}%)
          </span>
          Selected samples
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import Selection from "./Selection";
// import Requests from "../requests/Requests";
// import Request from "../requests/Request";

export default {
  components: {
    Selection,
    //  Requests,
    //  Request
  },
  props: {
    project: { type: Object, required: true },
    nbSelectedSamples: { type: Number, default: 0 },
  },
  data: () => {
    return {
      searchBar: "",
      selectedSelectionIds: [],
      selectionIntersection: true,

      // Selection creation
      selectionCreation: false,

      // Requests
      selectedRequestId: null,
    };
  },
  mounted() {},
  methods: {
    selectSelection(selectionId) {
      if (this.selectedSelectionIds.includes(selectionId))
        this.selectedSelectionIds = this.selectedSelectionIds.filter((mId) => mId !== selectionId);
      else this.selectedSelectionIds.push(selectionId);

      this.$emit("selectionSelected", this.selectedSelectionIds);
    },
    selectAll() {
      this.selectedSelectionIds = this.project.selections.map((s) => s.id);
      this.$emit("selectionSelected", this.selectedSelectionIds);
    },
    selectNone() {
      this.selectedSelectionIds = [];
      this.$emit("selectionSelected", this.selectedSelectionIds);
    },
    deleteSelection(selectionId) {
      this.$backendDialog
        .delSelection(selectionId)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection deleted",
          });

          this.selectedSelectionIds = this.selectedSelectionIds.filter(
            (sId) => sId !== selectionId
          );
          this.$emit("selectionSelected", this.selectedSelectionIds);
          this.$emit("selectionDeleted", selectionId);
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the selection",
          });
        });
    },
    selectRequest(requestId) {
      this.selectedRequestId = requestId;
    },
  },
  computed: {
    filteredSelections() {
      if (!this.project || !this.project.selections) return [];
      if (this.searchBar === "") return this.project.selections;
      return this.project.selections.filter((s) =>
        s.name.toLowerCase().includes(this.searchBar.toLowerCase())
      );
    },
  },
  watch: {
    selectionIntersection() {
      this.$emit("setSelectionIntersection", this.selectionIntersection);
    },
  },
};
</script>

<style scoped>
#selections {
  flex: 1;
  display: flex;
  flex-direction: column;
}
#selectionsPanel {
  flex: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
  background-color: white;
  border: solid 1px var(--greyDark);
  margin: 5px;
  transition: height 0.2s;
  height: 0%; /* Do not remove, very important for some reason */
}

#title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px;
  font-size: 1.4em;
}

#selectionList {
  flex: 1;
  overflow-y: auto;
}

#allData {
  padding: 24px 33px;
}
#allData .title {
  min-width: 78%;
}

#allData .sampleNumber {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* analysisControls */
#analysisControls {
  margin: 5px;
  padding: 0 5px 0 5px;
  flex-direction: row;
}

#analysisControls .dataGroup {
  padding: 5px 10px 5px 10px;
  margin-left: 10px;
  align-items: center;
  justify-content: space-evenly;
  font-weight: bold;
  color: var(--fontColor);
}

#analysisControls #nbSelectedSamples {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: flex-end;
  height: 40px;
}
#analysisControls #selectionIntersection {
  display: flex;
  flex: 2;
  align-items: center;
  justify-content: flex-end;
}
#analysisControls #selectionIntersection label {
  margin: 0 10px 0 10px;
}
</style>
