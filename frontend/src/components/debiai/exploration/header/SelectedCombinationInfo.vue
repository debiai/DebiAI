<template>
  <div id="SelectedDataInfo">
    <!-- <div>Selected samples :</div> -->
    <transition name="fade">
      <div
        v-if="nbCombination"
        id="selectedSamples"
        :title="'Selected samples: ' + (nbSelectedData / nbCombination) * 100 + '%'"
      >
        <div id="nbSelected">{{ nbSelectedData }} / {{ nbCombination }}</div>
        <div id="selectedBar">
          <div
            id="selectedBarValue"
            :style="'width:' + (nbSelectedData / nbCombination) * 100 + '%'"
          ></div>
        </div>
        <!-- <div id="percentSelect">
        ({{ Math.round((nbSelectedData / nbCombination) * 10000) / 100 }} %)
      </div> -->
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    nbCombination: { type: Number, required: true },
    nbSelectedData: { type: Number, required: true },
  },
};
</script>

<style lang="scss" scoped>
#SelectedDataInfo {
  display: flex;
  align-items: center;
  height: 100%;

  #selectedSamples {
    display: flex;
    align-items: center;
    flex-direction: column-reverse;
    gap: 3px;
    margin: 2px;
    padding: 2px;
    padding-top: 22px;
    // border-radius: 5px;

    #nbSelected {
      // margin: 0px 5px;
      font-size: 0.95em;
    }

    #percentSelect {
      color: grey;
    }

    #selectedBar {
      height: 5px;
      width: 8vw;
      margin-bottom: 2px;
      padding: 1px;
      border: solid grey 2px;
      // border-radius: 5px;

      #selectedBarValue {
        height: 5px;
        background: grey;
        transition: width 0.2s ease;
        // border-radius: 5px;
      }
    }
  }
}
</style>
