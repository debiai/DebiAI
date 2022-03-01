<template>
  <div id="DocumentationBlock">
    <div id="questionMark">
      <b id="i">i</b>
      <p id="docBlock"><slot /></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "DocumentationBlock",
};
</script>

<style scoped>
#docBlock {
  position: absolute;
  padding: 20px;
  margin: 0px;
  border: dashed 1px var(--infoDark);
  border-radius: 10px;
  color: var(--infoDark);
  background-color: rgb(213, 251, 255);
  text-align: left;
  z-index: 10;
  visibility: hidden;
  opacity: 0;
  transition: visibility 0s, opacity 0.1s linear;
  font-size: initial;
  text-decoration: none;
  align-self: flex-start;
  font-weight: normal;
  box-shadow: 0px 0px 25px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}
#questionMark #i {
  margin: 0 7px 0 7px;
  cursor: pointer;
  border: solid 1px var(--infoDark);
  color: var(--infoDark);
  background-color: rgb(245, 254, 255);
  border-radius: 100%;
  width: 18px;
  height: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 3px;
  text-decoration: none;
  font-size: initial;
}
#questionMark:hover > #docBlock {
  visibility: visible;
  opacity: 1;
}
</style>