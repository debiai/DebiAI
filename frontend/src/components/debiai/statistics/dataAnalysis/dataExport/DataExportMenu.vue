<template>
    <div id="DataExportMenu">
        <h2>
            Export widget data
            <button @click="$emit('cancel')" class="red">Cancel</button>
        </h2>
        <!-- Export params -->
        <form v-on:submit.prevent class="dataGroup">
            <!-- Exported data -->
            <div class="data">
                <span class="name"> Exported data </span>
                <pre class="value">


{{ JSON.stringify(dataToExport, undefined, 2) }}


                </pre>
            </div>
        </form>

        <!-- Export method list -->
        <ExportMethodSelection :disableExport="exporting" @exportMethodSelected="exportData" />
    </div>
</template>

  <script>
import ExportMethodSelection from "./ExportMethodSelection.vue";

export default {
    components: { ExportMethodSelection },
    name: "DataExportMenu",
    data() {
        return {
            exporting: false,
        };
    },
    props: {
        dataToExport: { type: Object, required: true },
    },
    created() { },
    methods: {
        exportData(methodId) {
            this.exporting = true;

            this.$backendDialog
                .exportData(this.dataToExport, methodId)
                .then(() => {
                    this.$store.commit("sendMessage", {
                        title: "success",
                        msg: "Data exported successfully",
                    });
                    this.$emit("exported");
                })
                .catch((e) => {
                    console.log(e);
                    if (e.response && e.response.data) {
                        this.$store.commit("sendMessage", {
                            title: "error",
                            msg: e.response.data,
                        });
                    } else {
                        this.$store.commit("sendMessage", {
                            title: "error",
                            msg: "Error while exporting the data",
                        });
                    }
                }).finally(() => {
                    this.exporting = false;
                });
        },
    },
};
</script>

  <style scoped>
  /* Form: */
  .dataGroup {
      flex-direction: column;
  }

  .dataGroup .data+.data {
      padding-top: 4px;
  }

  .dataGroup .value {
      margin: 0;
      padding:20px;
      display: block;
      flex: 1;
      text-align: left;
      max-width: 400px;
      max-height: 200px;
      overflow: scroll;
  }
  </style>