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
    </div>

    <!-- Controls & date -->
    <div id="right"></div>
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
  position: fixed;
  top: 0px;
  z-index: 2;

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
        color: var(--fontColorLight);

        a {
          cursor: pointer;
          color: var(--fontColor);
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
