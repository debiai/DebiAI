<template>
  <div id="SelectedDataInfo">
    <!-- <div>Selected samples :</div> -->
    <div
      id="selectedSamples"
      :title="'Selected samples: ' + (data.selectedData.length / data.nbLines) * 100 + '%'"
    >
      <div id="selectedBar">
        <div
          id="selectedBarValue"
          :style="'width:' + (data.selectedData.length / data.nbLines) * 100 + '%'"
        ></div>
      </div>
      <div id="bottom">
        <div id="nbSelected">{{ data.selectedData.length }} / {{ data.nbLines }}</div>
        <div id="percentSelect">
          {{ Math.round((data.selectedData.length / data.nbLines) * 10000) / 100 }} %
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
    flex-direction: column;
    gap: 3px;
    margin: 2px;
    padding: 2px;
    padding-top: 22px;
    // border-radius: 5px;

    #bottom {
      display: flex;
      align-items: center;
      gap: 5px;
      #nbSelected {
        // margin: 0px 5px;
        font-size: 0.95em;
        display: inline-block;
        vertical-align: middle;
      }
      #percentSelect {
        color: grey;
        font-size: 0.6em;
        display: inline-block;
        vertical-align: middle;
      }
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
