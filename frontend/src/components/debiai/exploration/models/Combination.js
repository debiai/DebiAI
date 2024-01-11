export class Combination {
  constructor(index, combinationValues, nbData) {
    this.index = index;
    this.values = combinationValues;
    this.metrics = {
      nbData: nbData,
    };
  }
}
