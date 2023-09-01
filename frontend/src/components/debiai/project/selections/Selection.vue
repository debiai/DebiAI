<template>
  <div
    class="Selection"
    @click="$emit('selected')"
    @mousedown.middle="$emit('selectedNewTab')"
  >
    <div class="left">
      <!-- selectionName & request id  -->
      <div class="name">
        <h3>{{ selection.name || selection.id }}</h3>
        <!-- Request if it exist -->
        <a
          title="Request that has created this selection"
          v-if="displayRequest && selection.requestId !== undefined"
          @click="(event) => selectRequest(selection.requestId, event)"
        >
          {{ selection.requestId }}
        </a>
      </div>
      <!-- date -->
      <span
        class="date"
        :title="$services.timeStampToDate(selection.creationDate)"
        v-if="selection.creationDate"
      >
        Created {{ $services.prettyTimeStamp(selection.creationDate) }}
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
      title="Selection sample number"
    >
      <inline-svg
        :src="require('../../../../assets/svg/data.svg')"
        width="20"
        height="20"
      />{{ "nbSamples" in selection ? selection.nbSamples : "?" }}
    </div>

    <!-- options -->
    <button
      class="red"
      @click="(event) => deleteSelection(event)"
      v-if="
        $store.state.ProjectPage.dataProviderInfo &&
        $store.state.ProjectPage.dataProviderInfo.canDelete &&
        $store.state.ProjectPage.dataProviderInfo.canDelete.selections
      "
    >
      Delete
    </button>
  </div>
</template>

<script>
export default {
  props: {
    selection: { type: Object, required: true },
    displayRequest: { type: Boolean, default: true },
  },
  methods: {
    deleteSelection(event) {
      this.$emit("delete");
      event.stopPropagation();
    },
    selectRequest(requestId, event) {
      this.$emit("selectRequest", requestId);
      event.stopPropagation();
    },
  },
};
</script>

<style scoped>
.Selection .left {
  flex-direction: column;
  min-width: 70%;
}

.Selection .left .name {
  display: flex;
}

.Selection .left a {
  padding-left: 10px;
  color: var(--primary);
}

.Selection .left a:hover {
  text-decoration: underline;
  color: var(--primary);
}

.Selection .sampleNumber {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
</style>
