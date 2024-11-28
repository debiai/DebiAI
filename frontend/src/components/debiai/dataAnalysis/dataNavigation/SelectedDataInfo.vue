<template>
  <div id="SelectedDataInfo">
    <!-- Original selected samples -->
    <div
      id="originalSelectedSamples"
      class="selectedSamples"
      :title="'Selected samples: ' + (nbOriginalSelectedData / data.nbLinesOriginal) * 100 + '%'"
    >
      <div id="selectedBar">
        <div
          id="selectedBarValue"
          :style="'width:' + (nbOriginalSelectedData / data.nbLinesOriginal) * 100 + '%'"
        ></div>
      </div>
      <div id="bottom">
        <div id="nbSelected">{{ nbOriginalSelectedData }} / {{ data.nbLinesOriginal }}</div>
        <div id="percentSelect">
          {{ Math.round((nbOriginalSelectedData / data.nbLinesOriginal) * 10000) / 100 }} %
        </div>
      </div>
    </div>

    <!-- Unfolded selected samples -->
    <Transition name="fade">
      <div
        v-if="currentlyUnfoldedVertically"
        id="unfoldedSelectedSamples"
        class="selectedSamples"
        :title="'Selected unfolded samples: ' + (nbUnfoldedSelectedData / data.nbLines) * 100 + '%'"
      >
        <div id="selectedBar">
          <div
            id="selectedBarValue"
            :style="'width:' + (nbUnfoldedSelectedData / data.nbLines) * 100 + '%'"
          ></div>
        </div>
        <div id="bottom">
          <div id="nbSelected">{{ nbUnfoldedSelectedData }} / {{ data.nbLines }}</div>
          <div id="percentSelect">
            {{ Math.round((nbUnfoldedSelectedData / data.nbLines) * 10000) / 100 }} %
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
export default {
  props: {
    data: { type: Object, required: true },
  },
  computed: {
    currentlyUnfoldedVertically() {
      return this.data.currentlyUnfoldedVertically();
    },
    nbOriginalSelectedData() {
      return this.data.nbOriginalSelectedData;
    },
    nbUnfoldedSelectedData() {
      return this.data.selectedData.length;
    },
  },
};
</script>

<style lang="scss" scoped>
#SelectedDataInfo {
  display: flex;
  align-items: center;
  flex-direction: row-reverse;
  height: 100%;

  .selectedSamples {
    display: flex;
    align-items: center;
    flex-direction: column;
    gap: 3px;
    margin: 2px;
    padding: 2px;
    padding-top: 15px;

    #bottom {
      display: flex;
      align-items: center;
      gap: 5px;
      #nbSelected {
        font-size: 0.95em;
        display: inline-block;
        vertical-align: middle;
      }
      #percentSelect {
        color: var(--fontColorLight);
        font-size: 0.6em;
        display: inline-block;
        vertical-align: middle;
      }
    }

    #selectedBar {
      height: 5px;
      width: 7vw;
      margin-bottom: 2px;
      border: solid var(--fontColorLight) 2px;
      border-radius: 2px;

      #selectedBarValue {
        height: 5px;
        background: var(--fontColorLight);
        transition: width 0.2s ease;
      }
    }
  }

  #unfoldedSelectedSamples {
    color: var(--success);
    #percentSelect {
      color: var(--success) !important;
    }
    #selectedBar {
      border-color: var(--success);
    }
    #selectedBarValue {
      background: var(--success) !important;
    }
  }
}
</style>
