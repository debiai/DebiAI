<template>
  <div id="frontPage">
    <!-- header -->
    <div id="header">
      <!-- DebiAI Logo -->
      <div id="left">
        <img
          src="@/assets/images/DebiAI_black.png"
          alt="DebiAI"
          id="debiaiLogo"
          height="48"
        />
      </div>

      <!-- Data-providers, searchbar -->
      <div id="right">
        <!-- Doc -->
        <button
          class="borderless"
          @click="openDocumentation"
          title="Documentation"
        >
          <inline-svg
            :src="require('@/assets/svg/questionMarkCircle.svg')"
            width="25"
            height="25"
          />
        </button>

        <!-- dropdown menu -->
        <div style="position: relative">
          <transition name="fade">
            <dropdown-menu
              v-if="displayMenu"
              :menu="[
                {
                  name: 'Data providers',
                  action: () => {
                    displayDataProviders = !displayDataProviders;
                  },
                  icon: 'data',
                },
                {
                  name: 'separator',
                },
                {
                  name: 'Legal & privacy policy',
                  action: openLegalNotice,
                  icon: 'legal',
                },
                {
                  name: 'Latest releases',
                  action: openLatestReleases,
                  icon: 'rocket',
                },
                {
                  name: 'Suggest a feature',
                  action: createIssue,
                  icon: 'idea',
                },
                {
                  name: appVersion,
                  action: openGithub,
                  icon: 'github',
                },
              ]"
              :offset="{ x: -70, y: 45 }"
              @close="displayMenu = false"
            />
          </transition>
        </div>

        <button
          id="menuButton"
          @click="displayMenu = !displayMenu"
          class="borderless"
        >
          <div class="dot"></div>
        </button>
      </div>
    </div>

    <!-- Title, name of the columns -->
    <div id="projectTitle">
      <h2>Projects</h2>

      <!-- Items details -->
      <div id="itemDetails">
        <!-- Nb samples -->
        <div
          class="nb nbSamples"
          title="Number of samples"
        >
          <inline-svg
            :src="require('@/assets/svg/data.svg')"
            width="16"
            height="16"
          />
          Samples
        </div>

        <!-- Nb selections -->
        <div
          class="nb nbSelections"
          title="Project selections"
        >
          <inline-svg
            :src="require('@/assets/svg/loop.svg')"
            width="16"
            height="16"
          />
          Selections
        </div>

        <!-- Nb model results -->
        <div
          class="nb nbModel"
          title="Model added to the project"
        >
          <inline-svg
            :src="require('@/assets/svg/gear.svg')"
            width="16"
            height="16"
          />
          Models
        </div>
      </div>

      <!-- controls -->
      <div id="control">
        <!-- Search bar -->
        <input
          class="search"
          placeholder="🔍  Filter projects"
          v-model="searchBar"
        />
        <!-- Refresh button -->
        <button
          class="borderless aligned gapped"
          @click="loadProjects"
          title="Refresh projects"
        >
          <inline-svg
            :src="require('@/assets/svg/update.svg')"
            width="15"
            height="15"
          />
        </button>
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
        </div>
      </div>
    </transition>

    <!-- Demo message -->
    <transition name="fade">
      <div
        id="demo"
        class="tip"
        v-if="projects !== null && projects.length"
      >
        <h1>Welcome to the DebiAI demonstration instance</h1>
        <div>
          Explore the capabilities of
          <a
            href="https://debiai.irt-systemx.fr/"
            target="_blank"
            >DebiAI</a
          >, a web application designed to help data-scientists:

          <ul>
            <li>Detect anomalies and bias in their datasets faster</li>
            <li>
              Analyze the results of their models according to the contexts that matter the most for
              the problem they are trying to solve.
            </li>
          </ul>

          This demonstration instance is a great starting point to experience our app's features and
          functionalities. It features two projects made from the
          <a
            href="https://woodscape.valeo.com/woodscape/"
            target="_blank"
            >WoodScape dataset</a
          >, a dataset of fish-eye images of urban scenes made for autonomous driving applications.
          <br />
          If you're interested in following specific use cases and learning through practical
          examples, check out our
          <br />
          <br />
          <a
            id="guideLink"
            href="https://debiai.irt-systemx.fr/useCases/woodscape/"
            target="_blank"
            >Complete step by step Guide</a
          >
          <br />
          <br />
          <br />

          For detailed information on how to setup and understand DebiAI, visit our
          <a
            href="https://debiai.irt-systemx.fr/"
            target="_blank"
            >Documentation Website</a
          >.
          <br />
          This demonstration instance is powered by the
          <a
            target="_blank"
            href="https://www.irt-systemx.fr/en/"
            >IRT SystemX</a
          >
          technological research institute and the
          <a
            target="_blank"
            href="https://www.confiance.ai/en/"
            >Confiance.ai</a
          >
          research program.
        </div>

        <div
          class="aligned padded"
          style="gap: 40px; padding-top: 30px;"
        >
          <a
            target="_blank"
            href="https://www.irt-systemx.fr/en/"
          >
            <img
              src="https://www.irt-systemx.fr/wp-content/uploads/2019/09/System-X-Blanc.png"
              alt="IRT SystemX"
              height="50"
            />
          </a>

          <a
            target="_blank"
            href="https://www.confiance.ai/en/"
          >
            <img
              src="https://www.confiance.ai/wp-content/uploads/2023/09/logo-confiance@2x-1.png"
              alt="Confiance.ai"
              height="50"
            />
          </a>
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
          Online documentation
        </a>
      </span>
    </div>

    <!-- Data provider modals -->
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
import DropdownMenu from "../../common/DropdownMenu.vue";
import dataProviders from "./dataproviders/DataProviders.vue";

export default {
  name: "FrontPage",
  components: {
    dataProviders,
    DropdownMenu,
  },
  data: () => {
    return {
      projects: null, // List of projects
      displayMenu: false, // Display the dropdown menu
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
    openDocumentation() {
      window.open("https://debiai.irt-systemx.fr/", "_blank");
    },
    openLatestReleases() {
      window.open("https://github.com/debiai/debiai/releases", "_blank");
    },
    openGithub() {
      window.open("https://github.com/debiai/debiai", "_blank");
    },
    createIssue() {
      window.open("https://github.com/debiai/debiai/issues/new/choose", "_blank");
    },
    openLegalNotice() {
      this.$router.push({
        path: "/legal",
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

    button {
      height: 30px;
    }

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
      padding-right: 20px;

      #menuButton {
        width: 60px;
        .dot,
        .dot:before,
        .dot:after {
          position: absolute;
          width: 4px;
          height: 4px;
          border-radius: 10px;
          background-color: var(--fontColor);
        }

        .dot {
          left: 50%;
          margin-top: -3px;
        }

        .dot:before {
          right: 10px;
          content: "";
        }

        .dot:after {
          left: 10px;
          content: "";
        }
      }
    }
  }
}

#projectTitle {
  width: 95%;
  max-width: 1300px;
  text-align: left;
  margin: 30px 20px 20px 15px;
  display: flex;
  justify-content: space-between;

  h2 {
    font-size: 2em;
    width: 500px;
  }

  #itemDetails {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .nb {
      display: flex;
      color: var(--fontColorLight);
      justify-content: flex-start;
      width: 150px;
      gap: 5px;
      font-size: 1.3em;

      svg {
        fill: var(--fontColorLight);
      }
    }
  }

  #control {
    display: flex;
    align-items: center;
    gap: 10px;

    button {
      height: 30px;
    }
    .search {
      width: 150px;
      border-radius: 5px;
      border: solid var(--greyDark) 1px;
      font-size: 1.1em;
    }
  }
}

/* Projects */
#projects {
  width: 100%;
  max-width: 1350px;
  overflow-y: auto;

  .project {
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    padding: 15px;
    margin: 0 10px 0 10px;
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

    /* Name */
    .name {
      width: 500px;
      justify-self: flex-start;
      align-items: flex-start;
      font-weight: bold;
      text-align: left;
    }

    /* Items */
    .items {
      display: flex;

      .nb {
        display: flex;
        color: var(--fontColorLight);
        justify-content: flex-start;
        width: 150px;
        gap: 5px;

        svg {
          fill: var(--fontColorLight);
        }
      }
    }

    /* Dates */
    .dates {
      color: var(--fontColorLight);
      width: 200px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      span {
        white-space: nowrap;
      }
    }
  }
}

/* No projects */
#loading {
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translate(-50%, -50%);
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

#demo {
  display: flex;
  max-width: 1100px;
  align-items: flex-start;
  flex-direction: column;
  text-align: left;

  margin: 3px;
  margin-top: 40px;
  padding: 30px 100px 10px;
  border-radius: 5px;

  h1 {
    margin-bottom: 20px;
  }

  #guideLink {
    padding: 8px 8px;
    border-radius: 10px;
    text-decoration: none;
    border: solid white 1px;
    font-size: 1.2em;
  }
}

// Small screens
@media screen and (max-width: 1000px) {
  #frontPage {
    font-size: 0.8em;
  }

  #projectTitle {
    h2 {
      display: none;
    }
  }

  #projects {
    .project {
      .items {
        flex-direction: column;
        gap: 5px;
      }
      .dates {
        align-items: flex-start;
      }
    }
  }

  #demo {
    height: 50vh;
    overflow-y: auto;
  }
}
</style>
