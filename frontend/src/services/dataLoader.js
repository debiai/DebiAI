import store from '../store'
import cacheService from './cacheService'
import services from "./services"

const backendDialog = require("./backendDialog")

const CATEGORIES = [
  { blName: "inputs", singleName: "input" },
  { blName: "groundTruth", singleName: "ground truth" },
  { blName: "contexts", singleName: "context" },
  { blName: "others", singleName: "other" },
]


// Requests functions
function startRequest(name) {
  let requestCode = services.uuid()
  store.commit("startRequest", { name, code: requestCode })
  return requestCode
}
function startProgressRequest(name) {
  let requestCode = services.uuid()
  store.commit("startRequest", { name, code: requestCode, progress: 0 })
  return requestCode
}
function updateRequestProgress(code, progress) {
  store.commit("updateRequestProgress", { code, progress })
}
function endRequest(code) {
  store.commit("endRequest", code)
}

// Get project samples Id list functions
async function getProjectSamplesIdList(projectMetadata, selectionIds = [], selectionIntersection = false, modelIds = [], commonResults = false) {
  // Returns the list of samples id for a project
  // this need to be done in a sequential way to avoid
  // too big requests

  const accepteSize = 10000
  const projectNbSamples = projectMetadata.nbSamples

  if (projectNbSamples === 0) { return [] }

  if (projectNbSamples === undefined || projectNbSamples === null || projectNbSamples <= accepteSize || selectionIds.length > 0 || modelIds.length > 0) {
    // At the moment, we gather all ID when we deal with selections and models
    // If we have a small project, we gather all ID
    // Also, if we don't have the number of samples, we gather all ID
    const res = await backendDialog.default.getProjectSamples(projectMetadata.projectId, {
      selectionIds, selectionIntersection, modelIds, commonResults
    })
    return res.samples
  } else {
    // We gather all the project samples ID
    // We need to split it in multiple requests
    let nbRequest = Math.ceil(projectNbSamples / accepteSize)
    let samplesIdList = []

    console.log("Splitting ID list request in ", nbRequest, " requests");
    let requestCode = startProgressRequest('Loading the project data ID list')

    try {
      console.time("getProjectSamplesIdList")
      for (let i = 0; i < nbRequest; i++) {
        const from = i * accepteSize
        const to = Math.min((i + 1) * accepteSize, projectNbSamples) - 1

        const res = await backendDialog.default.getProjectSamples(projectMetadata.projectId, { from, to })

        if (res.samples.length === 0) throw ("No samples found while loading project samples ID list from " + from + " to " + to)
        if (res.samples.length !== to - from + 1) throw ("Wrong number of samples while loading project samples ID list from " + from + " to " + to +
          ", got " + res.samples.length + " instead of " + (to - from + 1))
        samplesIdList = samplesIdList.concat(res.samples)
        updateRequestProgress(requestCode, (i + 1) / nbRequest)
      }
      console.timeEnd("getProjectSamplesIdList")
      endRequest(requestCode)
    } catch (error) {
      console.timeEnd("getProjectSamplesIdList")
      endRequest(requestCode)
      throw error
    }

    console.log("Request done, ", samplesIdList.length, " samples found over ", projectNbSamples, " samples requested");
    return samplesIdList
  }
}
async function getProjectMetadata(projectId, { considerResults }) {
  let projectInfo = await backendDialog.default.getProject(projectId)

  // Labels creation from block level info
  var metaData = {
    projectId: projectInfo.id,
    timestamp: projectInfo.creationDate,
    nbSamples: projectInfo.nbSamples,
    labels: [],
    categories: [],
    type: [],
  }
  
  // // Set the Sample_ID in the Other category
  // metaData.labels.push("Sample_ID")
  // metaData.categories.push("other")
  // metaData.type.push("unknown")

  projectInfo.blockLevelInfo.forEach(blockLevel => {
    // Set the block name in the Other category
    metaData.labels.push(blockLevel.name)
    metaData.categories.push("other")
    metaData.type.push("unknown")

    CATEGORIES.forEach(cat => {
      if (cat.blName in blockLevel)
        blockLevel[cat.blName].forEach(data => {
          metaData.labels.push(data.name)
          metaData.categories.push(cat.singleName)
          metaData.type.push(data.type)
        })
    });
  })

  // In case we are loading the results
  if (considerResults && "resultStructure" in projectInfo) {
    // push model Name
    metaData.labels.push("model")
    metaData.categories.push("results")

    // push model expected results
    projectInfo.resultStructure.forEach(data => {
      metaData.labels.push(data.name)
      metaData.categories.push("results")
    })
  }

  return metaData
}
async function downloadSamplesData(projectId, timestamp, sampleIds) {
  const CHUNK_SIZE = 2000
  let pulledData = 0
  let nbSamples = sampleIds.length

  // Create a request
  let requestCode = startProgressRequest('Loading the project data')
  console.time('Loading the project data')
  // Pull the tree
  let retArray = []
  let retDataIdlist = []

  try {
    while (pulledData < nbSamples) {

      let samplesToPull = sampleIds.slice(pulledData, pulledData + CHUNK_SIZE)

      // First, pull the samples from the browser memory
      let cachedSamples = await cacheService.getSamplesByIds(projectId, timestamp, samplesToPull)
      let samplesToDownload = samplesToPull.filter(sampleId => !(sampleId in cachedSamples))
      retArray = [...retArray, ...Object.values(cachedSamples)]
      retDataIdlist = [...retDataIdlist, ...Object.keys(cachedSamples)]

      if (samplesToDownload.length) {
        // Then download the missing samples
        console.log(samplesToDownload.length + " samples to download")

        let downloadedSamples = await backendDialog.default.getBlocksFromSampleIds(projectId, samplesToDownload)

        // We receive an map of samples
        let map = downloadedSamples.data

        // Stack the samples
        retArray = [...retArray, ...Object.values(map)]
        retDataIdlist = [...retDataIdlist, ...Object.keys(map)]

        // Store the samples in the cache
        // await cacheService.storeSamples(projectId, timestamp, map) TODO 
      }

      // Update the progress
      pulledData += CHUNK_SIZE
      updateRequestProgress(requestCode, pulledData / nbSamples)
    }
  } finally {
    endRequest(requestCode)
    console.timeEnd('Loading the project data')
  }

  return { dataArray: retArray, sampleIdList: retDataIdlist }
}


async function downloadResults(projectId, timestamp, modelId, sampleIds) {
  const CHUNK_SIZE = 10000
  let pulledData = 0
  // Create a request
  let requestCode = services.uuid()
  store.commit("startRequest", { name: modelId, code: requestCode, progress: 0 })
  let modelResultsRet = {}

  try {
    // Not done because more time is spent storing the cache : First, pull the tree from the browser memory
    // let cachedResults = await cacheService.getModelResultsByIds(projectId, timestamp, modelId, sampleIds)
    // let resutlsToDownload = sampleIds.filter(sampleId => !(sampleId in cachedResults))

    // add the cached results to our results without empty one
    // for (const sampleId in cachedResults)
    //   if (cachedResults[sampleId] !== null) modelResultsRet[sampleId] = cachedResults[sampleId]

    // Pull the tree
    // let nbSamples = resutlsToDownload.length
    // if (nbSamples) console.log(nbSamples + " results to download");

    let nbSamples = sampleIds.length
    while (pulledData < nbSamples) {

      let samplesToPull = sampleIds.slice(pulledData, pulledData + CHUNK_SIZE)

      let modelResults = await backendDialog.default.getModelResults(projectId, modelId, samplesToPull)
      modelResultsRet = Object.assign({}, modelResultsRet, modelResults)

      // TODO : Save restults in the cache, save {} in case of not evaluated
      // let resultsToSave = {}
      // samplesToPull.forEach(sampleId => {
      //   resultsToSave[sampleId] = sampleId in modelResultsRet ? modelResultsRet[sampleId] : null
      // });
      // cacheService.saveResults(projectId, timestamp, modelId, resultsToSave)

      pulledData += CHUNK_SIZE
      store.commit("updateRequestProgress", { code: requestCode, progress: pulledData / nbSamples })
    }
  } catch (error) {
    store.commit("endRequest", requestCode)
    throw error
  }
  store.commit("updateRequestProgress", { code: requestCode, progress: 1 })
  store.commit("endRequest", requestCode)
  return modelResultsRet
}

const min = (arr) => {
  let min = Infinity;
  for (let i = 0; i < arr.length; i++) if (arr[i] < min) min = arr[i];
  return min
}
const max = (arr) => {
  let max = -Infinity;
  for (let i = 0; i < arr.length; i++) if (arr[i] > max) max = arr[i];
  return max
}

// Main methods :
/**
 * @param {string} projectId
 * @returns
 */
async function loadData(projectId, selectionIds, selectionIntersection) {
  // Downloading project meta data, requiered to interprate the tree
  let projectMetadata = await getProjectMetadata(projectId, { considerResults: false })

  // Get the samples to pull
  let samplesToPull = await getProjectSamplesIdList(projectMetadata, selectionIds, selectionIntersection)

  // Download and convert the tree
  const { dataArray, sampleIdList } = await downloadSamplesData(
    projectId,
    projectMetadata.timestamp,
    samplesToPull
  )

  return {
    metaData: projectMetadata,
    array: [projectMetadata.labels, ...dataArray],
    sampleIdList
  }
}
/**
 * @param {string} projectId
 * @param {Array<string>} modelIds
 * @param {boolean} common get the common sample or not
 * @param {string?} selectionId Get model on the selection if provided
 */
async function loadDataAndModelResults(projectId, selectionIds, selectionIntersection, modelIds, commonResults) {

  // Downloading project meta data, requiered to interprate the tree
  let projectMetadata = await getProjectMetadata(projectId, { considerResults: true })

  // Get the samples ID to pull
  let samplesToPull = await getProjectSamplesIdList(projectMetadata, selectionIds, selectionIntersection, modelIds, commonResults)

  // Download and convert the tree
  const { dataArray, sampleIdList } = await downloadSamplesData(
    projectId,
    projectMetadata.timestamp,
    samplesToPull
  )

  // =========== Then add the model results
  // Create a request
  let requestCode = startProgressRequest('Loading the model results')

  try {
    let dataArrayFull = []
    let samplesToPullFull = []

    for (let i = 0; i < modelIds.length; i++) {
      const modelId = modelIds[i];

      let modelResults = await downloadResults(
        projectId,
        projectMetadata.timestamp,
        modelId,
        samplesToPull
      )

      
      // We now have a sample array and a list of results
      // We need to duplicate each one of the samples for each one of the sample results
      // ie : if a sample got evaluated on 3 models, the sample must be 3 time sample, each one
      // with his own model results

      const dataAndResultsArray = [];
      const modelsSamplesToPull = [];

      sampleIdList.forEach((sampleId, i) => {
        if (sampleId in modelResults) {
          dataAndResultsArray.push([...dataArray[i], modelId, ...modelResults[sampleId]])
          modelsSamplesToPull.push(sampleId)
        }
      });

      dataArrayFull = [...dataArrayFull, ...dataAndResultsArray]
      samplesToPullFull = [...samplesToPullFull, ...modelsSamplesToPull]
      store.commit("updateRequestProgress", { code: requestCode, progress: (i + 1) / modelIds.length })
    }
    store.commit("endRequest", requestCode)

    return {
      metaData: projectMetadata,
      array: [projectMetadata.labels, ...dataArrayFull],
      sampleIdList: samplesToPullFull
    }
  } catch (error) {
    store.commit("endRequest", requestCode)
    throw error
  }
}

// array to DebiAI analysis main data object
async function arrayToJson(array, metaData) {
  let requestCode = startProgressRequest("Preparing the analysis")
  console.time("Preparing the analysis")

  let ret = {
    labels: [],
    nbLines: 0,
    nbColumns: 0,
    columns: new Array(metaData.labels.length).fill([]),
    categories: [...CATEGORIES.map(c => c.singleName), "results"]
  };

  ret.labels = array[0];
  ret.nbLines = array.length - 1;
  ret.nbColumns = array[0].length;

  // deal with duplicate labels
  for (const [i, label] of ret.labels.entries()) {
    let dupInd = ret.labels.findIndex((l2, j) => label == l2 && i != j);
    let nbDup = 2;
    while (dupInd >= 0) {
      ret.labels[dupInd] = ret.labels[dupInd] + "_" + nbDup;
      dupInd = ret.labels.findIndex((l2, j) => label == l2 && i != j);
    }
  }

  for await (const [i, label] of ret.labels.entries()) {
    // Creating the column object
    let col = {
      label,
      index: i,
      values: [],
      type: null,
      typeText: "",
      category: "other"
    };

    // Filling the column
    for (let j = 1; j < ret.nbLines + 1; j++)
      col.values.push(array[j][i]);

    col.uniques = [...new Set(col.values)];
    col.nbOccu = col.uniques.length;

    // Cheking if the column is type text, number or got undefined values
    if (col.uniques.findIndex(v => v === undefined || v === "" || v === null) >= 0) {
      // undefined Values
      col.type = undefined;
      col.typeText = "undefined";
      col.undefinedIndexs = col.values
        .map((v, i) => (v == undefined || v == "" || v == null ? i : -1))
        .filter(v => v >= 0);
      console.warn("Undefined values : " + label);
      console.warn(col.uniques);
      console.warn(col.values);
    } else if (metaData.type[i] == "text" || col.uniques.find(v => isNaN(v))) {
      // String Values
      col.type = String;
      col.typeText = "Class";
      let tmpUniqMap = {}
      col.valuesIndexUniques = col.uniques.map((str, i) => {
        tmpUniqMap[str] = i
        return i
      });

      col.valuesIndex = col.values.map(str => tmpUniqMap[str]);
      col.min = min(col.valuesIndexUniques);
      col.max = max(col.valuesIndexUniques);
    } else {
      // Default Type
      col.type = Number;
      col.typeText = "Num";
      col.values = col.values.map(v => +v)
      col.uniques = col.uniques.map(v => +v)
      col.nbOccu = col.uniques.length;
      col.min = min(col.uniques);
      col.max = max(col.uniques);
      col.average =
        col.values.reduce((a, b) => a + b, 0) / ret.nbLines || 0;
      if (col.uniques.length < 100)
        col.uniques.sort((a, b) => a - b);
    }

    // deal with provided metaData
    col.category = metaData.categories[i]

    ret.columns[i] = col;

    updateRequestProgress(requestCode, (i + 1) / ret.nbColumns)
    console.timeLog("Preparing the analysis", "Column " + label + " " + (i + 1) + " / " + ret.nbColumns)
  }

  endRequest(requestCode)
  console.timeEnd("Preparing the analysis")

  return ret;
}

async function loadProjectSamples({
  projectId,
  selectionIds = null,
  selectionIntersection = false,
  modelIds = null,
  commomModelResults = false
}) {

  let requestCode = startRequest("The analysis is starting")

  // Load the project tree as an array
  let data, projectSamples
  try {
    if (modelIds && modelIds.length > 0) {
      projectSamples = await loadDataAndModelResults(
        projectId,
        selectionIds,
        selectionIntersection,
        modelIds,
        commomModelResults,
      )
    } else {
      projectSamples = await loadData(
        projectId,
        selectionIds,
        selectionIntersection
      )
    }
    let metaData = projectSamples.metaData
    let array = projectSamples.array
    let sampleIdList = projectSamples.sampleIdList

    // Convert the the array in an column lists ready for analysing
    data = await arrayToJson(array, metaData);
    data.sampleIdList = sampleIdList

  }
  finally { endRequest(requestCode) }

  return data
}

export default { loadProjectSamples }

