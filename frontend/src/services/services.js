const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
  navigator.userAgent
);
import { v4 as uuidv4 } from "uuid";
import {
  pearsonCorrelationMatrix,
  spearmanCorrelationMatrix,
} from "./statistics/correlationMatrices";
import store from "../store";

export default {
  // Responsive
  isMobile,

  // Time
  prettyTimeStamp(ts) {
    let sec = (Date.now() - ts) / 1000;
    if (sec < 60) return "Just now";
    let min = sec / 60;
    if (min < 60) return Math.floor(min) + " min ago";
    let h = min / 60;
    if (Math.floor(h) == 1) return "1 hour ago";
    if (h < 24) return Math.floor(h) + " hours ago";
    let days = h / 24;
    if (Math.floor(days) == 1) return "1 day ago";
    if (days < 30) return Math.floor(days) + " days ago";
    let months = days / 30;
    if (Math.floor(months) == 1) return "1 month ago";
    if (months < 12) return Math.floor(months) + " months ago";
    let years = months / 12;
    if (Math.floor(years) == 1) return "1 year ago";
    return Math.floor(years) + " years ago";
  },

  timeStampToTime(ts) {
    var a = new Date(ts);
    var hour = a.getHours() - 1; // GMT+1
    var min = a.getMinutes();
    var sec = a.getSeconds() + 1; // To end on a full second
    var time = sec + "s";
    if (min > 0) time = min + "m" + time;
    if (hour > 0) time = hour + "h " + time;

    return time;
  },

  timeStampToDate(ts) {
    var a = new Date(ts);
    var months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + " " + month + " " + year + " " + hour + ":" + min + ":" + sec;
    return time;
  },

  timeStampToHourAndMinute(ts) {
    var a = new Date(ts);
    var hour = a.getHours();
    var min = a.getMinutes();
    if (min < 10) min = "0" + min;
    if (hour < 10) hour = "0" + hour;
    var time = hour + "h" + min;
    return time;
  },

  getTimestamp() {
    return Date.now();
  },

  getDate() {
    return this.timeStampToDate(this.getTimestamp());
  },

  // Pretty
  prettyNumber(x) {
    if (x === null) return null;
    if (typeof x !== "number") return x;
    if (Math.abs(x) < 1000000) {
      return Number.isInteger(x) ? x : x.toFixed(2);
    }

    return x.toPrecision(3);
  },

  prettifyJSON(jsonObj, indentation = 0) {
    let prettifiedString = "";
    const indent = "  ".repeat(indentation);

    for (const key in jsonObj) {
      if (Object.prototype.hasOwnProperty.call(jsonObj, key)) {
        const formattedKey = `<b>${key}</b>`;
        if (Array.isArray(jsonObj[key])) {
          if (jsonObj[key].every((item) => typeof item === "string" || typeof item === "number")) {
            prettifiedString += `${indent}${formattedKey}: [${jsonObj[key].join(", ")}]\n`;
          } else {
            prettifiedString += `${indent}${formattedKey}:\n`;
            jsonObj[key].forEach((item, index) => {
              if (
                typeof item === "object" &&
                Array.isArray(item) &&
                item.every(
                  (nestedItem) => typeof nestedItem === "string" || typeof nestedItem === "number"
                )
              ) {
                prettifiedString += `${indent}  ${index}: [${item.join(", ")}]\n`;
              } else if (typeof item === "object") {
                prettifiedString += `${indent}  ${index}: `;
                prettifiedString += `\n${this.prettifyJSON(item, indentation + 3)}`;
              } else {
                prettifiedString += `${indent}  ${index}: ${item}\n`;
              }
            });
          }
        } else if (typeof jsonObj[key] === "object") {
          prettifiedString += `${indent}${formattedKey}:\n${this.prettifyJSON(
            jsonObj[key],
            indentation + 1
          )}`;
        } else {
          prettifiedString += `${indent}${formattedKey}: ${jsonObj[key]}\n`;
        }
      }
    }
    return prettifiedString;
  },

  // Random
  uuid() {
    return uuidv4();
  },

  // Statistics
  pearsonCorrelationMatrix,
  spearmanCorrelationMatrix,

  // Requests animations
  startRequest(name, cancelCallback = null) {
    let requestCode = uuidv4();
    store.commit("startRequest", { name, code: requestCode, cancelCallback });
    return requestCode;
  },
  startProgressRequest(name) {
    let requestCode = uuidv4();
    store.commit("startRequest", { name, code: requestCode, progress: 0 });
    return requestCode;
  },
  updateRequestProgress(code, progress) {
    store.commit("updateRequestProgress", { code, progress });
  },
  updateRequestQuantity(code, quantity) {
    store.commit("updateRequestQuantity", { code, quantity });
  },
  endRequest(code) {
    store.commit("endRequest", code);
  },
};
