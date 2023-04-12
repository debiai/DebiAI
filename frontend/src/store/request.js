export default class Request {
  constructor(name, code, progress) {
    this.name = name;
    this.code = code;
    this.progress = progress;
    this.quantity = 0; // Number of elements processed at the moment

    // Get creation time
    this.creationTime = Date.now();
  }
}
