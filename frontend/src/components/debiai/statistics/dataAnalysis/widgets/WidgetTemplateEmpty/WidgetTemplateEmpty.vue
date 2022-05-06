<template>
  <div id="WidgetTemplate" class="dataVisualisationWidget">
    Empty Widget Template
  </div>
</template>

<script>
export default {
  components: {
  },
  data() {
    return {
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
  },
  mounted() {
  },
  methods: {
  },
  computed: {
  },
  watch: {
  },
};
</script>

<style scoped>
#WidgetTemplate {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>