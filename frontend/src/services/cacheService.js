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
          // The data need to be erased in case of modifications
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

    request.onsuccess = () => {
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

// Hash-based cache with localStorage persistence
// Used to deal with 304 responses
class PersistentHashCache {
  constructor() {
    this.memoryCache = new Map();
    this.loadFromStorage();
  }

  loadFromStorage() {
    try {
      const stored = localStorage.getItem("debiai_hash_cache");
      if (stored) {
        const data = JSON.parse(stored);
        Object.entries(data).forEach(([key, value]) => {
          // Only load recent cache entries (e.g., last 24 hours)
          if (Date.now() - value.timestamp < 24 * 60 * 60 * 1000) {
            this.memoryCache.set(key, value);
          }
        });
      }
    } catch (error) {
      console.warn("Error loading hash cache from storage", error);
    }
  }

  saveToStorage() {
    try {
      const data = Object.fromEntries(this.memoryCache);
      localStorage.setItem("debiai_hash_cache", JSON.stringify(data));
    } catch (error) {
      console.warn("Error saving hash cache to storage", error);
    }
  }

  set(key, value) {
    this.memoryCache.set(key, value);
    this.saveToStorage();
  }

  get(key) {
    return this.memoryCache.get(key) || null;
  }

  clear() {
    this.memoryCache.clear();
    localStorage.removeItem("debiai_hash_cache");
  }
}

const persistentHashCache = new PersistentHashCache();

async function saveHashResponse(cacheKey, hash, response) {
  try {
    persistentHashCache.set(cacheKey, {
      hash,
      response,
      timestamp: Date.now(),
    });
  } catch (error) {
    console.warn("Error while saving hash response to cache", error);
  }
}

async function getHashResponse(cacheKey) {
  try {
    return persistentHashCache.get(cacheKey);
  } catch (error) {
    console.warn("Error while getting hash response from cache", error);
    return null;
  }
}

export default {
  saveSamples,
  resetDb,
  getSamplesByIds,
  // saveResults,
  // getModelResultsByIds,
  getNbSamples,
  saveHashResponse,
  getHashResponse,
};
