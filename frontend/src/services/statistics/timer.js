import backendDialog from "../backendDialog"
import config from '../../../config'
const SEND_LOG = config.SEND_LOG

// Use to count time and display in log file
// widget is the name of the widget, data is a description of which data were pushed into it.
var logTime = function (t0, widget, samples, projectId, others = "") {
  if (!SEND_LOG)
    return

  var t1 = performance.now();
  var time = t1 - t0;

  // Create json to send
  var log = { "widget": widget, "durationMs": time, "samplesSize": samples, "otherData": others, "project": projectId }
  //var log = time + ";"  + data ;

  // Sending request
  return backendDialog
    .log(projectId, log)
    .catch((error) => {
      console.log(error);
    })
}

export default {
  logTime
}