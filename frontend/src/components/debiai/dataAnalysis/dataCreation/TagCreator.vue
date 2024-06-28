<template>
  <div id="TagCreator">
    <h2>Tag the selected values</h2>
    <form
      v-on:submit.prevent
      class="dataGroup"
    >
      <!-- createdTags -->
      <!-- Selected samples -->
      <div class="data">
        <span class="name"> Selected samples </span>
        <span class="value"> {{ data.selectedData.length }} / {{ data.nbLines }} </span>
      </div>
      <div class="data">
        <span class="name"> Tag name </span>
        <span class="value">
          <input
            type="text"
            v-model="tagName"
            style="flex: 2"
          />
          <select
            v-model="tagName"
            v-if="taggedColumns.length"
            title="Complete an existing tag column"
          >
            <option
              v-for="taggedColName in taggedColumns"
              :key="taggedColName"
            >
              {{ taggedColName }}
            </option>
          </select>
        </span>
      </div>
      <div class="data">
        <span class="name"> Tag value : </span>
        <span class="value">
          <input
            type="number"
            v-model="tagValue"
          />
        </span>
      </div>
    </form>
    <span>
      <button
        type="submit"
        @click="create"
        :disabled="!tagNameOk || !tagValueOk"
      >
        {{ createdTags.includes(tagName) ? "Update" : "Create" }} the tag
      </button>
      <button
        @click="$emit('cancel')"
        class="red"
      >
        Cancel
      </button>
    </span>
  </div>
</template>

<script>
export default {
  name: "TagCreator",
  data() {
    return {
      tagName: "My tag",
      tagValue: 1,
      taggedColumns: [],
    };
  },
  props: {
    data: { type: Object, required: true },
  },
  created() {
    // Load the tagged columns name
    this.taggedColumns = this.data.columns.filter((c) => c.category == "tag").map((c) => c.label);
  },
  methods: {
    create() {
      let tagValue = parseInt(this.tagValue);

      // Check if tag already exist
      const column = this.data.getColumnByLabelAndCategory(this.tagName, "tag");
      if (column) {
        const values = [...column.values];
        this.data.selectedData.forEach((i) => (values[i] = tagValue));
        column.updateValues(values);

        this.$store.commit("sendMessage", {
          title: "success",
          msg: "Tag updated successfully",
        });
      } else {
        // Create new tag
        const values = new Array(this.data.nbLines).fill(0);
        this.data.selectedData.forEach((i) => (values[i] = tagValue));
        this.data.addColumn({
          label: this.tagName,
          values: values,
          category: "tag",
        });

        this.$store.commit("sendMessage", {
          title: "success",
          msg: "Tag created successfully",
        });
      }
      this.$emit("cancel");
    },
  },
  computed: {
    createdTags() {
      return this.data.columns.filter((c) => c.category === "tag").map((c) => c.label);
    },
    tagNameOk() {
      return (
        this.tagName.length >= 1 &&
        !this.data.columns.some((c) => c.label === this.tagName && c.category !== "tag")
      );
    },
    tagValueOk() {
      return this.tagValue !== "";
    },
  },
};
</script>

<style scoped>
.errorMsg {
  color: red;
}

.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 4px;
}
.dataGroup .value {
  flex: 1;
}
</style>
