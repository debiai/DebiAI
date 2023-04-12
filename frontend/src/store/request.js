export default class Request {
  constructor(name, code, progress) {
    this.name = name;
    this.code = code;
    this.progress = progress;

    // Get creation time
    this.creationTime = Date.now();
  }
}
