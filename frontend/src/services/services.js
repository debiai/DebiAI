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
    const a = new Date(ts);
    const day = a.getDay();
    const hour = a.getHours();
    const min = a.getMinutes();
    const sec = a.getSeconds() + 1; // To end on a full second
    let time = sec + "s";
    if (min > 0) time = min + "m" + time;
    if (hour > 0) time = hour + "h " + time;
    if (day > 0) time = day + "d " + time;
    return time;
  },

  timeStampToDate(ts, hoursOnly = false) {
    const a = new Date(ts);
    const months = [
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
    const year = a.getFullYear();
    const month = months[a.getMonth()];
    const date = a.getDate();
    const hour = a.getHours();
    const min = a.getMinutes();
    const sec = a.getSeconds();
    if (hoursOnly) return hour + ":" + min + ":" + sec;
    else return date + " " + month + " " + year + " " + hour + ":" + min + ":" + sec;
  },

  nbSecondsToTime(nbSeconds) {
    let seconds = Math.floor(nbSeconds);
    if (nbSeconds <= 0) return "0s";

    const days = Math.floor(seconds / 86400);
    seconds %= 86400;
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    seconds %= 60;

    let time = "";
    if (days > 0) time += `${days}d `;
    if (hours > 0 || days > 0) time += `${hours}h `;
    if (minutes > 0 || hours > 0 || days > 0) time += `${minutes}m `;
    time += `${seconds}s`;

    return time.trim();
  },

  timeSpentBetween(startTs, endTs) {
    const diffInSeconds = endTs - startTs;
    const hours = Math.floor(diffInSeconds / 3600);
    const minutes = Math.floor((diffInSeconds % 3600) / 60);
    const seconds = Math.floor(diffInSeconds % 60);

    let result = "";
    if (hours > 0) result += `${hours}h `;
    if (minutes > 0 || hours > 0) result += `${minutes}m `;
    result += `${seconds}s`;

    return result.trim();
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

  uppercaseFirstLetter(str) {
    if (typeof str !== "string") return str;
    return str.charAt(0).toUpperCase() + str.slice(1);
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
