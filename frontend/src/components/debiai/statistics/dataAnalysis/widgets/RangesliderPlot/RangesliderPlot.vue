<template>
  <div id="RangesliderPlot" class="dataVisualisationWidget">

    <div :id="'rangesliderPlot_' + this.index" />

  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

export default {
  components: {
  },
  data() {
    return {
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  mounted() {
    const trace1 = {
      type: "scatter",
      mode: "lines",
      name: 'AAPL High',
      x: [1, 2, 3, 4],
      y: [10, 15, 13, 17],
      line: { color: '#17BECF' }
    }

    const trace2 = {
      type: "scatter",
      mode: "lines",
      name: 'AAPL Low',
      x: [1, 2, 3, 4],
      y: [16, 5, 11, 9],
      line: { color: '#7F7F7F' }

    }


    const data = [trace1, trace2];

    const layout = {

      title: 'Time Series with Rangeslider',
      xaxis: {
        autorange: true,
        // range: ['2015-02-17', '2017-02-16'],
        // rangeselector: {
        //   buttons: [
        //     {
        //       count: 1,
        //       label: '1m',
        //       step: 'month',
        //       stepmode: 'backward'
        //     },
        //     {
        //       count: 6,
        //       label: '6m',
        //       step: 'month',
        //       stepmode: 'backward'
        //     },
        //     { step: 'all' }
        //   ]
        // },
        rangeslider: true,
        type: 'date'
      },
      yaxis: {
        autorange: true,
        range: [86.8700008333, 138.870004167],
        type: 'linear'
      }

    };

    Plotly.newPlot('rangesliderPlot_' + this.index, data, layout);

  },
  methods: {
  },
  computed: {
  },
  watch: {
  },
};
</script>

<style scoped>
#RangesliderPlot {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>