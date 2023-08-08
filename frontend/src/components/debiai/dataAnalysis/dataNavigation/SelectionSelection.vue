<template>
  <div id="SelectionSelection">
    <div id="selectionsPanel">
      <div id="title">
        <span class="aligned spaced">
          <h2>
            <inline-svg
              :src="require('@/assets/svg/loop.svg')"
              width="20"
              height="20"
            />
            Selections
          </h2>
          Start an analysis on another selection
          <button
            class="red"
            @click="$emit('cancel')"
          >
            Cancel
          </button>
        </span>
      </div>

      <!-- Selections -->
      <div
        id="selectionList"
        class="itemList"
      >
        <!-- All data -->
        <div
          id="allData"
          class="selection item selectable"
          @click="selectSelection()"
        >
          <div class="title">
            <h3 class="name">All data</h3>
          </div>
        </div>

        <!-- Other selections -->
        <Selection
          v-for="selection in selections"
          :key="selection.id"
          class="item selectable"
          :selection="selection"
          @selected="selectSelection(selection.id)"
          @selectedNewTab="selectSelectionNewTab(selection.id)"
          @delete="deleteSelection(selection.id)"
        />
        <!-- No selections msg -->
        <div
          v-if="selections.length == 0"
          style="text-align: center; padding-top: 20px"
        >
          No selections
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Selection from "../../project/selections/Selection.vue";

export default {
  components: { Selection },
  data() {
    return {
      selections: [],
    };
  },
  created() {
    this.$backendDialog.getSelections().then((selections) => {
      this.selections = selections;
    });
  },
  methods: {
    selectSelection(selectionId) {
      let dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      let projectId = this.$store.state.ProjectPage.projectId;

      this.$router.push({
        path: "/dataprovider/" + dataProviderId + "/project/" + projectId,
        query: {
          dataProviderId,
          projectId,
          selectionIds: selectionId,
          startAnalysis: true,
        },
      });
    },
    selectSelectionNewTab(selectionId) {
      let dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      let projectId = this.$store.state.ProjectPage.projectId;

      let routeData = this.$router.resolve({
        path: "/dataprovider/" + dataProviderId + "/project/" + projectId,
        query: {
          dataProviderId,
          projectId,
          selectionIds: selectionId,
          startAnalysis: true,
        },
      });
      window.open(routeData.href, "_blank");
    },
    deleteSelection(selectionId) {
      this.$backendDialog
        .delSelection(selectionId)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection deleted",
          });

          this.selections = this.selections.filter((s) => s.id !== selectionId);
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the selection",
          });
        });
    },
  },
};
</script>

<style scoped>
#SelectionSelection {
  height: 80vh;
  width: 35vw;
  color: black;
}
#selections {
  height: 100%;
}
</style>
