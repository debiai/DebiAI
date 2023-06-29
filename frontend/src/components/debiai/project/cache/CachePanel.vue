<template>
  <div id="CachePanel">
    <h3>Cache</h3>

    <div id="useCache">
      Cache loaded dada:
      <input
        type="checkbox"
        v-model="useCache"
      />
    </div>

    <div id="nbCached">Number of cache items: {{ nbCacheItems }}</div>

    <button>Clear cache</button>
  </div>
</template>

<script>
export default {
  props: {},
  data: () => {
    return {
      useCache: true,
      nbCacheItems: 0,
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>
#CachePanel {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
