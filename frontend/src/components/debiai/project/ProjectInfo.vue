<template>
  <div id="ProjectInfo">
    <div id="left">
      <!-- DebiAI & project path -->
      <div id="title">
        <h1
          id="DebiAI"
          @click="$emit('backToProjects')"
        >
          <img
            src="../../../../src/assets/images/DebiAI.png"
            alt="DebiAI"
            height="48"
          />
        </h1>
        <div class="path">
          <transition name="fade">
            <span v-if="project">
              <span
                @click="$emit('backToProjects')"
                class="link"
                >Projects</span
              >
              /
              {{ project.id }}
            </span>
          </transition>
        </div>
      </div>

      <!-- Project name & items -->
      <transition name="fade">
        <div
          id="projectTitle"
          v-if="project"
        >
          <h1 id="name">{{ project.id }}</h1>

          <!-- ProjectItems -->
          <div id="items">
            <!-- Nb samples -->
            <div
              class="item nbSamples"
              title="Number of samples"
            >
              <inline-svg
                :src="require('../../../assets/svg/data.svg')"
                width="25"
                height="25"
                fill="white"
              />
              {{ project.nbSamples }} samples
            </div>

            <!-- Nb selections -->
            <div
              class="item nbSelections"
              title="Project selections"
            >
              <inline-svg
                :src="require('../../../assets/svg/loop.svg')"
                width="25"
                height="25"
                fill="white"
              />
              {{ project.nbSelections }} selections
            </div>

            <!-- Nb models -->
            <div
              class="item nbModel"
              title="Model added to the project"
            >
              <inline-svg
                :src="require('../../../assets/svg/gear.svg')"
                width="25"
                height="25"
                fill="white"
              />
              {{ project.nbModels }} models
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- Controls & date -->
    <div id="right">
      <div id="btnsTop">
        <!-- Setting btn -->
        <button
          id="settings"
          @click="$emit('settings')"
        >
          <inline-svg
            :src="require('../../../assets/svg/settings.svg')"
            width="15"
            height="15"
            fill="white"
          />
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

      <transition name="fade">
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
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectInfo",
  props: { project: { type: Object } },
};
</script>

<style scoped>
#ProjectInfo {
  display: grid;
  grid-template-columns: 3fr 1fr;
  grid-template-rows: 1fr;
  grid-auto-flow: row;
  grid-template-areas: "left right";
  background-color: var(--primary);
  border-bottom: solid 5px var(--primaryDark);
  color: white;
}

#left {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 1.5fr 1fr;
  grid-auto-columns: 1fr;
  gap: 0px 0px;
  grid-auto-flow: row;
  grid-template-areas:
    "title"
    "name";
  grid-area: left;
  padding: 10px 0 20px 20px;
}

/* Title */
#title {
  display: grid;
  grid-template-columns: 0fr 1fr;
  grid-template-rows: 1fr;
  gap: 0px 0px;
  grid-auto-flow: row;
  grid-template-areas: "DebiAI path";
  grid-area: title;
}

#DebiAI {
  grid-area: DebiAI;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.path {
  grid-area: path;
  padding: 15px;
  display: flex;
  align-items: center;
}

.path .link {
  cursor: pointer;
  text-decoration: underline;
}

/* Project title */
#projectTitle {
  display: flex;
}

#name {
  text-decoration: underline;
  font-weight: normal;
}

#items {
  grid-area: items;
  display: flex;
  font-size: 1.2em;
  opacity: 0.8;
}

.item {
  padding-left: 2vw;
}

/* Right */
#right {
  display: flex;
  flex-direction: column;
  padding: 10px 20px 0 0;
}

#btnsTop {
  display: flex;
  margin: 5px;
}
#settings {
  flex: 0.4;
}

#delete {
  flex: 0.8;
}

#refresh {
  flex: 1;
}

#dates {
  grid-area: dates;
  display: flex;
  justify-content: space-between;
  align-items: center;
  opacity: 0.8;
}
</style>
