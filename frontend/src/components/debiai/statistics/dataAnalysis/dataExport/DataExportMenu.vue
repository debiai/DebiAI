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
                <span class="name"> Annotation value </span>
                <span class="value">
                    <input type="text" v-model="extraValue">
                    <DocumentationBlock>
                        Add an extra value to the exported Json data.
                        <br>
                        This value can be used for anotation or for object creation purpose.
                    </DocumentationBlock>
                </span>
            </div>
            <div class="data">
                <span class="name"> Exported data </span>
                <pre class="value" id="exportedData">

{{ JSON.stringify(dataToExportDisplay, undefined, 2) }}

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
            extraValue: null,
        };
    },
    props: {
        dataToExport: { type: Object, required: true },
    },
    created() { },
    methods: {
        exportData(methodId) {
            this.exporting = true;

            // Add extra value to data
            const dataToExport = { ...this.dataToExport };
            if (this.extraValue) dataToExport.value = this.extraValue;

            // Export data
            this.$backendDialog
                .exportData(dataToExport, methodId)
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
    computed: {
        dataToExportDisplay() {
            const data = this.$props.dataToExport;
            if (this.extraValue) data.value = this.extraValue;
            else delete data.value;
            return data;
        },
    },
};
</script>

<style scoped>
/* Form: */
.dataGroup {
    flex-direction: column;
    align-items: center;
}

.dataGroup .data+.data {
    padding-top: 4px;
}

.dataGroup #exportedData {
    margin: 0;
    padding-left: 10px;
    max-width: 400px;
    max-height: 230px;
    overflow: scroll;
    font-size: 0.7em;
    font-family: monospace;
    justify-content: flex-start;
    text-align: left;
}
</style>