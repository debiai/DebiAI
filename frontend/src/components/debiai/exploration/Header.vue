<template>
  <div id="Header">
    <div id="left">
      <!-- DebiAI Logo and project name -->
      <div id="logoAndName">
        <!-- DebiAI Logo -->
        <a @click="$emit('backToProjects')">
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
          <a @click="$emit('backToProjects')"> Projects </a>
          / <span style="color: var(--fontColorLight)"> {{ project.id }} / Exploration</span>
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

        <!-- Nb selections -->
        <div
          class="item nbSelections"
          title="Project selections"
        >
          <inline-svg :src="require('@/assets/svg/loop.svg')" />
          {{ project.nbSelections }} selections
        </div>

        <!-- Nb models -->
        <div
          class="item nbModel"
          title="Model added to the project"
        >
          <inline-svg :src="require('@/assets/svg/gear.svg')" />
          {{ project.nbModels }} models
        </div>
      </div>
    </div>

    <!-- Controls & date -->
    <div id="right">
      <!-- Dates -->
      <div
        id="dates"
        v-if="project && project.creationDate && project.updateDate"
      >
        <span :title="$services.timeStampToDate(project.creationDate)">
          Created {{ $services.prettyTimeStamp(project.creationDate) }}
        </span>
        <span :title="$services.timeStampToDate(project.updateDate)">
          Updated {{ $services.prettyTimeStamp(project.updateDate) }}
        </span>
      </div>

      <div id="topButtons">
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

  #topButtons {
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
