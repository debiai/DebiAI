<template>
  <div id="ObjectCreator">
    <div v-for="(value, name) in object" :key="name" class="keyRow">
      {{name}}:
      <input type="text" placeholder="Value" v-model="object[name]" />
      <button class="red" @click="removeKey(name)">Rem</button>
    </div>

    <form class="keyRow" v-on:submit.prevent>
      <input type="text" placeholder="Key name" v-model="newKeyName" />
      <button type="submit" @click="addKey">Add key</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "ObjectCreator",
  props: {
    object : {type: Object, required: true}
  },
  data: () => {
    return {
      newKeyName: ""
    };
  },
  methods: {
    addKey: function() {
      if (this.newKeyName == "") {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Key name must not be null"
        });
        return;
      }
      if (this.object[this.newKeyName] !== undefined) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Key name are unique"
        });
        return;
      }
      this.object[this.newKeyName] = null;
      this.$emit("objUpdate", this.object)
      this.$forceUpdate();
    },
    removeKey: function(name) {
      delete this.object[name];
      this.$emit("objUpdate", this.object)
      this.$forceUpdate();
    }
  },
  computed: {}
};
</script>

<style scoped>
#ObjectCreator {
  display: flex;
  flex-direction: column;
  border: solid black 1px;
  padding: 5px;
  border-radius: 5px;
}
.keyRow {
  padding: 2px;

}
</style>
