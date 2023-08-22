<template>
  <div id="CachePanel">
    <h3>
      <inline-svg
        :src="require('../../../../assets/svg/data.svg')"
        width="20"
        height="20"
      />
      <span> Cache </span>
      <documentation-block top>
        <h4>What is the cache?</h4>
        <p>
          The cache allows to avoid requesting the server for data that has already been requested.
        </p>
        <h4>How does it work?</h4>
        <p>
          When you request data from the server, the data is stored in your browser's cache. <br />
          If you request the same data again, the cache will be used instead of requesting the
          server.
        </p>
        <p>
          The cache is based on the project update date, if the project update date changes, the
          cache will be cleared.
        </p>
      </documentation-block>
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
      <div id="buttons">
        <button
          id="clearCache"
          @click="clearCache"
          :disabled="loading"
        >
          Clear cache
        </button>
        <button
          @click="getNbCacheItems"
          class="warning"
          title="Refresh cache info"
        >
          <inline-svg
            :src="require('@/assets/svg/update.svg')"
            width="15"
            height="15"
          />
        </button>
      </div>
    </div>
    <p
      v-else
      class="warning"
    >
      The project has no update date. <br />
      The cache will not be used.

      <documentation-block top>
        <h4>Why?</h4>
        <p>
          The cache is based on the project update date. <br />
          If we don't know when the project was updated, we can't know if the cache is up to date.
          If the project has no update date, the cache will not be used.
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
      nbCacheItems: null,
      updateDate: null,
      loading: false,
    };
  },
  mounted() {
    // We need to know the project update date to use the cache
    if (this.project.updateDate) {
      this.getNbCacheItems();

      // Check if the cache was previously disabled
      if (localStorage.getItem("useCache") === "false") this.useCache = false;
    }
  },
  methods: {
    getNbCacheItems() {
      this.nbCacheItems = null;
      this.updateDate = this.project.updateDate;
      cacheService.getNbSamples(this.updateDate).then((nb) => {
        this.nbCacheItems = nb;
      });
    },
    clearCache() {
      // Start request
      this.loading = true;
      const requestCode = this.$services.uuid();
      this.$store.commit("startRequest", {
        name: "Clearing the project cache",
        code: requestCode,
      });

      cacheService
        .resetDb()
        .then(() => {
          this.nbCacheItems = 0;
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Cache cleared",
          });
        })
        .catch((err) => {
          console.log(err);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Error while clearing cache",
          });
        })
        .finally(() => {
          this.$store.commit("endRequest", requestCode);
          this.loading = false;
        });
    },
  },
  computed: {},
  watch: {
    useCache: {
      handler: function (val) {
        localStorage.setItem("useCache", val);
        this.$store.commit("setUseCache", val);
      },
    },
  },
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

  h3 {
    display: flex;
    gap: 10px;
  }

  #content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    #buttons {
      display: flex;
      align-items: center;
      gap: 5px;

      button {
        height: 28px;
      }

      #clearCache {
        flex: 1;
      }
    }
  }
  .warning {
    display: flex;
    align-items: center;
    padding: 10px;
  }
}
</style>
