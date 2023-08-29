<template>
  <div id="frontPage">
    <!-- header -->
    <div id="header">
      <!-- Logo, version, doc link -->
      <div id="left">
        <!-- DebiAI Logo -->
        <img
          src="@/assets/images/DebiAI_black.png"
          alt="DebiAI"
          id="debiaiLogo"
          height="48"
        />
        <!-- DebiAI version -->
        <a
          id="version"
          href="https://github.com/debiai/debiai/"
          target="_blank"
        >
          {{ appVersion }}
        </a>
        <!-- Doc link -->
        <a
          id="docLink"
          href="https://debiai.irt-systemx.fr/"
          target="_blank"
        >
          Online documentation
        </a>
      </div>

      <!-- Data-providers, searchbar -->
      <div id="right">
        <!-- Data provider manager -->
        <button
          id="dataProviders"
          title="List the data providers"
          @click="displayDataProviders = !displayDataProviders"
        >
          Data providers
        </button>

        <!-- Refresh button -->
        <button
          class="warning"
          @click="loadProjects"
        >
          <inline-svg
            :src="require('@/assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>

        <!-- Search bar -->
        <input
          class="search"
          placeholder="Search project"
          v-model="searchBar"
        />
      </div>
    </div>

    <!-- Title, name of the columns -->
    <div id="projectTitle">
      <h2>Projects</h2>

      <!-- Items details -->
      <div id="itemDetails">
        <!-- Nb samples -->
        <div
          class="nbSamples"
          title="Number of samples"
        >
          <inline-svg
            :src="require('@/assets/svg/data.svg')"
            width="14"
            height="14"
          />
          Samples
        </div>

        <!-- Nb selections -->
        <div
          class="nbSelections"
          title="Project selections"
        >
          <inline-svg
            :src="require('@/assets/svg/loop.svg')"
            width="14"
            height="14"
          />
          Selections
        </div>

        <!-- Nb model results -->
        <div
          class="nbModel"
          title="Model added to the project"
        >
          <inline-svg
            :src="require('@/assets/svg/gear.svg')"
            width="17"
            height="17"
          />
          Models
        </div>
      </div>
    </div>
    <!-- Project list -->
    <transition name="fade">
      <div
        id="projects"
        v-if="projects !== null && projects.length"
      >
        <div
          class="project"
          v-for="project in filteredProject"
          :key="project.dataProviderId + ' / ' + project.id"
          @click="selectProject(project.dataProviderId, project.id)"
        >
          <!-- Project name -->
          <div class="name">{{ project.name }}</div>

          <!-- Project items -->
          <div class="items">
            <!-- Nb samples -->
            <div
              class="nb nbSamples"
              title="Number of samples"
            >
              <inline-svg
                :src="require('@/assets/svg/data.svg')"
                width="14"
                height="14"
              />
              {{ project.nbSamples !== null ? project.nbSamples : "?" }}
            </div>

            <!-- Nb selections -->
            <div
              class="nb nbSelections"
              title="Number of selections"
            >
              <inline-svg
                :src="require('@/assets/svg/loop.svg')"
                width="14"
                height="14"
              />
              {{ project.nbSelections !== null ? project.nbSelections : "?" }}
            </div>

            <!-- Nb models -->
            <div
              class="nb nbModel"
              title="Number of model added to the project"
            >
              <inline-svg
                :src="require('@/assets/svg/gear.svg')"
                width="17"
                height="17"
              />
              {{ project.nbModels !== null ? project.nbModels : "?" }}
            </div>
          </div>
          <!-- Dates -->
          <div class="dates">
            <span
              class="createdDate"
              :title="$services.timeStampToDate(project.creationDate)"
              v-if="project.creationDate"
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

          <!-- Exploration button -->
          <div class="exploration aligned right">
            <button
              @click.stop
              @click="selectProjectExploration(project.dataProviderId, project.id)"
            >
              Exploration
            </button>
          </div>
        </div>
      </div>
    </transition>
    <!-- Loading -->
    <div
      id="loading"
      v-if="projects === null"
    >
      Loading
    </div>
    <!-- No project message -->
    <div
      id="noProjects"
      v-else-if="!projects.length"
    >
      <span>
        No projects<br /><br />
        Find out how to add a project on our
        <a
          href="https://debiai.irt-systemx.fr/dataInsertion"
          target="_blank"
        >
          Website
        </a>
      </span>
    </div>

    <!-- Data provider modal -->
    <modal
      v-if="displayDataProviders"
      @close="displayDataProviders = false"
    >
      <dataProviders @cancel="displayDataProviders = false" />
    </modal>
  </div>
</template>

<script>
import jsonPackage from "../../../../package";
import dataProviders from "./dataproviders/DataProviders.vue";

export default {
  name: "FrontPage",
  components: {
    dataProviders,
  },
  data: () => {
    return {
      projects: null, // List of projects
      dataProviders: null, // List of data providers that contains the projects
      searchBar: "",
      appVersion: jsonPackage.version,
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
    selectProject(dataProviderId, projectId) {
      this.$router.push({
        path: "/dataprovider/" + dataProviderId + "/project/" + projectId,
        params: { projectId, dataProviderId },
      });
    },
    selectProjectExploration(dataProviderId, projectId) {
      this.$router.push({
        path: "/dataprovider/" + dataProviderId + "/project/" + projectId + "/exploration",
        params: { projectId, dataProviderId },
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

<style lang="scss" scoped>
#frontPage {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;

  #header {
    height: 60px;
    width: 100%;

    display: flex;
    align-items: center;
    justify-content: space-between;

    background-color: var(--greyLight);
    border-bottom: var(--greyDark) 2px solid;

    #left {
      display: flex;
      align-items: center;
      gap: 10px;

      a {
        text-decoration: none;
        color: var(--fontColorLight);
      }

      #debiaiLogo {
        margin: 0px 0px 0px 15px;
      }
    }

    #right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
  }
}

#projectTitle {
  width: 100%;
  max-width: 1300px;
  text-align: left;
  margin: 30px 30px 20px 15px;
  display: flex;
  justify-content: space-between;

  h2 {
    flex: 3;
    margin-left: 30px;
  }

  #itemDetails {
    flex: 1;
    display: flex;
    gap: 10px;
    justify-content: space-between;
    align-items: center;
    color: var(--fontColorLight);
    padding-right: 270px;
  }

  #itemDetails > * {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 5px;
  }
}

/* Projects */
#projects {
  width: 100%;
  max-width: 1350px;
  flex: 1;
  overflow-y: auto;

  .project {
    cursor: pointer;
    display: grid;
    grid-template-columns: 3fr 1fr 1fr 100px;
    grid-template-rows: 1fr;
    grid-template-areas: "name items dates";

    padding: 15px;
    margin: 0 20px 0 20px;
    border-bottom: solid rgba(0, 0, 0, 0.172) 2px;
    transition: background-color ease-out 0.1s;
    min-height: 40px;

    &:first-child {
      border-top: solid rgba(0, 0, 0, 0.172) 2px;
    }

    &:hover {
      background-color: rgba(0, 0, 0, 0.076);
    }

    & > * {
      display: flex;
      align-items: center;
    }

    /* Name & desc  */
    .name {
      grid-area: name;
      display: flex;
      align-items: flex-start;
      font-weight: bold;
    }

    /* Items */
    .items {
      flex: 1;
      display: flex;

      .nb {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 0 5px 0 5px;

        .nbSamples {
          grid-area: nbSamples;
        }

        .nbSelections {
          grid-area: nbSelections;
        }

        .nbModel {
          grid-area: nbModel;
        }
      }
    }

    /* Dates */
    .dates {
      opacity: 0.8;
      grid-area: dates;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      span {
        white-space: nowrap;
      }
    }

    .createdDate {
      grid-area: createdDate;
    }

    .updatedDate {
      grid-area: updatedDate;
    }
  }
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
