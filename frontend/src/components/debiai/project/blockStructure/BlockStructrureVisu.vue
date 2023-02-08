<template>
  <div id="BlockStructrureVisu">
    <div id="blockLevels">
      <div class="BlockLevelSegment" v-for="(bl, i) in blockLevels" :key="i">
        <div class="blockLevel">
          <div class="blockLevelTop">
            <div class="blockLevelTitle">
              <span>{{ bl.name }}</span>
            </div>
          </div>
          <div class="keyListList">
            <div class="keyList" v-for="type in types" :key="type">
              <div v-if="type in bl">
                <div v-if="bl[type].length > 0">
                  <strong>{{ type }}</strong>
                  <div v-for="k in bl[type]" :key="k.name" class="key">
                    <div class="keyName">{{ k.name }}</div>
                    <div class="keyType" :title="'Default : ' + k.default">
                      {{ k.type }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlockStructrureVisu",
  components: {},
  data: () => {
    return {
      types: ["groundTruth", "contexts", "inputs", "others"],
      blockLevels: [],
    };
  },
  created() {
    this.blockLevelInfo = this.$store.state.ProjectPage.blockLevels;
    if (!this.blockLevelInfo) this.blockLevels = [];
    else this.blockLevels = this.blockLevelInfo;
  },
  methods: {
    getInputFromType: function (type) {
      if (type == "String") {
        return "text";
      }
      if (type == "Interger" || type == "Float") {
        return "number";
      }
      if (type == "Boolean") {
        return "checkbox";
      }
    },
  },
  computed: {},
};
</script>

<style scoped>
#BlockStructrureVisu {
  text-align: center;
  border-radius: 10px;
}
#top {
  display: flex;
  align-items: center;
  justify-content: center;
}
#top button {
  margin: 10px;
}
#blockLevels {
  display: flex;
  align-items: center;
  overflow: auto;
}
.BlockLevelSegment {
  display: flex;
  align-items: center;
}

#blockLevels > :first-child {
  margin-left: auto;
}
#blockLevels > :last-child {
  margin-right: auto;
}
/* BlockLevel */

.blockLevel {
  padding-top: 10px;
  padding-bottom: 10px;
  margin: 2px;
}
.blockLevelTop {
  display: flex;
  border: solid black 1px;

  border-radius: 10px 10px 0px 0px;

  padding: 3px 8px 3px 8px;
}
.blockLevelTitle {
  flex: 1;
}
button {
  padding: 5px;
  margin: 0px;
}
.deleteBtn {
  height: 14px;
  width: 14px;
  padding: 0;
  margin: 0;
  border-radius: 100%;
}
.deleteBtn.bl {
  margin: 5px;
}

/* Key List */
.keyListList {
  border: solid black 1px;
  border-top: 0px;
  border-radius: 0px 0px 10px 10px;
  min-height: 10px;
  display: flex;
}
.keyList {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  margin: 5px;
}

/* Key */
.key {
  display: flex;
  align-items: center;
  border-bottom: dotted 1px rgb(139, 139, 139);
}
.keyName {
  flex: 1;
  text-align: left;
  padding-left: 5px;
}
.keyType {
  cursor: pointer;
  margin: 1px;
  padding: 2px;
  border: solid gray 1px;
  border-radius: 5px;
}
.deleteBtn.k {
  margin: 2px;
}
</style>
