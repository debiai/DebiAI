// Util for exporting analysis results
// as a list of images and markdown report

const Plotly = require("plotly.js/dist/plotly");

const getAnalysisExport = async (widgets) => {
  // Get images from widgets
  const images = [];
  for (let i = 0; i < widgets.length; i++) {
    const widget = widgets[i];
    console.log(widget);
    const widgetId = widget.id;
    console.log(widgetId);

    // Get the widget div
    const widgetDiv = document.getElementById(widgetId);
    console.log(widgetDiv);
    console.log(widgetDiv.componentInstance);

    // if (widget.type == "plotly") {
    //   const img = await plotlyPlotToImage(widget.data);
    //   images.push(img);
    //   text.push(widget.description);
    // }
  }
};

/**
 * Exports a Plotly chart to a JPEG image file and downloads it.
 * @param {HTMLElement} plot - The Plotly chart to export.
 * @param {number} [width=400] - The desired width of the exported image.
 * @param {number} [height=300] - The desired height of the exported image.
 * @param {string} [filename="plot.jpeg"] - The desired filename of the downloaded image.
 * @returns {Promise<string>} - The URL of the generated image.
 */
export async function plotlyTImage(plot, width = 400, height = 300, filename = "plot.jpeg") {
  try {
    // Get plot pixel size
    const plotSize = plot.getBoundingClientRect();
    if (plotSize.width) width = plotSize.width;
    if (plotSize.height) height = plotSize.height;

    // Generate an image of the plot
    const imageUrl = await Plotly.toImage(plot, {
      format: "jpeg",
      width,
      height,
    });

    // Download the image
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = filename;
    link.click();

    return imageUrl;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to export Plotly chart to image.");
  }
}

export default getAnalysisExport;