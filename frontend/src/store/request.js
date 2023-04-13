export default class Request {
  constructor(name, code, progress, cancelCallback) {
    this.name = name;
    this.code = code;
    this.progress = progress;
    this.cancelCallback = cancelCallback;
    if (this.cancelCallback) this.cancellable = true;
    // Number of elements processed at the moment
    this.quantity = 0;

    // Get creation time
    this.creationTime = Date.now();
  }

  cancel() {
    if (this.cancellable) {
      this.cancelCallback();
    }
  }
}
