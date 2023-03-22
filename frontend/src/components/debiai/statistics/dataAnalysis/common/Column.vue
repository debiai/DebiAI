<template>
  <div id="column">
    <!-- Label display -->
    <button
      v-if="column.type !== undefined && !disabled"
      :class="selected ? 'label selected' : 'label'"
      @click="select"
      :title="selected ? 'Unselect ' + column.label : 'Select ' + column.label"
    >
      {{ column.label }}
    </button>
    <div
      v-else-if="column.type == undefined"
      class="label disabled"
    >
      {{ column.label }}
    </div>
    <div
      v-else
      class="label"
    >
      {{ column.label }}
    </div>

    <!-- Number of uniques values display -->
    <div
      v-if="disabled || (!reduced && (!colorSelection || column.type == undefined))"
      :class="selectedAsColor ? 'nbOccu color' : 'nbOccu'"
      title="Number of uniques values"
    >
      {{ column.nbOccu }}
    </div>
    <button
      v-else-if="!reduced"
      :class="selectedAsColor ? 'nbOccu color btn' : 'nbOccu btn'"
      title="Number of uniques values
Click to set column as the main color"
      @click="selectAsColor"
    >
      {{ column.nbOccu }}
    </button>

    <!-- Type display -->
    <div
      :class="'type ' + column.typeText"
      title="Column type"
    >
      {{ column.typeText }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    column: { type: Object, required: true },
    selected: { type: Boolean, default: true },
    reduced: { type: Boolean, default: false },
    colorSelection: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
  },
  methods: {
    select() {
      this.$emit("selected", this.column.index);
    },
    selectAsColor() {
      this.$store.commit("setColoredColumnIndex", this.column.index);
    },
  },
  computed: {
    selectedAsColor: function () {
      return this.$store.state.SatisticalAnasysis.coloredColumnIndex == this.column.index;
    },
  },
};
</script>

<style scoped>
#column {
  display: flex;
  background-color: rgb(228, 222, 222);
  border-radius: 10px;
  margin: 5px;
  transition: all 0.3s;
}
#column:hover {
  background-color: rgb(214, 213, 213);
}

/* Label  */

#column .label {
  width: 140px;
  justify-content: center;
  align-items: center;

  background-color: var(--dark);
  border-color: var(--darkDark);
  color: white;
  border-radius: 10px 0px 0px 10px;
  font-weight: bold;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: "-";
  /* transition: all 0.1s; */
}
#column button.selected {
  background-color: var(--primary);
  border-color: var(--primaryDark);
}
#column button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 3px 3px rgba(255, 255, 255, 0.2);
}
#column button:active {
  background-color: var(--primaryDark);
  border: 0;
}

#column .disabled {
  cursor: not-allowed;
  width: 120px;
  border-bottom: none;

  background-color: var(--undefined);
  color: rgb(27, 27, 27);
  border-radius: 10px 0px 0px 10px;
  font-weight: bold;
  padding: 10px;
}

/* Occu */
#column .nbOccu {
  min-width: 40px;
  padding: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #929292;
  color: #fff;
  font-weight: bold;
}
#column .nbOccu.btn {
  margin: 2px;
  border-color: #616161;
}

/* Color Animation */

#column .nbOccu.color {
  background: rgb(253, 29, 29);
  background: linear-gradient(
    135deg,
    rgba(253, 29, 29, 1) 0%,
    rgba(252, 147, 56, 1) 40%,
    rgba(128, 166, 122, 1) 51%,
    rgba(103, 156, 171, 1) 60%,
    rgba(69, 71, 252, 1) 100%
  );
}

@-webkit-keyframes AnimationName {
  0% {
    background-position: 46% 0%;
  }
  50% {
    background-position: 55% 100%;
  }
  100% {
    background-position: 46% 0%;
  }
}
@-moz-keyframes AnimationName {
  0% {
    background-position: 46% 0%;
  }
  50% {
    background-position: 55% 100%;
  }
  100% {
    background-position: 46% 0%;
  }
}
@keyframes AnimationName {
  0% {
    background-position: 46% 0%;
  }
  50% {
    background-position: 55% 100%;
  }
  100% {
    background-position: 46% 0%;
  }
}

/* // Type  */
#column .type {
  display: flex;
  justify-content: center;
  align-items: center;

  margin: 7px;
  padding-left: 7px;
  padding-right: 7px;

  border-radius: 10px;
  color: black;
}
#column .type.Num {
  background: var(--number);
}
#column .type.Class {
  background: var(--class);
}
#column .type.undefined {
  background: var(--undefined);
}
</style>
