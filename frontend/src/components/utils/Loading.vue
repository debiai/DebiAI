<template>
  <div id="loading">
    <!-- Displaying the current requests -->
    <transition-group
      id="list"
      name="list"
      tag="p"
    >
      <div
        class="request"
        v-for="req in requests"
        :key="req.code"
      >
        <!-- Name of the request -->
        <div class="top">
          <div class="name">{{ req.name }}</div>
          <div class="loader" />
        </div>

        <!-- Progress bar if anny -->
        <div
          class="progress"
          v-if="req.progress !== undefined"
        >
          <div
            class="bar"
            :style="'width:' + req.progress * 100 + '%'"
          ></div>
        </div>

        <!-- Time remaining-->
        <div
          v-if="req.remaining !== undefined"
          class="remaining"
        >
          Time remaining: {{ $services.timeStampToTime(req.remaining) }} <br />
          <span v-if="req.remaining > 60000">
            Time of arrival: ~{{ $services.timeStampToHourAndMinute(req.timeArrival + 60000) }}
          </span>
        </div>

        <!-- Quantity processed -->
        <div
          v-if="req.quantity > 0"
          class="quantity"
        >
          Amount loaded: {{ req.quantity }} <br />
          Time spent: {{ $services.timeStampToTime(Date.now() - req.creationTime) }} <br />
          Time per 100000 items:
          {{ $services.timeStampToTime(((Date.now() - req.creationTime) / req.quantity) * 100000) }}
        </div>

        <!-- Button to cancel the request -->
        <button
          v-if="req.cancellable"
          @click="cancelRequest(req)"
          class="blue"
        >
          Cancel
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
export default {
  name: "Loading",
  data: () => {
    return {};
  },
  created() {},
  methods: {
    removeMsg(msg) {
      this.$store.commit("removeMessage", msg);
    },
    cancelRequest(req) {
      this.$store.commit("cancelRequest", req.code);
    },
  },
  computed: {
    requests() {
      const requests = this.$store.state.Dashboard.requests;
      const time = Date.now();

      requests.forEach((request) => {
        if (request.progress !== undefined && request.progress > 0) {
          // Calculating the remaining time
          const timeSpent = time - request.creationTime;
          const estimatedTimeLeft = timeSpent / request.progress - timeSpent;
          request.remaining = estimatedTimeLeft;

          // Calculating the time of arrival
          const timeArrival = time + estimatedTimeLeft;
          request.timeArrival = timeArrival;
        }
      });

      return requests;
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
  background-color: var(--blue);
  border-radius: 3px;
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
  border: 2px solid var(--greyLight);
  border-top: 3px solid var(--blue);
  border-right: 3px solid var(--blue);
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
  border: 2px solid var(--greyLight);
  border-radius: 5px;
}
.request .progress .bar {
  /* width: 30%; */
  height: 100%;
  background-color: var(--greyLight);
  transition: width 0.5s ease-in-out;
}

.request .remaining {
  margin-top: 3px;
  font-size: 0.8em;
  text-align: left;
  font-weight: bold;
}
.request .quantity {
  margin-top: 3px;
  font-size: 0.8em;
  text-align: left;
  font-weight: bold;
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
</style>
