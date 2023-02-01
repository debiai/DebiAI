<template>
  <div id="frontPage">
    <!-- header -->
    <div id="head">
      <!-- DebiAI Logo -->
      <img src="@/assets/images/DebiAI.png" alt="DebiAI" height="48" />
      <!-- DebiAI version -->
      <a id="version" href="https://github.com/debiai/debiai/" target="_blank">
        {{ appVersion }}
      </a>
      <!-- Doc link -->
      <a
        id="version"
        href="https://debiai.irt-systemx.fr/debiai/"
        target="_blank"
      >
        Online documentation
      </a>

      <!-- IRT Logo -->
      <p id="irtLogo">
        <img src="@/assets/images/SystemX.png" alt="SystemX" height="38" />
      </p>

      <!-- Data provider manager -->
      <button
        id="dataProviders"
        title="List the data providers"
        @click="displayDataProviders = !displayDataProviders"
      >
        Manage data providers
      </button>
      <input placeholder="Search project" v-model="searchBar" />
    </div>

    <!-- Title, name of the columns -->
    <div id="projectTitle">
      <h2>Projects :</h2>

      <!-- Items details -->
      <div id="itemDetails">
        <!-- Nb samples -->
        <div class="nbSamples" title="Number of samples">
          <inline-svg
            :src="require('@/assets/svg/data.svg')"
            width="14"
            height="14"
          />
          Samples
        </div>

        <!-- Nb requests -->
        <div class="nbSelections" title="Project selections">
          <inline-svg
            :src="require('@/assets/svg/request.svg')"
            width="14"
            height="14"
          />
          Requests
        </div>

        <!-- Nb selections -->
        <div class="nbSelections" title="Project selections">
          <inline-svg
            :src="require('@/assets/svg/loupe.svg')"
            width="14"
            height="14"
          />
          Selections
        </div>

        <!-- Nb tags -->
        <div class="nbSelections" title="Project selections">
          <inline-svg
            :src="require('@/assets/svg/tag.svg')"
            width="14"
            height="14"
          />
          Tags
        </div>

        <!-- Nb model results -->
        <div class="nbModel" title="Model added to the project">
          <inline-svg
            :src="require('@/assets/svg/gear.svg')"
            width="17"
            height="17"
          />
          Models
        </div>
      </div>
      <div id="controls">
        <button class="warning" @click="loadProjects">
          <inline-svg
            :src="require('@/assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>
      </div>
    </div>
    <!-- Project list -->
    <transition name="fade">
      <div id="projects" v-if="projects !== null && projects.length">
        <div
          class="project"
          v-for="project in filteredProject"
          :key="project.id"
          @click="selectProject(project.id)"
        >
          <!-- Project name & description -->
          <div class="nameDesc">
            <div class="name">{{ project.name }}</div>
            <div class="description">
              <!-- TODO -->
            </div>
          </div>
          <!-- Project items -->
          <div class="items" v-if="!project.error">
            <!-- Nb samples -->
            <div class="nbSamples" title="Number of samples">
              <inline-svg
                :src="require('@/assets/svg/data.svg')"
                width="14"
                height="14"
              />
              {{ project.nbSamples }}
            </div>

            <!-- Nb requests -->
            <div class="nbRequests" title="Project requests">
              <inline-svg
                :src="require('@/assets/svg/request.svg')"
                width="14"
                height="14"
              />
              {{ project.nbRequests }}
            </div>

            <!-- Nb selections -->
            <div class="nbSelections" title="Project selections">
              <inline-svg
                :src="require('@/assets/svg/loupe.svg')"
                width="14"
                height="14"
              />
              {{ project.nbSelections }}
            </div>

            <!-- Nb tags -->
            <div class="nbTags" title="Project tags">
              <inline-svg
                :src="require('@/assets/svg/tag.svg')"
                width="14"
                height="14"
              />
              {{ project.nbTags }}
            </div>

            <!-- Nb model results -->
            <div class="nbModel" title="Model added to the project">
              <inline-svg
                :src="require('@/assets/svg/gear.svg')"
                width="17"
                height="17"
              />
              {{ project.nbModels }}
            </div>
          </div>
          <div class="items error" v-else>
            Something is wrong with the project :
            <br />
            {{ project.exeption }}
          </div>
          <!-- Dates -->
          <div class="dates" v-if="!project.error">
            <span
              class="createdDate"
              :title="$services.timeStampToDate(project.creationDate)"
            >
              Created {{ $services.prettyTimeStamp(project.creationDate) }}
            </span>
            <span
              class="updatedDate"
              :title="$services.timeStampToDate(project.updateDate)"
              v-if="project.updateDate !== project.creationDate"
            >
              Updated {{ $services.prettyTimeStamp(project.updateDate) }}
            </span>
          </div>
        </div>
      </div>
    </transition>
    <!-- Loading -->
    <div id="loading" v-if="projects === null">Loading</div>
    <!-- No project message -->
    <div id="noProjects" v-else-if="!projects.length">
      <span>
        No projects<br /><br />
        Find out how to add a project on our
        <a href="https://debiai.irt-systemx.fr/dataInsertion" target="_blank">
          Website
        </a>
      </span>
    </div>

    <!-- Data provider modals -->
    <modal v-if="displayDataProviders">
      <dataProviders @cancel="displayDataProviders = false" />
    </modal>
  </div>
</template>

<script>
import { version } from "../../../../package";
import dataProviders from "./dataproviders/DataProviders.vue";

export default {
  name: "FrontPage",
  components: {
    dataProviders,
  },
  data: () => {
    return {
      projects: null,
      searchBar: "",
      appVersion: version,
      displayDataProviders: false,
    };
  },
  created() {
    // Load the projects
    this.loadProjects();
  },
  methods: {
    loadProjects() {
      this.projects = null;
      this.$backendDialog
        .getProjects()
        .then((projects) => {
          this.projects = projects.sort((a, b) => b.updateDate - a.updateDate);
        })
        .catch((e) => {
          console.error(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Unexpected error while loading projects",
          });
        });
    },
    selectProject(projectId) {
      this.$router.push({
        path: "/project/" + projectId,
        params: { projectId }, // tu put the name in the title
      });
    },
  },
  computed: {
    filteredProject() {
      if (this.projects === null) return null;
      if (this.searchBar === "") return this.projects;

      return this.projects.filter((p) =>
        p.name.toLowerCase().includes(this.searchBar.toLowerCase())
      );
    },
  },
};
</script>

<style scoped>
#frontPage {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Head  */
#head {
  display: flex;
  padding: 5px;
  background-color: var(--primary);
  border-bottom: solid 5px var(--primaryDark);
  color: white;
  align-items: center;
}

#head #version {
  padding-left: 15px;
  font-size: 1.4em;
  font-family: system-ui;
  color: white;
}

#head #version:visited {
  color: white;
}

#head #irtLogo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  padding: 0;
  margin: 0;
}

#head #debiaiLogo {
  justify-content: center;
  padding: 0;
  margin: 0;
}

#head #dataProviders {
  margin-right: 20px;
}

#projectTitle {
  text-align: left;
  padding: 15px;
  margin: 0 15px 0 15px;
  display: flex;
  justify-content: space-between;
}

#projectTitle h2 {
  flex: 3;
}

#projectTitle #itemDetails {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8em;
  opacity: 0.7;
}

#projectTitle #itemDetails > * {
  flex: 1;
  text-align: left;
}

#projectTitle #controls {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

/* Projects */
#projects {
  flex: 1;
  overflow-y: auto;
}

.project {
  cursor: pointer;
  display: grid;
  grid-template-columns: 3fr 1fr 1fr;
  grid-template-rows: 1fr;
  grid-template-areas: "nameDesc items dates";

  padding: 15px;
  margin: 0 20px 0 20px;
  border-bottom: solid rgba(0, 0, 0, 0.172) 2px;
  transition: background-color ease-out 0.1s;
}

.project:first-child {
  border-top: solid rgba(0, 0, 0, 0.172) 2px;
}

.project:hover {
  background-color: rgba(0, 0, 0, 0.076);
}

.project > * {
  display: flex;
  align-items: center;
}

/* Name & desc  */
.nameDesc {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 0fr 1fr;
  gap: 0px 0px;
  grid-template-areas:
    "name"
    "description";
  grid-area: nameDesc;
}

.name {
  grid-area: name;
  text-align: left;
  font-weight: bold;
}

.description {
  grid-area: description;
  text-align: left;
  opacity: 0.8;
}

/* Items */
.items {
  justify-content: space-around;
  display: flex;
  opacity: 0.8;
}

.items > * {
  flex: 1;
  text-align: left;
}

.nbSamples {
  grid-area: nbSamples;
}

.nbSelections {
  grid-area: nbSelections;
}

.nbModel {
  grid-area: nbModel;
}

/* Dates */
.dates {
  opacity: 0.8;
  grid-area: dates;
  display: flex;
  flex-direction: column;
}

.createdDate {
  grid-area: createdDate;
}

.updatedDate {
  grid-area: updatedDate;
}

/* No projects */
#loading {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5em;
  opacity: 0.5;
}

#noProjects {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: 1.5em;
  opacity: 0.5;
}
</style>
