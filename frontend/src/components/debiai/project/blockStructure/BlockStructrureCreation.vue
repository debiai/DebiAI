<template>
  <div id="BlockStructrureCreation">
    <!-- New block level Modal -->
    <Modal v-show="addingBlockLevel">
      <form v-on:submit.prevent>
        <h3>New block level</h3>
        <input
          ref="newBlockLevelname"
          v-model="newBLname"
          placeholder="Block level name"
        />
        <br />
        <button type="submit" @click="createBlockLevel">Add</button>
        <button class="red" @click="addingBlockLevel = false">Cancel</button>
      </form>
    </Modal>

    <!-- New block level Modal -->
    <Modal v-show="remaneBlockLevel">
      <form v-on:submit.prevent>
        <h3>Rename block level</h3>
        <input
          ref="newBlockLevelname"
          v-model="renamedName"
          placeholder="Block level name"
        />
        <br />
        <button type="submit" @click="renameBlockName(renamedName)">
          Rename
        </button>
        <button class="red" @click="remaneBlockLevel = false">Cancel</button>
      </form>
    </Modal>

    <!-- New category Modal -->
    <Modal v-show="addingBlockLevelKey">
      <form v-on:submit.prevent>
        <h3>New {{ keyCategory }}</h3>
        <input
          ref="newBlockLevelkeyname"
          v-model="blKeyName"
          placeholder="Key name"
        />
        <select v-model="blKeyType">
          <option>String</option>
          <option>Interger</option>
          <option>Float</option>
          <option>Boolean</option>
        </select>
        <br />Default value :
        <input
          :type="getInputFromType(blKeyType)"
          v-model="blKeyDefault"
          step="any"
          :placeholder="blKeyType"
        />
        <br />
        <button type="submit" @click="createBlockLevelKey">Add</button>
        <button class="red" @click="addingBlockLevelKey = false">Cancel</button>
      </form>
    </Modal>

    <div id="top">
      <button v-if="editMode" @click="save">Save</button>
    </div>
    <div id="blockLevels">
      <div class="BlockLevelSegment" v-for="(bl, i) in blockLevels" :key="i">
        <button
          v-if="editMode"
          @click="addBlockLevel(i)"
          title="Add a block level"
        >
          +
        </button>
        <div class="blockLevel">
          <div class="blockLevelTop">
            <div class="blockLevelTitle">
              <button
                class="info"
                v-if="editMode"
                @click="openRenameBlockName(i, bl.name)"
              >
                {{ bl.name }}
              </button>
              <span v-else>{{ bl.name }}</span>
            </div>
            <button
              v-if="editMode"
              class="red deleteBtn bl"
              title="Remove block level"
              @click="removeBlockLevel(i)"
            ></button>
          </div>
          <div class="keyListList">
            <div class="keyList" v-for="type in types" :key="type">
              <div v-if="type in bl">
                <div v-if="editMode || (!editMode && bl[type].length > 0)">
                  <button v-if="editMode" @click="addBlockLevelkey(i, type)">
                    Add {{ type }}
                  </button>
                  <strong v-else>{{ type }}</strong>
                  <div v-for="(k, j) in bl[type]" :key="k.name" class="key">
                    <div class="keyName">{{ k.name }}</div>
                    <div class="keyType" :title="'Default : ' + k.default">
                      {{ k.type }}
                    </div>
                    <button
                      v-if="editMode"
                      class="red deleteBtn k"
                      title="Remove key"
                      @click="removeKey(i, type, j)"
                    ></button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <button
        v-if="editMode"
        @click="addBlockLevel(blockLevels.length)"
        title="Add a block level"
      >
        +
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlockStructrureCreation",
  components: {},
  props: {
    projectId: { type: String, required: true },
  },
  data: () => {
    return {
      types: ["groundTruth", "contexts", "inputs", "others"],
      blockLevels: [],
      editMode: false,

      // Add block level
      addingBlockLevel: false,
      newBlockLevelPos: 0,
      newBLname: "",

      // Rename block level
      remaneBlockLevel: false,
      renamedName: "",

      // Add block level key
      addingBlockLevelKey: false,
      selectedBlockLevelPos: false,
      keyCategory: "",
      blKeyName: "",
      blKeyType: "String",
      blKeyDefault: null,
    };
  },
  created() {
    this.blockLevelInfo = this.$store.state.ProjectPage.blockLevels;
    console.log(this.blockLevelInfo);
    if (!this.blockLevelInfo) {
      this.blockLevels = [
        {
          name: "First Block",
        },
        {
          name: "Second Block",
        },
        {
          name: "Sample",
        },
      ];
      this.editMode = true;
      this.blockLevels.forEach((blockLevel) => {
        this.types.forEach((type) => {
          blockLevel[type] = [];
        });
      });
    } else this.blockLevels = this.blockLevelInfo;
  },
  methods: {
    addBlockLevel: function (pos) {
      this.addingBlockLevel = true;
      this.newBlockLevelPos = pos;
      this.$nextTick(() => {
        this.$refs.newBlockLevelname.focus();
      });
    },
    createBlockLevel: function () {
      if (!this.nameOk(this.newBLname)) return;
      let newLevel = {
        name: this.newBLname,
        groundTruth: [],
        contexts: [],
        inputs: [],
        others: [],
      };
      this.newBLname = "";
      this.addingBlockLevel = false;
      this.blockLevels.splice(this.newBlockLevelPos, 0, newLevel);
    },
    removeBlockLevel: function (pos) {
      this.blockLevels.splice(pos, 1);
    },

    nameOk(name) {
      if (name == "") {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Block level name must not be empty",
        });
        return false;
      }
      if (name.length > 40) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Block level name is too long",
        });
        return false;
      }
      if (name.includes("/")) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Block level name got invalid caracters",
        });
        return false;
      }
      return true;
    },

    // Rename block level
    openRenameBlockName(blockId, name) {
      this.renamedName = name;
      this.renamedBlockId = blockId;
      this.remaneBlockLevel = true;
    },
    renameBlockName(newName) {
      if (!this.nameOk(newName)) return;

      this.remaneBlockLevel = false;
      this.blockLevels[this.renamedBlockId].name = newName;
    },

    // block level key
    addBlockLevelkey: function (blockLevelPos, category) {
      this.keyCategory = category;
      this.selectedBlockLevelPos = blockLevelPos;
      this.addingBlockLevelKey = true;
      this.$nextTick(() => {
        this.$refs.newBlockLevelkeyname.focus();
      });
    },
    createBlockLevelKey: function () {
      if (this.blKeyName == "") {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: this.keyCategory + " key name must not be empty",
        });
        return;
      }
      if (this.blKeyName.length > 40) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: this.keyCategory + " key name is too long",
        });
        return;
      }
      if (
        this.blockLevels[this.selectedBlockLevelPos][this.keyCategory].find(
          (bl) => bl.name == this.blKeyName
        )
      ) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: this.keyCategory + " Keys names are unique",
        });
        return;
      }
      let newKey = {
        name: this.blKeyName,
        type: this.blKeyType,
        default: this.blKeyDefault,
      };
      this.blKeyName = "";
      this.blKeyDefault = "";
      this.addingBlockLevelKey = false;
      this.blockLevels[this.selectedBlockLevelPos][this.keyCategory].push(
        newKey
      );
    },
    removeKey: function (blockLevelPos, category, keyPos) {
      this.blockLevels[blockLevelPos][category].splice(keyPos, 1);
    },
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

    // Save
    save: function () {
      if (this.blockLevels.length == 0) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "At least one block level is needed",
        });
        return;
      }

      this.$backendDialog
        .saveProjectlevels(this.projectId, this.blockLevels)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "The project block levels have been saved",
          });

          this.$emit("create", this.blockLevels);
        });
    },
  },
  computed: {},
};
</script>

<style scoped>
#BlockStructrureCreation {
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
