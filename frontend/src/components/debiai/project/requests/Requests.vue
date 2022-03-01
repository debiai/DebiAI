<template>
  <div id="Requests">
    <!-- Requests creation modal -->
    <modal v-if="requestCreation">
      <RequestCreation
        @close="requestCreation = false"
        @newRequest="updateRequests"
      />
    </modal>

    <!-- Request modal -->
    <modal v-if="selectedRequestId">
      <Request
        :requestId="selectedRequestId"
        @close="selectedRequestId = null"
        @newSelection="$emit('newSelection')"
      />
    </modal>

    <div id="requests" class="card">
      <div class="header">
        <h2>
          <inline-svg
            :src="require('../../../../assets/svg/request.svg')"
            width="20"
            height="20"
            style="margin-right: 10px"
          />Requests
          <DocumentationBlock>
            A <b> request</b> is a very light set of constraints that can be
            used to filter the project samples and create selections.
            <br />
            A <b> selection </b>
            is a list of samples created by a request at a given moment based on
            the data currently added to the project. This is why selections from
            the same request can be different if the samples have evolved.
          </DocumentationBlock>
        </h2>
        <div v-if="selectionMode">Select a request</div>
        <span>
          <!-- Create a request btn -->
          <button
            v-if="!selectionMode"
            @click="requestCreation = !requestCreation"
          >
            + Create a new request
          </button>
          <button class="red" @click="$emit('close')">Close</button>
        </span>
      </div>

      <div class="itemList">
        <!-- No requests msg -->
        <transition name="fade">
          <div v-if="requests !== null && requests.length === 0">
            No requests
          </div>
        </transition>
        <!-- Requests list -->
        <transition name="fade">
          <div class="itemList" v-if="requests !== null && requests.length > 0">
            <!-- Request Item -->
            <div
              class="item request selectable"
              v-for="request in requests"
              v-bind:key="request.id"
              @click="selectRequest(request)"
            >
              <!-- Request name -->
              <h4 class="requestName">
                {{ request.name }}
              </h4>
              <!-- description -->
              <span class="requestDescription">
                {{ request.description }}
              </span>

              <!-- nb Filters -->
              <span class="nbFilters" title="Request filters">
                {{ request.filters.length }}
                <inline-svg
                  :src="require('../../../../assets/svg/filter.svg')"
                  width="14"
                  height="14"
                />
              </span>

              <!-- Creation date -->
              <span
                class="date"
                :title="$services.timeStampToDate(request.creationDate)"
              >
                Created {{ $services.prettyTimeStamp(request.creationDate) }}
              </span>

              <!-- delete btn -->
              <button
                @click="(event) => removeRequest(event, request.id)"
                class="red"
              >
                Delete
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import RequestCreation from "./RequestCreation.vue";
import Request from "./Request.vue";

export default {
  components: { RequestCreation, Request },
  props: { selectionMode: { type: Boolean, default: false } },
  data() {
    return {
      requests: null,
      requestCreation: false,
      selectedRequestId: null,
    };
  },
  created() {
    this.getRequests();
  },
  methods: {
    getRequests() {
      let projectId = this.$store.state.ProjectPage.projectId;
      this.requests = null;
      this.$backendDialog.getRequests(projectId).then((requests) => {
        this.requests = requests;
        // sort requests by creation date
        this.requests.sort((a, b) => b.creationDate - a.creationDate);
      });
    },
    selectRequest(request) {
      if (this.selectionMode) this.$emit("requestSelected", request);
      else this.selectedRequestId = request.id;
    },
    removeRequest(event, requestId) {
      let projectId = this.$store.state.ProjectPage.projectId;

      this.$backendDialog
        .delRequest(projectId, requestId)
        .then(() => {
          this.requests = this.requests.filter(
            (request) => request.id !== requestId
          );
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Request deleted",
          });
        })
        .catch((error) => {
          console.error(error);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Error while deleting the request",
          });
        });
      event.stopPropagation();
    },
    updateRequests() {
      this.requestCreation = false;
      this.getRequests();
    },
  },
};
</script>

<style scoped>
#Requests {
  height: 80vh;
  width: 50vw;
  display: flex;
}
.card {
  flex: 1;
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  padding-bottom: 20px;
}
.header h2 {
  display: flex;
  justify-content: space-between;
}
.request {
  justify-content: space-between;
}
.requestName {
  min-width: 100px;
}
.requestDescription {
  font-size: 0.9em;
  opacity: 0.7;
  white-space: pre-wrap;
}
.nbFilters {
  min-width: 40px;
}
.date {
  min-width: 80px;
}
</style>