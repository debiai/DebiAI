import services from "../services";

// Default components layout
const defaultLayout = {
  layout: [
    {
      widgetKey: "ParallelCoordinate",
    },
    {
      widgetKey: "DistributionPlot",
      y: 6,
      width: 6,
      height: 4,
    },
    {
      widgetKey: "DistributionPlot",
      x: 6,
      y: 6,
      width: 6,
      height: 4,
    },
    {
      widgetKey: "PointPlot",
      y: 10,
    },
  ],
};

// Loading the visualization components
const BASE_LAYOUT = {
  x: 0,
  y: 0,
  width: 12,
  minWidth: 2,
  maxWidth: 15,
  height: 6,
  minHeight: 2,
  maxHeight: 15,
};

// Apply Base layout to default layout
defaultLayout.layout = defaultLayout.layout.map((widget) => {
  return { ...BASE_LAYOUT, ...widget };
});

const availableWidgetsConfiguration = {};
// Load every json configuration extension in the widgets folder
const availableWidgets = require.context(
  "../../components/debiai/dataAnalysis/widgets",
  true,
  /configuration\.json$/i
);

availableWidgets.keys().forEach((componentFilePath) => {
  // Get the component id from the file name
  const componentKey = componentFilePath.split("/")[1];
  try {
    const configuration = require("../../components/debiai/dataAnalysis/widgets/" +
      componentKey +
      "/configuration.json");

    // Check configuration
    if (configuration.display === false) return;

    let widgetName = configuration.name || componentKey;
    let widgetDescription = configuration.description || "";

    // Check if the widget has a layout configuration
    let widgetLayout;
    if ("layout" in configuration) {
      widgetLayout = { ...BASE_LAYOUT, ...configuration.layout };
    } else {
      widgetLayout = { ...BASE_LAYOUT };
    }

    // Check for categories
    let widgetCategories = [];
    if ("categories" in configuration) widgetCategories = configuration.categories;

    // Check for project types
    let widgetProjectTypes = [];
    if ("projectTypes" in configuration) widgetProjectTypes = configuration.projectTypes;

    // Check if the widget has a documentation link
    let widgetDocumentationLink = null;
    if ("documentationLink" in configuration)
      widgetDocumentationLink = configuration.documentationLink;

    // Save the component configuration
    availableWidgetsConfiguration[componentKey] = {
      name: widgetName,
      description: widgetDescription,
      widgetKey: componentKey,
      layout: widgetLayout,
      categories: widgetCategories,
      projectTypes: widgetProjectTypes,
      documentationLink: widgetDocumentationLink,
    };
  } catch (e) {
    console.log(e);
    console.warn("Error loading widget : " + componentKey + " configuration");
  }
});

function createWidget(widgetKey) {
  // A uuid is generated for the widget
  const widgetId = services.uuid();

  // Create a copy of the widget configuration
  const layoutCopy = { ...availableWidgetsConfiguration[widgetKey].layout };
  const copyConfiguration = { ...availableWidgetsConfiguration[widgetKey] };
  copyConfiguration.layout = layoutCopy;
  console.log(copyConfiguration);
  console.log(widgetId);
  console.log("test");
  return { ...copyConfiguration, id: widgetId };
}

function getAvailableWidgets() {
  // Return the list of available widgets with their configuration

  let widgetList = Object.keys(availableWidgetsConfiguration).map((widgetKey) => {
    return {
      componentKey: availableWidgetsConfiguration[widgetKey].widgetKey,
      name: availableWidgetsConfiguration[widgetKey].name,
      description: availableWidgetsConfiguration[widgetKey].description,
      categories: availableWidgetsConfiguration[widgetKey].categories,
      projectTypes: availableWidgetsConfiguration[widgetKey].projectTypes,
      documentationLink: availableWidgetsConfiguration[widgetKey].documentationLink,
    };
  });

  return widgetList;
}

function widgetExists(widgetKey) {
  return widgetKey in availableWidgetsConfiguration;
}

export default {
  defaultLayout,
  createWidget,
  getAvailableWidgets,
  widgetExists,
};
