<template>
  <div id="Header">
    <div id="left">
      <!-- DebiAI Logo and project name -->
      <div id="logoAndName">
        <!-- DebiAI Logo -->
        <a
          @click.exact="backToProjects()"
          @click.middle.exact="backToProjects(true)"
          @click.ctrl.exact="backToProjects(true)"
        >
          <img
            src="@/assets/images/DebiAI_black.png"
            alt="DebiAI"
            id="debiaiLogo"
            height="48"
          />
        </a>

        <!-- Project name -->
        <div
          id="projectName"
          v-if="project"
        >
          <a
            @click.exact="backToProjects()"
            @click.middle.exact="backToProjects(true)"
            @click.ctrl.exact="backToProjects(true)"
            style="color: var(--fontColorLight)"
          >
            Projects
          </a>
          /
          <a
            @click.exact="backToProject()"
            @click.middle.exact="backToProject(true)"
            @click.ctrl.exact="backToProject(true)"
          >
            {{ project.name }}
          </a>
          / Exploration
        </div>
      </div>

      <!-- Project items -->
      <div
        id="items"
        v-if="project"
      >
        <!-- Nb samples -->
        <div
          class="item nbSamples"
          title="Number of samples"
        >
          <inline-svg :src="require('@/assets/svg/data.svg')" />
          {{ project.nbSamples }} samples
        </div>
      </div>
    </div>

    <!-- Controls & date -->
    <div id="right">
      <!-- Dates -->
      <div
        id="dates"
        v-if="project && (project.creationDate || project.updateDate)"
      >
        <span
          v-if="project.creationDate"
          :title="$services.timeStampToDate(project.creationDate)"
        >
          Created {{ $services.prettyTimeStamp(project.creationDate) }}
        </span>
        <span
          v-if="project.updateDate"
          :title="$services.timeStampToDate(project.updateDate)"
        >
          Updated {{ $services.prettyTimeStamp(project.updateDate) }}
        </span>
      </div>

      <div id="buttonsTop">
        <!-- Refresh btn -->
        <button
          id="refresh"
          class="warning"
          @click="$emit('refresh')"
        >
          <inline-svg
            :src="require('../../../assets/svg/update.svg')"
            width="10"
            height="10"
          />
          Refresh
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: { project: { type: Object } },
  emits: ["settings", "refresh", "deleteProject"],
  data: () => {
    return {};
  },
  methods: {
    backToProjects() {
      this.$router.push({
        name: "frontPage",
      });
    },
    backToProject() {
      this.$router.push({
        name: "project",
        params: {
          dataProviderId: this.$store.state.ProjectPage.dataProviderId,
          projectId: this.project.id,
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
#Header {
  height: 60px;
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 50px;

  background-color: var(--greyLight);
  border-bottom: var(--greyDark) 2px solid;

  #left {
    display: flex;
    align-items: center;
    gap: 20px;

    #logoAndName {
      display: flex;
      align-items: center;
      gap: 10px;

      #debiaiLogo {
        margin: 5px 10px 0px 15px;
        cursor: pointer;
      }

      #projectName {
        font-size: 18px;
        font-weight: bold;

        a {
          cursor: pointer;
          text-decoration: none;

          &:hover {
            text-decoration: underline;
          }
        }
      }
    }

    #items {
      display: flex;
      flex-direction: row;
      align-items: center;
      color: var(--fontColorLight);
      gap: 20px;
      padding-left: 30px;

      svg {
        width: 15px;
        height: 15px;
        fill: var(--fontColorLight);
      }
    }
  }
}

/* Right */
#right {
  display: flex;
  align-items: center;
  gap: 20px;

  #buttonsTop {
    display: flex;
    align-items: center;
    margin: 5px;

    #settings {
      width: 60px;
    }
  }
  #dates {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--fontColorLight);
    gap: 20px;
  }
}
</style>
