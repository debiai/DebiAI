<template>
  <div id="Request">
    <transition name="fade">
      <div id="header" v-if="request !== null">
        <div id="title">
          <h3>Request :</h3>
          <h2>{{ request.name }}</h2>
          <!-- Creation date -->
          <span
            class="date"
            :title="$services.timeStampToDate(request.creationDate)"
          >
            Created {{ $services.prettyTimeStamp(request.creationDate) }}
          </span>
        </div>

        <button class="red" @click="$emit('close')">Close</button>
      </div>
    </transition>
    <transition name="fade">
      <div id="content" v-if="request !== null">
        <!-- Request description & filters -->
        <div id="info" class="itemList">
          <!-- Request description -->
          <div style="margin-bottom: 30px">
            <h2>Request description</h2>
            <span v-if="request.description" id="description">
              {{ request.description }}
            </span>
            <span v-else> No description </span>
          </div>

          <!-- Request filters -->
          <div id="filters">
            <h2>Request filters</h2>
            <div
              class="filter item"
              v-for="(filter, i) in request.filters"
              v-bind:key="i"
            >
              <!-- filter column label -->
              <span>
                on
                <b class="filterColumnLabel">
                  {{ filter.columnLabel }}
                </b>
              </span>
              <!-- filter type -->
              <div class="filterType">Type : {{ filter.type }}</div>
              <!-- filter inverted -->
              <div class="filterInverted" v-if="filter.inverted">
                <span>Inverted</span>
              </div>
              <!-- filter values or intervals -->
              <div class="filterValues" v-if="filter.type === 'values'">
                <div class="value" v-for="(value, j) in filter.values" :key="j">
                  {{ value }}
                </div>
              </div>
              <div class="filterIntervals" v-if="filter.type === 'intervals'">
                <div
                  class="interval"
                  v-for="(interval, j) in filter.intervals"
                  :key="j"
                >
                  Min : {{ interval.min }}, Max : {{ interval.max }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Request selection list & new selection form -->
        <div id="selections" class="card">
          <h2>Request selections</h2>
          <!-- New selection -->
          <div id="newSelection" class="card">
            <u> Create a new selection from the request filters : </u>
            <span>
              Selection name :
              <input type="text" v-model="newSelectionName" />
              <button @click="newSelection" :disabled="!newSelectionName">
                Create
              </button>
            </span>
          </div>
          <!-- request Selections -->
          <div id="selectionsList" class="itemList">
            <!-- No selection msg -->
            <div style="padding: 20px" v-if="!request.selections.length">
              No selections
            </div>

            <Selection
              class="item"
              v-for="(selection, i) in request.selections"
              :key="i"
              :selection="selection"
              @delete="deleteSelection(selection.id)"
              :displayRequest="false"
            />
          </div>
        </div>
      </div>
    </transition>
    <div v-if="requestHasBeenDeleted" class="aligned spaced">
      The request has been deleted
      <button class="red" @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import Selection from "../selections/Selection";

export default {
  name: "Request",
  components: { Selection },
  props: { requestId: { type: String, required: true } },
  data() {
    return {
      request: null,
      requestHasBeenDeleted: false,
      // Request selections
      newSelectionName: null,
    };
  },
  created() {
    this.newSelectionName = this.$services.getDate();
    this.getRequest();
  },
  methods: {
    getRequest() {
      let projectId = this.$store.state.ProjectPage.projectId;
      this.request = null;
      this.$backendDialog
        .getRequest(projectId, this.requestId)
        .then((request) => {
          this.request = request;
          // sort request selections by creation date
          this.request.selections.sort((a, b) => {
            return b.creationDate - a.creationDate;
          });
        })
        .catch((err) => {
          if (err.response.status === 404) this.requestHasBeenDeleted = true;
          else {
            console.error(err);
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Error while loading the request",
            });
          }
        });
    },

    newSelection() {
      let projectId = this.$store.state.ProjectPage.projectId;
      this.$backendDialog
        .createSelectionFromRequest(
          projectId,
          this.request.id,
          this.newSelectionName
        )
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection created",
          });

          this.getRequest();
          this.$emit("newSelection");
        })
        .catch((error) => {
          console.error(error);
          // If code is 403, one of the column does not exist
          if (error.response && error.response.status === 403) {
            this.$store.commit("sendMessage", {
              title: "warning",
              msg: "One of the columns can't be used to create this selection",
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Error while creating the selection",
            });
          }
        });
    },
    deleteSelection(selectionId) {
      let projectId = this.$store.state.ProjectPage.projectId;
      this.$backendDialog
        .delSelection(projectId, selectionId)
        .then(() => {
          this.$backendDialog;
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection deleted",
          });
          this.getRequest();
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the selection",
          });
        });
    },
  },
};
</script>

<style scoped>
#Request {
  height: 80vh;
  width: 80vw;
  display: flex;
  flex-direction: column;
}
#header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
}
#header #title {
  display: flex;
  align-items: center;
}
#header #title h3 {
  padding-right: 20px;
}
#header .date {
  padding-left: 20px;
}

#content {
  display: flex;
}
#content #info {
  flex: 1;
  padding: 20px;
}
#content #selections {
  flex: 1;
  padding: 20px;
}
#content #description {
  white-space: pre-wrap;
  opacity: 0.7;
}
#content #selections #newSelection {
  display: flex;
  padding: 20px;
}

.filter {
  display: flex;
  justify-content: space-between;
}
.filter .filterInverted {
  border: solid red 1px;
  color: red;
  border-radius: 10px;
  padding: 3px;
  font-size: 0.9em;
}
.filter .filterValues {
  display: flex;
}
.filter .filterValues .value {
  margin: 3px;
}
</style>