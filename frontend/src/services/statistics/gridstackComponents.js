import services from "../services"

// Default components layout
const defaultLayout = [
  {
    key: "ParallelCoordinate",
    x: 0,
    y: 0,
    width: 12,
    height: 5,
  },
  {
    key: "PointPlot",
    x: 6,
    y: 5,
    width: 6,
    height: 5,
  },
  {
    key: "RepartitionPlot",
    x: 0,
    y: 5,
    width: 6,
    height: 5,
  }
];

// Loading the visualization components
const BASE_LAYOUT = {
  x: 0,
  y: 0,
  width: 5,
  minWidth: 2,
  maxWidth: 15,
  height: 4,
  minHeight: 2,
  maxHeight: 15,
}

const availableWidgetsConfiguration = {}
// Load every json configuration extension in the widgets folder
const availableWidgets = require.context(
  "../../components/debiai/statistics/dataAnalysis/widgets",
  true,
  /configuration\.json$/i
);

availableWidgets.keys().forEach((componentFilePath) => {
  // Get the component id from the file name
  const componentKey = componentFilePath.split("/")[1];
  try {
    const configuration = require("../../components/debiai/statistics/dataAnalysis/widgets/" +
      componentKey + "/configuration.json");

    // Check configuration
    let widgetName = configuration.name || componentKey;
    let widgetSimple = configuration.simple || false;

    let widgetLayout
    if ('layout' in configuration) {
      widgetLayout = { ...BASE_LAYOUT, ...configuration.layout };
    } else {
      widgetLayout = { ...BASE_LAYOUT };
    }

    // Save the component configuration
    availableWidgetsConfiguration[componentKey] = {
      name: widgetName,
      simple: widgetSimple,
      key: componentKey,
      layout: widgetLayout,
    }
  } catch (e) {
    console.log(e);
    console.warn("Error loading widget : " + componentKey + " configuration");
  }
})

function createWidget(widgetKey) {
  // A uuid is generated for the widget
  const widget = {
    ...availableWidgetsConfiguration[widgetKey],
    id: services.uuid(),
  };
  return widget;
}

function getAvailableWidgets() {
  let widgetList = Object.keys(availableWidgetsConfiguration).map((widgetKey) => {
    return {
      componentKey: availableWidgetsConfiguration[widgetKey].key,
      componentName: availableWidgetsConfiguration[widgetKey].name,
     };
  })
  return widgetList;
}


export default {
  defaultLayout,
  createWidget,
  getAvailableWidgets
}
