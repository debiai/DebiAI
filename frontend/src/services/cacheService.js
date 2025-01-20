import store from "../store";

// The browser cache service
// Used to store samples and results for faster loading with the indexed db cache system
const DB_VERSION = 1;

async function getDb(timestamp) {
  const projectId = store.state.ProjectPage.projectId;
  const dataProviderId = store.state.ProjectPage.dataProviderId;
  const dbName = `${dataProviderId}___${projectId}`;

  return new Promise((resolve, reject) => {
    let request = window.indexedDB.open(dbName, DB_VERSION);

    request.onerror = (e) => {
      console.log("Error opening db", e);
      reject("Error");
    };

    request.onsuccess = (e) => {
      // Connection successful
      // Checking that the timestamp is the same

      let transaction = e.target.result.transaction("data", "readwrite");
      const dataStore = transaction.objectStore("data");
      let timestampRequest = dataStore.get("timestamp");

      timestampRequest.onsuccess = () => {
        let timestampObj = timestampRequest.result;
        if (!timestampObj || !timestampObj.timestamp || timestampObj.timestamp !== timestamp) {
          // The database isn't up to date
          // The dada need to be erased in case of modifications
          console.log("Resetting the project database");

          // Samples store
          let sampleTransaction = e.target.result.transaction("samples", "readwrite");
          const sampleStore = sampleTransaction.objectStore("samples");
          let sampleStoreRequest = sampleStore.clear();

          sampleStoreRequest.onsuccess = () => {
            console.log("Sample store cleared");
            // Results store
            let resultsTransaction = e.target.result.transaction("results", "readwrite");
            const resultsStore = resultsTransaction.objectStore("results");
            let resultsStoreRequest = resultsStore.clear();

            resultsStoreRequest.onsuccess = () => {
              console.log("results store cleared");
              // Data store
              let transaction = e.target.result.transaction("data", "readwrite");
              const dataStore = transaction.objectStore("data");
              let dataStoreRequest = dataStore.clear();

              dataStoreRequest.onsuccess = () => {
                console.log("data store cleared");
                // add the timestamp
                dataStore.put({ id: "timestamp", timestamp });
                resolve(e.target.result);
              };
            };
          };
        } else {
          resolve(e.target.result);
        }
      };
    };

    request.onupgradeneeded = (e) => {
      console.log("Init cache database");

      let db = e.target.result;
      db.createObjectStore("samples", { keyPath: "sampleId" });
      db.createObjectStore("results", { keyPath: ["sampleId", "modelId"] });
      let dataStore = db.createObjectStore("data", { keyPath: "id" });

      // add the timestamp
      dataStore.put({ id: "timestamp", timestamp });
    };
  });
}

async function resetDb() {
  const projectId = store.state.ProjectPage.projectId;
  const dataProviderId = store.state.ProjectPage.dataProviderId;
  const dbName = `${dataProviderId}___${projectId}`;

  return new Promise((resolve, reject) => {
    let request = window.indexedDB.deleteDatabase(dbName);

    request.onerror = (e) => {
      console.log("Error deleting db", e);
      reject("Error");
    };

    request.onsuccess = (e) => {
      resolve();
    };
  });
}

async function saveSamples(timestamp, samples) {
  // Samples :
  // {
  //   id1: [...],
  //   id2: [...],
  //   ...
  // }

  try {
    let db = await getDb(timestamp);
    console.time("Saving data to the cache");

    return new Promise((resolve) => {
      // Init transaction
      let trans = db.transaction("samples", "readwrite");
      trans.oncomplete = () => {
        console.timeEnd("Saving data to the cache");
        resolve();
      };
      trans.onerror = (e) => {
        console.timeEnd("Saving data to the cache");
        console.log("Error");
        console.log(e);
        resolve();
      };

      // Get the sample store
      let sampleStore = trans.objectStore("samples");

      // Save all sample
      Object.entries(samples).forEach(([sampleId, sample]) =>
        sampleStore.put({ sampleId: sampleId.toString(), data: sample })
      );
    });
  } catch (error) {
    console.warn("Error while saving samples to cache");
  }
}

async function getSamplesByIds(timestamp, sampleIds) {
  try {
    let db = await getDb(timestamp);

    return new Promise((resolve) => {
      let trans = db.transaction("samples", "readonly");
      let sampleStore = trans.objectStore("samples");
      let samples = {};
      let lastSample = sampleIds.length;

      console.time("Loading data from cache");
      sampleIds.forEach((sampleId, i) => {
        let resultRequest = sampleStore.get(sampleId.toString());
        resultRequest.onsuccess = () => {
          if (resultRequest.result) samples[sampleId] = resultRequest.result.data;
          if (i == lastSample - 1) {
            console.timeEnd("Loading data from cache");
            resolve(samples);
          }
        };
        resultRequest.onerror = (e) => {
          console.timeEnd("Loading data from cache");
          console.log("Error");
          console.log(e);
          resolve(samples);
        };
      });
    });
  } catch (error) {
    console.warn("Error while loading samples from cache");
    return {};
  }
}

async function getNbSamples(timestamp) {
  // Get the number of samples in the cache for the current project
  try {
    let db = await getDb(timestamp);

    return new Promise((resolve) => {
      let trans = db.transaction("samples", "readonly");
      let sampleStore = trans.objectStore("samples");
      const request = sampleStore.count();
      request.onsuccess = () => {
        resolve(request.result);
      };
      request.onerror = (e) => {
        console.log("Error");
        console.log(e);
        resolve(0);
      };
    });
  } catch (error) {
    console.warn("Error while loading samples from cache");
    return null;
  }
}

// async function saveResults(timestamp, modelId, results) {
//   let db = await getDb(timestamp);
//   console.time("Saving results to the cache");

//   return new Promise((resolve) => {
//     let trans = db.transaction("results", "readwrite");
//     trans.oncomplete = () => {
//       console.timeEnd("Saving results to the cache");
//       resolve();
//     };
//     trans.onerror = (e) => {
//       console.timeEnd("Saving results to the cache");
//       console.log("Error");
//       console.log(e);
//       resolve();
//     };

//     let resultsStore = trans.objectStore("results");
//     Object.entries(results).forEach(([sampleId, result]) =>
//       resultsStore.put({ sampleId, modelId, result })
//     );
//   });
// }

// async function getModelResultsByIds(timestamp, modelId, sampleIds) {
//   let db = await getDb(timestamp);

//   return new Promise((resolve) => {
//     let trans = db.transaction("results", "readonly");
//     let resultsStore = trans.objectStore("results");
//     let results = {};
//     let lastSample = sampleIds.length;

//     console.time("Loading results from cache");
//     sampleIds.forEach((sampleId, i) => {
//       // For unknown reason, the modelID and sampleID in the double key
//       // need to be swapped :
//       let resultRequest = resultsStore.get([modelId, sampleId]);
//       resultRequest.onsuccess = () => {
//         if (resultRequest.result) results[sampleId] = resultRequest.result.result;
//         if (i == lastSample - 1) {
//           console.timeEnd("Loading results from cache");
//           resolve(results);
//         }
//       };
//       resultRequest.onerror = (e) => {
//         console.timeEnd("Loading results from cache");
//         console.log("Error");
//         console.log(e);
//         resolve(results);
//       };
//     });
//   });
// }

// async function getAllResults(db) {
//   return new Promise((resolve) => {

//     let trans = db.transaction(['results'], 'readonly');
//     trans.oncomplete = () => {
//       resolve(results);
//     };

//     let store = trans.objectStore('results');
//     let results = [];

//     store.openCursor().onsuccess = e => {
//       let cursor = e.target.result;
//       if (cursor) {
//         results.push(cursor.value)
//         cursor.continue();
//       }
//     };

//   });
// }

export default {
  saveSamples,
  resetDb,
  getSamplesByIds,
  // saveResults,
  // getModelResultsByIds,
  getNbSamples,
};
