import store from '../store'
import cacheService from '../services/cacheService'
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

  if (!projectNbSamples || projectNbSamples < accepteSize || selectionIds.length > 1 ||  modelIds.length > 1) {
    // At the moment, we gather all ID when we deal with selections and models
    // If we have a small project, we gather all ID
    // Also, if we don't have the number of samples, we gather all ID
    return backendDialog.default.getProjectSamples(projectMetadata.projectId, {
      selectionIds, selectionIntersection, modelIds, commonResults
    })
  } else {
    // We gather all the project samples ID
    // We need to split it in multiple requests
    let nbRequest = Math.ceil(projectNbSamples / accepteSize)
    let samplesIdList = []

    console.log("Splitting request in ", nbRequest, " requests");

    for (let i = 0; i < nbRequest; i++) {
      console.log("Request ", i, " / ", nbRequest);
      const from = i * accepteSize
      const to = Math.min((i + 1) * accepteSize, projectNbSamples) - 1
      console.log("From ", from, " to ", to)
      const samplesId = await backendDialog.default.getProjectSamples(projectMetadata.projectId, { from, to })
      samplesIdList = samplesIdList.concat(samplesId)
    }

    console.log("Request done, ", samplesIdList.length, " samples found over ", projectNbSamples, " samples requested");

    return samplesIdList
  }
}

// Get the values / results of the blocks
function getBlockValues(block) {
  // Adding the block name into the values
  var values = [block.name]

  // store all key-values into an array
  CATEGORIES.forEach(cat => {
    if (cat.blName in block)
      for (const [, val] of Object.entries(block[cat.blName]))
        values.push(val)
  });

  return values
}

function getBlockValuesWithRestults(block) {
  // In case we are loading the results
  let modelsResults = []
  if ("results" in block) {
    for (const modelId of Object.keys(block["results"])) {
      // push model Name (modelId)
      // push each model results

      modelsResults.push([modelId, ...block["results"][modelId]])
    }
  }
  return modelsResults
}

function getBlockRecur(block, considerResults) {
  // Getting bloc values
  var values = getBlockValues(block)
  if (block.childrenInfoList == undefined || block.childrenInfoList.length == 0) {
    // Sample, end of tree

    if (considerResults) {
      // We need to duplicate the lane for each models
      let modelResults = getBlockValuesWithRestults(block)
      return modelResults.map(result => values.concat(result));
    }

    // Single value if not considerResults
    return [values]
  }
  else {
    // Getting all child values
    let childValues = []
    block.childrenInfoList.forEach(childBlock => childValues.push(...getBlockRecur(childBlock, considerResults)));

    // Mergin childs and current block values
    //     CurBlock childs
    //     a        1
    //     a        2
    //     a        3

    //     b        1
    //     b        2
    //     b        3

    let array = []
    childValues.forEach(cv => array.push(values.concat(cv)));
    return array
  }
}

function getSampleHashList(block, considerResults) {
  if (block.childrenInfoList == undefined || block.childrenInfoList.length == 0) {
    // Sample, end of tree, return the hash
    if (considerResults) {
      // We need to duplicate the lane for each models
      let modelResults = getBlockValuesWithRestults(block)
      return modelResults.map(() => block.id);
    }

    // Single value if not considerResults
    return [block.id]
  }
  else {
    // Getting all child values
    let childHash = []
    block.childrenInfoList.forEach(childBlock => childHash.push(...getSampleHashList(childBlock, considerResults)));
    return childHash
  }
}

// Tree to array
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
async function downloadTree(projectId, timestamp, sampleIds) {
  const CHUNK_SIZE = 2000
  let pulledData = 0
  let nbSamples = sampleIds.length

  // Create a request
  let requestCode = startProgressRequest('Loading the project data')
  console.time('Loading the project data')
  // Pull the tree
  let retArray = []
  let retHashlist = []

  try {
    while (pulledData < nbSamples) {

      let samplesToPull = sampleIds.slice(pulledData, pulledData + CHUNK_SIZE)

      // First, pull the samples from the browser memory
      let cachedSamples = await cacheService.getSamplesByIds(projectId, timestamp, samplesToPull)
      let samplesToDownload = samplesToPull.filter(sampleId => !(sampleId in cachedSamples))
      retArray = [...retArray, ...Object.values(cachedSamples)]
      retHashlist = [...retHashlist, ...Object.keys(cachedSamples)]

      if (samplesToDownload.length) {
        // Then download the missing samples
        console.log(samplesToDownload.length + " samples to download")

        let downloadedSamples = await backendDialog.default.getBlocksFromSampleIds(projectId, samplesToDownload)

        if (downloadedSamples.dataMap) {
          // Dataprovider project, we derectly receive an map of samples
          let map = downloadedSamples.data
          Object.keys(map).forEach(dataId => {
            map[dataId] = [dataId, ...map[dataId]]
          });
          // Add the samples ID to the array
          retArray = [...retArray, ...Object.values(map)]
          retHashlist = [...retHashlist, ...Object.keys(map)]
        } else {
          // Python module project, we receive a tree that we need to convert
          let { samplesId, array } = await treeToArray(downloadedSamples, { considerResults: false })
          retArray = [...retArray, ...array]
          retHashlist = [...retHashlist, ...samplesId]
          // Save data in the cache
          let sampleToSave = array.map((data, i) => { return { sampleId: samplesId[i], data } })
          cacheService.saveSamples(projectId, timestamp, sampleToSave)
        }
      }

      // Update the progress
      pulledData += CHUNK_SIZE
      updateRequestProgress(requestCode, pulledData / nbSamples)
    }
  } finally {
    endRequest(requestCode)
    console.timeEnd('Loading the project data')
  }

  return { dataArray: retArray, sampleHashList: retHashlist }
}

function treeToArray(tree, { considerResults }) {
  // Recursive creation of the Array values
  var array = []
  tree.forEach(block => array.push(...getBlockRecur(block, considerResults)));

  // get the samples id hash list
  var samplesId = []
  tree.forEach(block => samplesId.push(...getSampleHashList(block, considerResults)));

  // Return the data array :  [[label 1, label 2], [value 1-1, value 1-2], ...]
  return { array, samplesId }
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
async function loadTree(projectId, selectionIds, selectionIntersection) {
  // Downloading project meta data, requiered to interprate the tree
  let projectMetadata = await getProjectMetadata(projectId, { considerResults: false })

  // Get the samples to pull
  let samplesToPull = await getProjectSamplesIdList(projectMetadata, selectionIds, selectionIntersection)

  // Download and convert the tree
  const { dataArray, sampleHashList } = await downloadTree(
    projectId,
    projectMetadata.timestamp,
    samplesToPull.samples
  )

  return {
    metaData: projectMetadata,
    array: [projectMetadata.labels, ...dataArray],
    sampleHashList
  }
}
/**
 * @param {string} projectId
 * @param {Array<string>} modelIds
 * @param {boolean} common get the common sample or not
 * @param {string?} selectionId Get model on the selection if provided
 */
async function loadTreeAndModelResults(projectId, selectionIds, selectionIntersection, modelIds, commonResults) {

  // Downloading project meta data, requiered to interprate the tree
  let projectMetadata = await getProjectMetadata(projectId, { considerResults: true })

  // Get the samples ID to pull
  let samplesToPull = await getProjectSamplesIdList(projectMetadata, selectionIds, selectionIntersection, modelIds, commonResults)

  // Download and convert the tree
  const { dataArray, sampleHashList } = await downloadTree(
    projectId,
    projectMetadata.timestamp,
    samplesToPull.samples
  )

  // =========== Then add the model results
  // Create a request
  let requestCode = services.uuid()
  store.commit("startRequest", { name: 'Loading the model results', code: requestCode, progress: 0 })

  try {
    let dataArrayFull = []
    let samplesToPullFull = []

    for (let i = 0; i < modelIds.length; i++) {
      const modelId = modelIds[i];

      let modelResults = await downloadResults(
        projectId,
        projectMetadata.timestamp,
        modelId,
        samplesToPull.samples
      )

      const dataAndResultsArray = [];
      const modelsSamplesToPull = [];

      // We now have a sample array and a list of results
      // We need to duplicate each one of the samples for each one of the results
      // ie : if a sample got evaluated on 3 models, there need to be 3 of this sample, each one
      // with his own model results

      sampleHashList.forEach((sampleId, i) => {
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
      sampleHashList: samplesToPullFull
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
      projectSamples = await loadTreeAndModelResults(
        projectId,
        selectionIds,
        selectionIntersection,
        modelIds,
        commomModelResults,
      )
    } else {
      projectSamples = await loadTree(
        projectId,
        selectionIds,
        selectionIntersection
      )
    }
    let metaData = projectSamples.metaData
    let array = projectSamples.array
    let sampleHashList = projectSamples.sampleHashList

    // Convert the the array in an column lists ready for analysing
    data = await arrayToJson(array, metaData);
    data.sampleHashList = sampleHashList

  }
  finally { endRequest(requestCode) }

  return data
}

export default { loadProjectSamples }

