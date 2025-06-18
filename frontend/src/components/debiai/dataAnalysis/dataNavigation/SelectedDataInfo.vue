<template>
  <div id="SelectedDataInfo">
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

    <!-- Exploration selected samples -->
    <div
      id="explorationsSelectedSamples"
      class="selectedSamples"
      v-if="data.mode === 'exploration'"
    >
      <div id="sampleText">
        <inline-svg
          :src="require('@/assets/svg/data.svg')"
          width="10"
          height="10"
        />
        Selected samples
      </div>
      <div id="selectedBar">
        <div
          id="selectedBarValue"
          :style="
            'width:' + (data.nbExplorationSelectedSamples / data.projectNbSamples) * 100 + '%'
          "
        ></div>
      </div>
      <div id="bottom">
        <div id="nbSelected">
          {{ data.nbExplorationSelectedSamples }} / {{ data.projectNbSamples }}
        </div>
        <div id="percentSelect">
          {{
            Math.round((data.nbExplorationSelectedSamples / data.projectNbSamples) * 10000) / 100
          }}
          %
        </div>
      </div>
    </div>

    <!-- Original selected samples -->
    <div
      id="originalSelectedSamples"
      class="selectedSamples"
    >
      <div
        id="sampleText"
        v-if="data.mode !== 'exploration'"
      >
        <inline-svg
          :src="require('@/assets/svg/data.svg')"
          width="10"
          height="10"
        />
        Selected samples
      </div>
      <div
        id="sampleText"
        v-else
      >
        <inline-svg
          :src="require('@/assets/svg/realCombinations.svg')"
          width="10"
          height="10"
        />
        Selected combinations
      </div>
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
  flex-direction: row;
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
    #sampleText {
      color: var(--fontColorLight);
      font-size: 0.8em;
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
    fill: var(--success);

    #percentSelect {
      color: var(--success) !important;
    }
    #selectedBar {
      border-color: var(--success);
    }
    #selectedBarValue {
      background: var(--success) !important;
    }
    #sampleText {
      color: var(--success) !important;
    }
  }
}
</style>
