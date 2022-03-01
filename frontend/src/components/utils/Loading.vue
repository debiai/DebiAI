<template>
  <div id="loading">
    <!-- Displaying the current requests -->
    <transition-group id="list" name="list" tag="p">
      <div class="request" v-for="req in requests" :key="req.code">
        <div class="top">
          <div class="name">{{ req.name }}</div>
          <div class="loader" />
        </div>
        <!-- Display the progress bar if anny -->
        <div class="progress" v-if="req.progress !== undefined">
          <div class="bar" :style="'width:' + req.progress * 100 + '%'"></div>
        </div>
      </div>
    </transition-group>
    <!-- Displaying the server connection status -->
    <div id="connectionStatus">
      <span
        id="status"
        @click="pingServer"
        :title="serverUrl"
        :class="serverStatus"
        >{{ serverStatus }}</span
      >
    </div>
  </div>
</template>

<script>
import config from "../../../config";

export default {
  name: "Loading",
  data: () => {
    return {
      serverStatus: "unknown",
      serverUrl: null,
    };
  },
  created() {
    this.serverUrl = config.API_URL;

    this.pingServer();
    setInterval(() => {
      this.pingServer();
    }, 100000);
  },
  methods: {
    removeMsg(msg) {
      this.$store.commit("removeMessage", msg);
    },
    pingServer() {
      this.$backendDialog
        .ping()
        .then(() => {
          this.serverStatus = "Online";
        })
        .catch(() => {
          this.serverStatus = "Offline";
        });
    },
  },
  computed: {
    requests() {
      return this.$store.state.Dashboard.requests;
    },
  },
  watch: {
    serverStatus(n) {
      if (n == "Online") {
        this.$store.commit("sendMessage", {
          title: "success",
          msg: "The server is Online",
        });
      }
      if (n == "Offline") {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "The server is Offline",
        });
      }
    },
  },
};
</script>

<style scoped>
#loading {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 10;

  overflow: hidden;
}
#list {
  margin-bottom: 0px;
  margin-bottom: 0px;
  display: flex;
  flex-direction: column-reverse;
  align-items: flex-end;
}

/* requests */
.request {
  display: flex;
  flex-direction: column;

  margin-right: 8px;
  margin-bottom: 4px;
  padding: 4px;
  color: #fff;
  background-color: var(--info);
  border-radius: 5px;
  transition: all 0.1s;

  overflow: hidden;
}

.request .top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.request .top .name {
  padding-right: 5px;
}

.request .top .loader {
  border: 2px solid #f3f3f3; /* Light grey */
  border-top: 3px solid #3498db; /* Blue */
  border-right: 3px solid #3498db; /* Blue */
  border-radius: 100%;
  width: 10px;
  height: 10px;
  animation: spin 6s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.request .progress {
  height: 4px;
  min-width: 200px;
  margin-top: 3px;
  border: 2px solid #f3f3f3; /* Light grey */
  border-radius: 5px;
}
.request .progress .bar {
  /* width: 30%; */
  height: 100%;
  background-color: #cfecff;
  transition: width 0.5s ease-in-out;
}

/* Trasitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.2s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}

/* connection Status */
#connectionStatus {
  text-align: right;
}
#connectionStatus #srvUrl {
  text-shadow: 0 0 3px #fff;
}
#connectionStatus #status {
  padding: 3px;
  margin: 2px;
  border: solid black 1px;
  border-radius: 5px;
  cursor: pointer;
}
#connectionStatus #status.Online {
  background: var(--success);
  border-color: var(--success);
  color: white;
}
#connectionStatus #status.Offline {
  background: var(--danger);
  border-color: var(--danger);
  color: white;
}
</style>