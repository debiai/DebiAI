<template>
  <div id="ObjectCreator">
    <div v-for="key in objectStructure" :key="key.name" class="keyRow">
      <div class="name">{{key.name}}</div>
      <div class="unit">({{key.type}})</div>
      <input
        v-if="key.type == 'String'"
        type="text"
        placeholder="Text"
        v-model="object[key.name]"
        required
      />
      <input
        v-if="key.type == 'Interger'"
        type="number"
        placeholder="Number"
        v-model="object[key.name]"
        required
      />
      <input
        v-if="key.type == 'Float'"
        type="number"
        step="any"
        placeholder="Number"
        v-model="object[key.name]"
        required
      />
      <input
        v-if="key.type == 'Boolean'"
        type="checkbox"
        step="0.1"
        placeholder="Number"
        v-model="object[key.name]"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "ObjectCreator",
  props: {
    objectStructure: { type: Array, required: true },
    object: { type: Object, required: true }
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
      this.$emit("objUpdate", this.object);
      this.$forceUpdate();
    },
    removeKey: function(name) {
      delete this.object[name];
      this.$emit("objUpdate", this.object);
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
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.unit {
  color: gray;
}
</style>
