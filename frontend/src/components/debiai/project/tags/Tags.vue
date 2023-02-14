<template>
  <div id="Tags">
    <h2 class="aligned spaced">
      Tags
      <button
        class="warning"
        @click="loadTags"
      >
        Refresh
      </button>
    </h2>
    <!-- tag list -->
    <transition name="fade">
      <div
        id="tagList"
        class="itemList marged"
        v-if="tags"
      >
        <!-- tags -->
        <div
          class="tag item spaced"
          v-for="tag in tags"
          :key="tag.id"
        >
          <!-- name -->
          {{ tag.name }}
          <!-- Nb samples -->
          <div
            class="nbSamples"
            title="Number of samples"
          >
            <inline-svg
              :src="require('../../../../assets/svg/data.svg')"
              width="14"
              height="14"
            />
            {{ tag.nbSamples }}
          </div>
          <!-- Dates -->
          <div class="dates">
            <span
              class="date createdDate"
              :title="$services.timeStampToDate(tag.creationDate)"
            >
              Created {{ $services.prettyTimeStamp(tag.creationDate) }}
            </span>
            <br />
            <span
              class="date updatedDate"
              :title="$services.timeStampToDate(tag.updateDate)"
              v-if="tag.updateDate !== tag.creationDate"
            >
              Updated {{ $services.prettyTimeStamp(tag.updateDate) }}
            </span>
          </div>
          <button
            class="red"
            @click="deleteTag(tag.id)"
          >
            Delete
          </button>
        </div>
      </div>
    </transition>
    <!-- loading -->
    <div v-if="!tags">Loading tags</div>
    <div v-else-if="tags.length === 0">No tags</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tags: null,
    };
  },
  created() {
    // Load the tags
    this.loadTags();
  },
  methods: {
    loadTags() {
      this.tags = null;
      this.$backendDialog
        .getTags()
        .then((tags) => {
          this.tags = tags;
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't load the tags",
          });
        });
    },
    deleteTag(tagId) {
      this.$backendDialog
        .deleteTag(tagId)
        .then(() => {
          this.loadTags();
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Tag deleted successfully",
          });
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't delete the tag",
          });
        });
    },
  },
};
</script>

<style scoped></style>
