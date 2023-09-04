<template>
  <div
    id="ColorTag"
    :class="colorTagClass"
    :title="title"
  >
    <div v-if="color === 'green'">✔</div>
    <div v-if="color === 'blue'">i</div>
    <div v-if="color === 'red'">✖</div>
    <div v-if="color === 'yellow'">&#x26A0;</div>
  </div>
</template>

<script>
export default {
  name: "ColorTag",
  props: {
    color: {
      type: String, // Blue, Red, Green, Yellow
    },
    title: {
      type: String,
      default: "",
    },
  },
  computed: {
    colorTagClass() {
      return `colorTag ${this.color}`;
    },
  },
};
</script>

<style lang="scss" scoped>
#ColorTag {
  width: 21px;
  height: 21px;

  display: flex;
  justify-content: center;
  align-items: center;

  border-radius: 50px;
  border: 1px solid;

  transition: all 0.2s;
  font-size: large;

  &.green {
    border-color: var(--success);
    color: var(--success);
  }
  &.blue {
    border-color: var(--blue);
    color: var(--blue);
    font-family: "Font Awesome 5 Free";
  }
  &.red {
    border-color: var(--danger);
    color: var(--danger);
  }
  &.yellow {
    border-color: var(--warning);
    color: var(--warning);
  }
}
</style>
