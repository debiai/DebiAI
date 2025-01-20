// Returns an MxM matrix of Pearson correlation coefficients between each pair of columns in data (NxM).
function pearsonCorrelationMatrix(data) {
  const m = data.length;
  const matrix = Array.from({ length: m }, () => Array(m).fill(0));

  // Pearson between two arrays
  function pearson(x, y) {
    let sumX = 0,
      sumY = 0,
      sumXY = 0,
      sumX2 = 0,
      sumY2 = 0;
    const len = x.length;
    for (let i = 0; i < len; i++) {
      sumX += x[i];
      sumY += y[i];
      sumXY += x[i] * y[i];
      sumX2 += x[i] ** 2;
      sumY2 += y[i] ** 2;
    }
    const numerator = len * sumXY - sumX * sumY;
    const denominator = Math.sqrt((len * sumX2 - sumX ** 2) * (len * sumY2 - sumY ** 2));
    return denominator === 0 ? 0 : numerator / denominator;
  }

  // Build matrix
  for (let i = 0; i < m; i++) {
    for (let j = i; j < m; j++) {
      const correlation = pearson(data[i], data[j]);
      matrix[i][j] = correlation;
      matrix[j][i] = correlation; // Mirror value
    }
  }

  return matrix;
}

// Returns an MxM matrix of Spearman correlation coefficients between each pair of columns in data (NxM).
function spearmanCorrelationMatrix(data) {
  const m = data.length;
  const matrix = Array.from({ length: m }, () => Array(m).fill(0));

  // Rank an array
  function rank(arr) {
    const sorted = [...arr].map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
    const ranks = new Array(arr.length);
    let currentRank = 1;
    for (let i = 0; i < sorted.length; i++) {
      if (i > 0 && sorted[i][0] === sorted[i - 1][0]) {
        ranks[sorted[i][1]] = ranks[sorted[i - 1][1]];
      } else {
        ranks[sorted[i][1]] = currentRank;
      }
      currentRank++;
    }
    return ranks;
  }

  // Simple Pearson helper for ranks
  function pearson(x, y) {
    let sumX = 0,
      sumY = 0,
      sumXY = 0,
      sumX2 = 0,
      sumY2 = 0;
    const len = x.length;
    for (let i = 0; i < len; i++) {
      sumX += x[i];
      sumY += y[i];
      sumXY += x[i] * y[i];
      sumX2 += x[i] ** 2;
      sumY2 += y[i] ** 2;
    }
    const numerator = len * sumXY - sumX * sumY;
    const denominator = Math.sqrt((len * sumX2 - sumX ** 2) * (len * sumY2 - sumY ** 2));
    return denominator === 0 ? 0 : numerator / denominator;
  }

  // Build matrix by ranking each column then computing Pearson
  for (let i = 0; i < m; i++) {
    const ri = rank(data[i]);
    for (let j = i; j < m; j++) {
      const rj = rank(data[j]);
      const correlation = pearson(ri, rj);
      matrix[i][j] = correlation;
      matrix[j][i] = correlation; // Mirror value
    }
  }
  return matrix;
}

// Example export
module.exports = {
  pearsonCorrelationMatrix,
  spearmanCorrelationMatrix,
};
