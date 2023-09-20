<template>
  <div
    id="Widget"
    class="item selectable"
    @click="$emit('add', widget)"
  >
    <!-- Widget configuration modal -->
    <modal
      v-if="displayConfigurations"
      @close="displayConfigurations = false"
    >
      <div
        id="configurationList"
        class="itemList"
      >
        <h3>
          Widget configurations
          <button
            @click="displayConfigurations = false"
            class="red"
          >
            Cancel
          </button>
        </h3>
        <WidgetConfList
          :widgetKey="widget.componentKey"
          :configurations="configurations"
          v-on:selected="
            (configuration) => {
              displayConfigurations = false;
              $emit('addWithConf', { widget, configuration });
            }
          "
          v-on:deleted="confDeleted()"
        />
      </div>
    </modal>

    <!-- Widget icon image -->
    <progressive-img
      :src="require(`@/components/debiai/dataAnalysis/widgets/${widget.componentKey}/icon.png`)"
      class="icon"
    />

    <div id="title">
      <h3 class="name">{{ widget.name }}</h3>
      <div class="description">{{ widget.description }}</div>
    </div>

    <!-- Configurations -->
    <button
      class="confBtn"
      v-if="nbConfigurations && nbConfigurations > 0"
      style="display: flex; align-items: center"
      title="Add this widget with a previously saved configuration"
      @click.stop
      @click="openConfigurations"
    >
      <inline-svg
        :src="require('@/assets/svg/save.svg')"
        width="16"
        height="16"
        style="margin-right: 5px"
      />
      {{ nbConfigurations }}
    </button>

    <!-- Documentation -->
    <button
      v-if="widget.documentationLink"
      class="docBtn"
      title="Widget online documentation"
      style="margin-right: 5px"
      @click.stop
      @click="openDocumentation"
    >
      ?
    </button>
  </div>
</template>

<script>
import WidgetConfList from "../widgetConfiguration/WidgetConfList.vue";
import Vue from "vue";
import VueProgressiveImage from "vue-progressive-image";

Vue.use(VueProgressiveImage);

export default {
  components: { WidgetConfList },
  props: {
    widget: { required: true, type: Object },
    nbConfigurations: { type: Number, default: 0 },
  },
  data() {
    return {
      description: "",
      configurations: [], // [{ id, name, description, configuration, projectId, dataProviderId, creatinDate }]
      displayConfigurations: false,
    };
  },
  methods: {
    openConfigurations() {
      this.$emit("selected");
      this.getConfigurations().then(() => {
        if (this.configurations.length > 0)
          this.displayConfigurations = !this.displayConfigurations;
      });
    },
    async getConfigurations() {
      this.configurations = [];

      // Load widget configurations
      this.configurations = await this.$backendDialog.getWidgetConfigurations(
        this.widget.componentKey
      );
    },
    openDocumentation() {
      window.open(this.widget.documentationLink, "_blank");
    },
    confDeleted() {
      this.getConfigurations();
      this.$emit("confDeleted");
    },
  },
};
</script>

<style lang="scss" scoped>
#Widget {
  display: flex;
  flex-direction: row;
  gap: 5px;
}

.icon {
  width: 50px;
  margin-right: 10px;
}

#title {
  flex: 1;
  display: flex;
  flex-direction: column;

  .name {
    font-weight: bold;
    text-align: left;
    padding: 2px;
    padding-top: 4px;
  }
  .description {
    text-align: left;
    color: var(--fontColorLight);
  }
}

#configurationList {
  display: flex;
  flex-direction: column;
  padding: 10px;
  width: 500px;

  h3 {
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.confBtn {
  background: transparent;
  border: none;
  &:hover {
    background-color: var(--greyDark);
  }
  opacity: 0.6;
  padding: 10px;
  border-radius: 5px;
}

.docBtn {
  background-color: transparent;
  border-radius: 100px;
  border: solid 1px var(--fontColorLight);
  width: 30px;
  height: 30px;
  opacity: 0;
  &:hover {
    background-color: var(--greyDark);
  }
}

#Widget:hover .docBtn {
  opacity: 0.6;
}
</style>
