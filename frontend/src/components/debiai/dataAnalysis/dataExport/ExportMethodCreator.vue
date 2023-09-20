<template>
  <div id="ExportMethodCreator">
    <h2 class="aligned spaced">
      <span class="aligned spaced">
        Creation of a new export method
        <DocumentationBlock>
          Please note that all the export requests will be sent through the DebiAI server and not
          the client. <br />
          If the service that you are trying to reach is located on a different device, the use of
          localhost won't work.
        </DocumentationBlock>
      </span>

      <button
        @click="$emit('cancel')"
        class="red marged"
      >
        Cancel
      </button>
    </h2>

    <!-- Export method name -->
    <form
      v-on:submit.prevent
      class="dataGroup"
    >
      <!-- Selected samples -->
      <div class="data">
        <span class="name"> Export method name </span>
        <span class="value">
          <input
            type="text"
            v-model="exportMethodName"
            style="flex: 2"
          />
        </span>
      </div>
    </form>

    <div
      id="methodList"
      class="itemList"
    >
      <!-- Post export type -->
      <div
        id="post"
        class="item"
      >
        <h3>Post - http</h3>
        <div class="parameters">
          <span>
            Url:
            <input
              type="text"
              v-model="postUrl"
              placeholder="http://localhost:3010/debiai_export/"
            />
          </span>
        </div>
        <button
          class="green"
          @click="createMethod('post', [postUrl])"
        >
          Create
        </button>
      </div>

      <!-- Kafka export type -->
      <div
        id="kafka"
        class="item"
      >
        <h3>Kafka</h3>
        <div class="parameters">
          <span>
            Server:
            <input
              type="text"
              v-model="kafkaServer"
              placeholder="kafka.svc.local:9092"
            />
          </span>
          <span>
            Topic:
            <input
              type="text"
              v-model="kafkaTopic"
              placeholder="kafka_topic"
            />
          </span>
        </div>
        <button
          class="green"
          @click="createMethod('kafka', [kafkaServer, kafkaTopic])"
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
      exportMethodName: "New export method",

      // Post
      postUrl: "",

      // Kafka
      kafkaServer: "",
      kafkaTopic: "",
    };
  },
  methods: {
    createMethod(type, parameters) {
      console.log(type, parameters);
      this.$backendDialog
        .addExportMethod(this.exportMethodName, type, parameters)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Export method created successfully",
          });
          this.$emit("created");
        })
        .catch((e) => {
          console.log(e);
          console.log(e.response);
          if ("response" in e && "data" in e.response) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: e.response.data,
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "An error occurred",
            });
          }
        });
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
  flex: 1;
  gap: 5px;
  padding: 0px 30px 3px 30px;
}
.parameters span input {
  width: 300px;
}
</style>
