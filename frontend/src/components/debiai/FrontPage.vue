<template>
  <div id="frontPage">
    <!-- header -->
    <div id="head">
      <p id="debiaiLogo">
        <img src="../../../src/assets/images/DebiAI.png" alt="DebiAI" height="48" />
      </p>
      <a id="version" href="https://github.com/debiai/debiai/" target="_blank">0.17.1</a>
      <a id="version" href="https://debiai.irt-systemx.fr/debiai/" target="_blank">Online documentation</a>

      <p id="irtLogo">
        <!-- IRT Logo -->
        <img src="../../../src/assets/images/SystemX.png" alt="SystemX" height="38" />
      </p>
      <input placeholder="Search project" v-model="searchBar" />
      <!-- <button id="addProject" title="Coming soon" disabled>New project</button> -->
    </div>

    <!-- Title -->
    <div id="projectTitle">
      <h2>Projects :</h2>

      <!-- Items details -->
      <div id="itemDetails">
        <!-- Nb samples -->
        <div class="nbSamples" title="Number of samples">
          <inline-svg :src="require('../../assets/svg/data.svg')" width="14" height="14" />
          Samples
        </div>

        <!-- Nb requests -->
        <div class="nbSelections" title="Project selections">
          <inline-svg :src="require('../../assets/svg/request.svg')" width="14" height="14" />
          Requests
        </div>

        <!-- Nb selections -->
        <div class="nbSelections" title="Project selections">
          <inline-svg :src="require('../../assets/svg/loupe.svg')" width="14" height="14" />
          Selections
        </div>

        <!-- Nb tags -->
        <div class="nbSelections" title="Project selections">
          <inline-svg :src="require('../../assets/svg/tag.svg')" width="14" height="14" />
          Tags
        </div>

        <!-- Nb model results -->
        <div class="nbModel" title="Model added to the project">
          <inline-svg :src="require('../../assets/svg/gear.svg')" width="17" height="17" />
          Models
        </div>
      </div>
      <div id="controls">
        <button class="warning" @click="loadProjects">
          <inline-svg :src="require('../../assets/svg/update.svg')" width="10" height="10" />
          Refresh
        </button>
      </div>
    </div>
    <!-- Project list -->
    <transition name="fade">
      <div id="projects" v-if="projects">
        <div class="project" v-for="project in filteredProject" :key="project.id" @click="selectProject(project.id)">
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
              <inline-svg :src="require('../../assets/svg/data.svg')" width="14" height="14" />
              {{ project.nbSamples }}
            </div>

            <!-- Nb requests -->
            <div class="nbRequests" title="Project requests">
              <inline-svg :src="require('../../assets/svg/request.svg')" width="14" height="14" />
              {{ project.nbRequests }}
            </div>

            <!-- Nb selections -->
            <div class="nbSelections" title="Project selections">
              <inline-svg :src="require('../../assets/svg/loupe.svg')" width="14" height="14" />
              {{ project.nbSelections }}
            </div>

            <!-- Nb tags -->
            <div class="nbTags" title="Project tags">
              <inline-svg :src="require('../../assets/svg/tag.svg')" width="14" height="14" />
              {{ project.nbTags }}
            </div>

            <!-- Nb model results -->
            <div class="nbModel" title="Model added to the project">
              <inline-svg :src="require('../../assets/svg/gear.svg')" width="17" height="17" />
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
            <span class="createdDate" :title="$services.timeStampToDate(project.creationDate)">
              Created {{ $services.prettyTimeStamp(project.creationDate) }}
            </span>
            <span class="updatedDate" :title="$services.timeStampToDate(project.updateDate)"
              v-if="project.updateDate !== project.creationDate">
              Updated {{ $services.prettyTimeStamp(project.updateDate) }}
            </span>
          </div>
        </div>
      </div>
    </transition>
    <div v-if="projects === null">Loading</div>
  </div>
</template>

<script>
export default {
  name: "FrontPage",
  props: {},
  data: () => {
    return {
      projects: null,
      searchBar: "",
    };
  },
  created() {
    // Load the projects
    this.loadProjects();
  },
  methods: {
    loadProjects() {
      this.projects = null;
      this.$backendDialog.getProjects().then((projects) => {
        this.projects = projects.sort((a, b) => b.updateDate - a.updateDate);
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
  padding: 10px;
  background-color: var(--primary);
  border-bottom: solid 5px var(--primaryDark);
  color: white;
}

#head>* {
  display: flex;
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
  flex: 1;
  justify-content: center;
  padding: 0;
  margin: 0;
}

#head #debiaiLogo {
  justify-content: center;
  padding: 0;
  margin: 0;
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

#projectTitle #itemDetails>* {
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

.project>* {
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

.items>* {
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
</style>
