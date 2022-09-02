<template>
    <div id="ExportMethodSelection">
        <!-- Export method list -->
        <div>
            <h3 style="text-align: left; padding-top: 15px">
                Select an export method:
            </h3>
            <div id="exportMethods" class="card" v-if="exportMethods">

                <div v-if="exportMethods.length === 0" class="marged">
                    No export method available, please create one.
                </div>

                <div class="itemList">
                    <div class="exportMethod item" v-for="exportMethod in exportMethods" :key="exportMethod.id">
                        <h3 class="name">
                            {{ exportMethod.name }}
                            <button class="red" @click="deleteExportMethod(exportMethod.id)"
                                v-if="exportMethod.deletable !== false">
                                <b>Delete</b>
                            </button>
                            <span style="flex: 1"></span>
                            <button class="green" @click="selectExportMethod(exportMethod.id)"
                                :disabled="disableExport">
                                Export
                            </button>
                        </h3>

                        <div class="details">
                            <div class="type">{{ exportMethod.type }}</div>
                            <div class="parameters">
                                <div class="parameter" v-for="(parameter, i) in exportMethod.parameters" :key="i">
                                    <u> {{ exportMethod.parameterNames[i] }}:</u>
                                    {{ parameter }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else id="exportMethods" class="card" style="justify-content: center; color: grey">
                Loading export methods
            </div>
        </div>
        <div style="text-align: right">
            <button class="green" @click="newExportMethod">New export method</button>
        </div>

        <!-- New Method modal -->
        <modal v-if="newExportMethodModal">
            <ExportMethodCreator @cancel="newExportMethodModal = false"
                @created="newExportMethodModal = false; loadExportMethods()" />
        </modal>
    </div>
</template>

  <script>
import ExportMethodCreator from "./ExportMethodCreator.vue";

export default {
    components: { ExportMethodCreator },
    name: "SelectionExportMenu",
    data() {
        return {
            exportMethods: null,
            newExportMethodModal: false,
        };
    },
    props: {
        disableExport: { type: Boolean, default: false },
    },
    created() {
        // Load the exportMethods
        this.loadExportMethods();
    },
    methods: {
        loadExportMethods() {
            this.exportMethods = null;
            this.$backendDialog.getExportMethods().then((exportMethods) => {
                this.exportMethods = exportMethods;
            });
        },
        selectExportMethod(methodId) {
            this.$emit("exportMethodSelected", methodId);
        },

        deleteExportMethod(id) {
            this.$backendDialog.deleteExportMethod(id).then(() => {
                this.$store.commit("sendMessage", {
                    title: "success",
                    msg: "Export method deleted",
                });
            }).catch((err) => {
                console.error(err);
                this.$store.commit("sendMessage", {
                    title: "error",
                    msg: "Error while deleting the export method",
                });
            }).finally(() => this.loadExportMethods());

        },

        newExportMethod() {
            this.newExportMethodModal = !this.newExportMethodModal;
        },
    },
    computed: {},
};
</script>

  <style scoped>
  /* Methods: */
  #exportMethods {
      display: flex;
      min-width: 600px;
      height: 400px;
      overflow: auto;
  }

  .exportMethod {
      display: flex;
      flex: 1;
      flex-direction: column;
      align-items: stretch;
  }

  .exportMethod .name {
      display: flex;
      align-items: center;
      gap: 10px;
  }

  .exportMethod .details {
      display: flex;
      align-items: flex-start;
      padding: 10px;
      gap: 10px;
  }

  .exportMethod .details .parameters {
      border-left: 1px solid rgb(75, 75, 75);
      text-align: left;
      padding-left: 15px;
      opacity: 80%;
  }

  .exportMethod .details .parameter {
      padding-bottom: 8px;
  }
  </style>