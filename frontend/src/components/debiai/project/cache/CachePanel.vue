<template>
  <div id="CachePanel">
    <h3>
      <inline-svg
        :src="require('../../../../assets/svg/data.svg')"
        width="20"
        height="20"
      />
      <span> Cache </span>
    </h3>
    <div
      id="content"
      v-if="updateDate"
    >
      <div id="useCache">
        Enable project data cache:
        <input
          type="checkbox"
          v-model="useCache"
        />
      </div>

      <div id="nbCached">Project cached items: {{ nbCacheItems }}</div>
      <button>Clear cache</button>
    </div>
    <p
      v-else
      class="warning"
    >
      The project has no update date. <br />
      The cache will not be used.

      <documentation-block top followCursor>
        <h4>Why?</h4>
        <p>
          The cache is based on the project update date. <br />
          If we don't know when the project was updated, we can't know if the cache is up to date. If the project has no update date, the cache will not be used.
        </p>
      </documentation-block>
    </p>
  </div>
</template>

<script>
// import  from "../../../../services/cacheService"
import cacheService from "@/services/cacheService";

export default {
  props: {
    project: { type: Object, require: true },
  },
  data: () => {
    return {
      useCache: true,
      nbCacheItems: 0,
      updateDate: null,
    };
  },
  mounted() {
    if (this.project.updateDate) {
      this.updateDate = this.project.updateDate;
      cacheService.getNbSamples(this.updateDate).then((nb) => {
        console.log("nb samples", nb);
        this.nbCacheItems = nb;
      });
    }
  },
  methods: {},
  computed: {},
};
</script>

<style scoped lang="scss">
#CachePanel {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
  #content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .warning {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    margin: 3px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #ffc108;
    color: #181616;
  }
}
</style>
