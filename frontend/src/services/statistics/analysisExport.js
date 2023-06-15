// Util for exporting analysis results
// as a list of images and markdown report

const Plotly = require("plotly.js/dist/plotly");
const JSZip = require("jszip");
const FileSaver = require("file-saver");

export async function plotlyToImage(plot, width = 400, height = 300, filename = "plot.jpeg") {
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

    return imageUrl;
  } catch (error) {
    console.log(error);
    return null;
  }
}

function getImageName(index, widget) {
  const name = widget.name.replace(/ /g, "-");
  const widgetName = widget.widget.replace(/ /g, "-");
  return `${index + 1}_${widgetName}_${name}.jpeg`;
}

export async function getAnalysisExport(widgetResults, projectName) {
  // ===== Create a zip file
  const zip = new JSZip();

  // ===== Add the images in a folder
  const imagesFolder = zip.folder("images");
  for (let i = 0; i < widgetResults.length; i++) {
    const widget = widgetResults[i];
    const imageUrl = widget.imageUrl;
    if (!imageUrl) return;

    const imageFilename = getImageName(i, widget);
    const imageBlob = await fetch(imageUrl).then((r) => r.blob());
    imagesFolder.file(imageFilename, imageBlob, { base64: true });
  }

  // ===== Generate the markdown analysis file
  let markdown = `# ${projectName} DebiAI Analysis\n`;

  // Add the time
  const date = new Date();
  const timeString = date.toLocaleTimeString("fr-FR");
  const dateString = date.toLocaleDateString("fr-FR");
  markdown += `\n ${dateString} - ${timeString}\n`;

  // Add the widgets
  for (let i = 0; i < widgetResults.length; i++) {
    // Title
    const widget = widgetResults[i];
    markdown += `\n## ${widget.widget} - ${widget.name}\n`;

    // Config
    if (widget.config) {
      const config = JSON.stringify(widget.config, null, 2);
      markdown += `\n\`\`\`json\n${config}\n\`\`\`\n`;
    }

    // Image
    if (widget.imageUrl) {
      const imageFilename = getImageName(i, widget);
      markdown += `\n![${widget.name}](images/${imageFilename})\n`;
    }
  }

  // Add the markdown analysis file
  zip.file("analysis.md", markdown);

  // Generate the zip file
  zip.generateAsync({ type: "blob" }).then(function (content) {
    FileSaver.saveAs(content, projectName + "_Analysis.zip");
  });
}
