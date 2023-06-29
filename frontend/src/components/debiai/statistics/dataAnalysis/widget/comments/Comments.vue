<template>
  <div id="Comments">
    <!-- New comment modal -->
    <Modal
      v-if="newCommentModal"
      @close="newCommentModal = false"
    >
      <div id="newCommentModal">
        <!-- Title -->
        <h3 class="aligned spaced gapped">
          New comment
          <button
            class="red"
            @click="newCommentModal = false"
          >
            Close
          </button>
        </h3>
        <!-- Form -->
        <form @submit.prevent>
          <!-- Comment title -->
          <label> Comment title </label>
          <span class="value">
            <input
              type="text"
              v-model="newCommentTitle"
              style="flex: 1"
              placeholder="Comment title"
              @keydown.enter="addComment"
              ref="newCommentTitle"
            />
          </span>
          <!-- Comment description -->
          <label> Description </label>
          <span class="value">
            <textarea
              v-model="newCommentText"
              style="height: 50px; flex: 1"
              placeholder="Comment text, write your interpretation of this widget results here"
              @keydown.enter="addComment"
            />
          </span>

          <!-- Submit btn -->
          <button
            type="submit"
            @click="addComment"
          >
            Comment
          </button>
        </form>
      </div>
    </Modal>

    <!-- Comments title -->
    <h3
      class="aligned spaced gapped"
      id="title"
    >
      <span>
        <inline-svg
          :src="require('@/assets/svg/comment.svg')"
          width="18"
          height="18"
          style="margin-right: 3px"
        />
        Comments
        <documentation-block>
          This is the widget comments section, here you can add comments to the widget. This can be
          used to write down your interpretation of the widget results.
          <br />
          <br />
          The comment will we exported with the widget image/results when you export this analysis
          page.
          <br />
          <br />
          The comments are saved locally for now, so they will be lost if you refresh the page.
        </documentation-block>
      </span>

      <span>
        <button
          class="green"
          @click="newCommentModal = true"
        >
          New comment
        </button>
        <button
          class="red"
          @click="$emit('close')"
        >
          Close
        </button>
      </span>
    </h3>

    <!-- Comment list-->
    <div
      id="commentList"
      class="itemList"
    >
      <!-- <div
        id="noComments"
        v-if="comments.length === 0"
      >
        <h3>No comments yet</h3>
      </div> -->

      <transition-group name="scale">
        <div
          class="comment item"
          v-for="comment in comments"
          :key="comment.id"
        >
          <h4 class="commentTitle">
            <inline-svg
              :src="require('@/assets/svg/comment.svg')"
              width="13"
              height="13"
              style="margin-right: 3px"
            />
            {{ comment.title }}
          </h4>
          <p class="text">{{ comment.text }}</p>

          <button
            class="white"
            @click="deleteComment(comment.id)"
            title="Delete comment"
          >
            <inline-svg
              :src="require('@/assets/svg/close.svg')"
              width="10"
              height="10"
            />
          </button>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    comments: { type: Array, required: true },
    // {
    //   id: "id",
    //   title: "title",
    //   text: "test",
    // },
  },
  data() {
    return {
      // New comment
      newCommentModal: false,
      newCommentTitle: "",
      newCommentText: "",
    };
  },
  methods: {
    addComment() {
      this.$emit("addComment", {
        title: this.newCommentTitle,
        text: this.newCommentText,
      });
      this.newCommentModal = false;
    },
    deleteComment(commentId) {
      this.$emit("removeComment", commentId);
    },
  },
  watch: {
    newCommentModal(val) {
      if (val) {
        this.$nextTick(() => {
          this.$refs.newCommentTitle.focus();
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#Comments {
  border-top: 1px solid #ccc;
  margin: 20px;
  padding-top: 10px;

  #title {
    padding-bottom: 10px;

    span {
      display: flex;
      align-items: center;
      gap: 5px;
    }
  }

  #commentList {
    overflow: auto;

    .comment {
      display: flex;
      gap: 30px;
      padding: 0px;
      align-items: center;

      .commentTitle {
        text-align: left;
        word-break: break-all;
        min-width: 140px;
      }
      .text {
        text-align: left;
        word-break: break-all;
        white-space: pre-wrap;
      }

      button {
        margin-left: auto;
      }
    }
  }
}

#newCommentModal {
  form {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;

    input,
    textarea {
      flex: 1;
      margin: 10px;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      transition: border-color 0.2s;
      width: 350px;
    }

    button {
      align-self: flex-end;
    }
  }
}
</style>
