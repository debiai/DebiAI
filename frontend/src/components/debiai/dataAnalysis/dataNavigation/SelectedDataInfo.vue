<template>
  <div id="SelectedDataInfo">
    <div>Selected samples :</div>
    <div
      id="selectedSamples"
      :title="(selectedData.length / data.nbLines) * 100 + '%'"
    >
      <div id="nbSelected">{{ selectedData.length }} / {{ data.nbLines }}</div>
      <div id="selectedBar">
        <div
          id="selectedBarValue"
          :style="'width:' + (selectedData.length / data.nbLines) * 100 + '%'"
        ></div>
      </div>
      <div id="percentSelect">
        {{ Math.round((selectedData.length / data.nbLines) * 10000) / 100 }} %
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
};
</script>

<style scoped>
#SelectedDataInfo {
  display: flex;
  align-items: center;
  height: 100%;
}
#selectedSamples {
  display: flex;
  align-items: center;
  margin: 2px;
  padding: 2px;

  border-radius: 5px;
}

#nbSelected {
  margin: 0px 5px;
}
#percentSelect {
  width: 70px;
}

#selectedBar {
  height: 13px;
  width: 10vw;
  margin: 0px 15px;
  margin-bottom: 2px;
  padding: 1px;

  border: solid black 1px;
  border-radius: 5px;
}
#selectedBarValue {
  height: 13px;

  background: black;
  transition: width 0.2s ease;
  border-radius: 5px;
}
</style>
