<template>
  <div id="Header">
    <div id="left">
      <!-- DebiAI Logo and project name -->
      <div id="logoAndName">
        <!-- DebiAI Logo -->
        <a
          @click.exact="$emit('backToProjects')"
          @click.middle.exact="$emit('backToProjects', true)"
          @click.ctrl.exact="$emit('backToProjects', true)"
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
            @click.exact="$emit('backToProjects')"
            @click.middle.exact="$emit('backToProjects', true)"
            @click.ctrl.exact="$emit('backToProjects', true)"
          >
            Projects
          </a>
          / {{ project.name }}
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
          v-if="project.nbSamples !== undefined && project.nbSamples !== null"
        >
          <inline-svg :src="require('@/assets/svg/data.svg')" />
          {{ project.nbSamples }} samples
        </div>
        <div
          class="item nbSamples"
          title="Number of samples"
          v-else
        >
          <inline-svg :src="require('@/assets/svg/data.svg')" />
          ?
        </div>

        <!-- Nb selections -->
        <div
          class="item nbSelections"
          title="Project selections"
          v-if="project.nbSelections !== undefined && project.nbSelections !== null"
        >
          <inline-svg :src="require('@/assets/svg/loop.svg')" />
          {{ project.nbSelections }} selections
        </div>
        <div
          class="item nbSelections"
          title="Project selections"
          v-else
        >
          <inline-svg :src="require('@/assets/svg/loop.svg')" />
          ?
        </div>
        <!-- Nb models -->
        <div
          class="item nbModel"
          title="Model added to the project"
          v-if="project.nbModels !== undefined && project.nbModels !== null"
        >
          <inline-svg :src="require('@/assets/svg/gear.svg')" />
          {{ project.nbModels }} models
        </div>
        <div
          class="item nbModel"
          title="Model added to the project"
          v-else
        >
          <inline-svg :src="require('@/assets/svg/gear.svg')" />
          ?
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
        <!-- Setting btn -->
        <button
          id="settings"
          @click="$emit('settings')"
        >
          <inline-svg
            :src="require('../../../assets/svg/settings.svg')"
            width="12"
            height="12"
            fill="white"
          />
        </button>

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

        <!-- Delete btn -->
        <button
          id="delete"
          class="red"
          @click="$emit('deleteProject')"
          v-if="
            $store.state.ProjectPage.dataProviderInfo &&
            $store.state.ProjectPage.dataProviderInfo.canDelete &&
            $store.state.ProjectPage.dataProviderInfo.canDelete.projects
          "
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: { project: { type: Object } },
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
          color: var(--fontColorLight);
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
