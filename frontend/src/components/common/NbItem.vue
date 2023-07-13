<!-- Nb items, Used in collapsible header and more -->
<template>
  <div class="nbItem">
    <!-- Nb selected -->
    <span class="nb blue">
      {{ nbSelected }}
    </span>
    <span> / </span>
    <span class="nb"> {{ nbTotal }} </span>
  </div>
</template>

<script>
export default {
  name: "NbItem",
  props: {
    nbSelected: { type: Number, default: 0 },
    nbTotal: { type: Number, default: 0 },
  },
};
</script>

<style scoped lang="scss">
.nbItem {
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 0.9em;
  color: #888;
  gap: 5px;

  .nb {
    background-color: #eee;
    border-radius: 6px;
    padding: 2px 4px;
    border: 2px solid #ccc;
    font-size: 0.9em;
    color: #888;

    &.blue {
      background-color: #cfe2ff;
      border-color: #4f89ca;
      color: #3b6595;
    }
  }
}
</style>
