const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
import { v4 as uuidv4 } from 'uuid';

export default {
  isMobile,

  prettyTimeStamp(ts) {
    let sec = (Date.now() - ts) / 1000
    if (sec < 60) return "Just now"
    let min = sec / 60
    if (min < 60) return Math.floor(min) + " min ago"
    let h = min / 60
    if (Math.floor(h) == 1) return "1 hour ago"
    if (h < 24) return Math.floor(h) + " hours ago"
    let days = h / 24
    if (Math.floor(days) == 1) return "1 day ago"
    if (days < 30) return Math.floor(days) + " days ago"
    let months = days / 30
    if (Math.floor(months) == 1) return "1 mounth ago"
    if (months < 12) return Math.floor(months) + " months ago"
    let years = months / 12
    if (Math.floor(years) == 1) return "1 year ago"
    return Math.floor(years) + " years ago"
  },

  timeStampToDate(ts) {
    var a = new Date(ts);
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
    return time;
  },

  prettyNumber(x) {
    if (x === null) return null
    if (typeof x !== 'number') return x
    if (Math.abs(x) < 1000000) {
      return Number.isInteger(x) ? x : x.toFixed(2)
    }

    return x.toPrecision(3)
  },

  csvToArray(csvString) {
    let delimiter = ","
    if (!csvString || !csvString.length) return [];

    const pattern = new RegExp(
      ("(\\" + delimiter + "|\\r?\\n|\\r|^)" +
        "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
        "([^\"\\" + delimiter + "\\r\\n]*))"
      ), "gi"
    );

    let rows = [[]];
    let matches = true;

    while (matches) {
      matches = pattern.exec(csvString)
      if (!matches) continue
      const matched_delimiter = matches[1];
      const matched_cellQuote = matches[2];
      const matched_cellNoQuote = matches[3];

      /*
       * Edge case: Data that starts with a delimiter
       */
      if (matches.index == 0 && matched_delimiter)
        rows[rows.length - 1].push("");

      /*
       * Fix empty lines
       */
      // if (!matches[2] && !matches[3])
      //   continue;

      if (matched_delimiter.length && matched_delimiter !== delimiter)
        rows.push([]);

      const matched_value = (matched_cellQuote)
        ? matched_cellQuote.replace(
          new RegExp("\"\"", "g"), "\""
        )
        : matched_cellNoQuote;

      rows[rows.length - 1].push(matched_value);

    }
    return rows;
  },

  uuid() {
    return uuidv4()
  },

  getTimestamp() {
    return Date.now()
  },

  getDate() {
    return this.timeStampToDate(this.getTimestamp())
  }
}