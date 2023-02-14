<template>
  <div
    :id="'SampleArray' + index"
    class="dataVisualisationWidget"
  >
    <!-- Columns selection Modals -->
    <ColumnSelection
      v-show="settings"
      title="Select the columns to display in the array"
      :data="data"
      :validateRequiered="true"
      :colorSelection="true"
      :defaultSelected="selectedColumnsIds"
      v-on:cancel="settings = false"
      v-on:validate="columnsSelect"
    />

    <vue-table-dynamic
      v-if="displayArray"
      :params="params"
    ></vue-table-dynamic>
  </div>
</template>

<script>
import VueTableDynamic from "vue-table-dynamic";

// components
import ColumnSelection from "../../common/ColumnSelection";
import swal from "sweetalert";

export default {
  components: {
    VueTableDynamic,
    ColumnSelection,
    // Column,
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  data() {
    return {
      displayArray: false,
      selectedColumnsIds: [],
      settings: true,
      columnsSelection: false,

      // VueTableDynamic props
      params: {
        data: [[]],
        header: "row",
        // border: true,
        stripe: true,
        // showCheck: true, // TODO : use as data selection
        enableSearch: true,
        pagination: true,
        height: 100,
        pageSize: 10,
        // pageSizes: [5, 10, 20, 50],
      },
    };
  },
  created() {
    // Select the 3 firsts columns
    for (let i = 0; i < 3; i++) if (this.data.nbColumns > i) this.selectedColumnsIds.push(i);

    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
    });
    this.$parent.$on("redraw", this.updateArray);
  },
  mounted() {
    this.setArrayHeight();

    this.$parent.$parent.$on("GridStack_resizestop", () => {
      this.setArrayHeight();
    });
  },
  methods: {
    setArrayHeight() {
      let d = document.getElementById("SampleArray" + this.index) || null;
      if (d) this.params.height = d.clientHeight - 120; //* 0.75;
    },
    updateArray() {
      if (this.selectedData.length <= 1000) this._updateArray();
      else {
        swal({
          title: "Display the array ?",
          text: "There is a lot of samples to display, the process may be  resource-intensive.\rYou can always select fewer data.",
          buttons: true,
          dangerMode: true,
        }).then((validate) => {
          if (validate) this._updateArray();
          else if (!this.displayArray) this.settings = true;
        });
      }
    },
    _updateArray() {
      let labels = this.selectedColumnsIds.map((i) => this.data.columns[i].label);
      var data = new Array(this.selectedData.length + 1); // Number of rows
      data[0] = labels;

      for (var i = 1; i < data.length; i++) data[i] = new Array(this.selectedColumnsIds.length); // Number of columns

      this.selectedColumnsIds.forEach((columnIndex, i) => {
        let col = this.data.columns.find((c) => c.index == columnIndex);
        this.selectedData.map((j, indRow) => (data[indRow + 1][i] = col.values[j]));
      });

      this.displayArray = true;
      this.settings = false;

      this.params.data = data;
      this.params.sort = this.selectedColumnsIds.map((c, i) => i);
      this.$parent.selectedDataWarning = false;
    },
    columnsSelect(columnIndexs) {
      this.selectedColumnsIds = columnIndexs;

      this.settings = false;
      this.updateArray();
    },
  },
  computed: {},
  watch: {
    selectedData: function () {
      this.$parent.selectedDataWarning = true;
    },
  },
};
</script>

<style scoped></style>
