<template>
  <div id="ExportMethodCreator">
    <h2 class="aligned spaced">
      <span class="aligned spaced">
        Creation of a new export method
        <DocumentationBlock>
          Please note that all the export requests will be sent through the
          DebiAI server and not the client. <br />
          If the service that you are trying to reach is located on a different
          device, the use of localhost won't work.
        </DocumentationBlock>
      </span>

      <button @click="$emit('cancel')" class="red marged">Cancel</button>
    </h2>

    <div id="methodList" class="itemList">
      <div id="kafka" class="item">
        <h3>Kafka</h3>
        <div class="parameters">
          <span>
            Method name:
            <input
              type="text"
              v-model="methodName"
              placeholder="Kafka export"
            />
          </span>
          <span>
            Server:
            <input
              type="text"
              v-model="kafkaServer"
              placeholder="localhost:9092"
            />
          </span>
          <span>
            Topic:
            <input type="text" v-model="kafkaTopic" placeholder="kafka_topic" />
          </span>
        </div>
        <button
          class="green"
          @click="createMethod('kafka', { kafkaServer, kafkaTopic })"
        >
          Create
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExportMethodCreator",
  data() {
    return {
      // Kafka
      methodName: "",
      kafkaServer: "",
      kafkaTopic: "",
    };
  },
  created() {
    // Load the exportMethods
    // TODO
  },
  methods: {
    createMethod(name, parameters) {
      console.log(name, parameters);
      //   this.$backendDialog
      //     .updateTag(projectId, this.selectionName, tagHash)
      //     .then(() => {
      //       this.$store.commit("sendMessage", {
      //         title: "success",
      //         msg: "Tag uploaded successfully",
      //       });
      //       this.$emit("created");
      //     })
      //     .catch((err) => {
      //       console.error(err);
      //       this.$store.commit("sendMessage", {
      //         title: "error",
      //         msg: "Error while saving or updating the tag to the server",
      //       });
      //     });
      this.$emit("created");
    },
  },
  computed: {
    selectionExportNameOk() {
      return this.selectionName.length >= 1;
    },
  },
};
</script>

<style scoped>
#methodList .item {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  margin: 5px;
}

.parameters {
  display: flex;
  flex-direction: column;
  text-align: left;
  gap: 5px;
  padding: 0px 30px 3px 30px;
}
</style>