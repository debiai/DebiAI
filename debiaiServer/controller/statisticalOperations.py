import pandas as pd
import numpy as np
import numpy.random as nr

from scipy.stats import pearsonr, spearmanr
from scipy.special import digamma
import scipy.spatial as ss
from scipy.spatial import cKDTree
from math import log, fabs, sqrt


#  === Correlation matrix ===
def pearsonCorrelation(data):
    """Computes the Pearson's coefficient for every pair of variables provided

    Parameters
    ----------
    data: list of lists where each list contains the observations of a single variable
        : Array of rows with the same sizes (discrete & continuous)

    Return
    ------
    result: correlation matrix along with the p-value of the significance test of the coefficients
            significance level legend: 3(***) -> p-value<0.01 -> The coefficient is significant at 99%
                                        2(**) -> p-value<0.05 ->The coefficient is significant at 95%
                                         1(*) -> p-value<0.1  -> The coefficient is significant at 90%

    """

    for i in range(len(data) - 1):
        assert len(data[i]) == len(
            data[i + 1]
        ), "The provided samples should have the same length"
    # transform the list of samples to dataframe
    df = pd.DataFrame(data).transpose()
    rho = df.corr()  # calculate the correlation matrix
    pval = df.corr(method=lambda x, y: pearsonr(x, y)[1]) - np.eye(
        *rho.shape
    )  # calculate the p-value
    # return the number of *
    p = pval.applymap(lambda x: (len([i for t in [0.01, 0.05, 0.1] if x <= t])))
    ret = rho.values.tolist()
    for i in range(rho.shape[0]):
        for j in range(rho.shape[1]):
            ret[i][j] = [float(rho[i][j]), float(p[i][j])]
    return (
        ret,
        200,
    )  # pearson correlation matrix with the significance of the coefficient


def spearmanCorrelation(data):
    """
    Computes the Spearman's coefficient for every pair of variables provided

        Parameters
        ----------
        data: list of lists where each list contains the observations of a single variable

        Return
        ------
        result: correlation matrix along with the p-value of the significance test of the coefficients
                significance level legend: 3(***) -> p-value<0.01 -> The coefficient is significant at 99%
                                            2(**) -> p-value<0.05 ->The coefficient is significant at 95%
                                             1(*) -> p-value<0.1  -> The coefficient is significant at 90%

    """
    for i in range(len(data) - 1):
        assert len(data[i]) == len(
            data[i + 1]
        ), "The provided samples should have the same length"
    # transform the list of samples to dataframe
    df = pd.DataFrame(data).transpose()
    rho = df.corr(method="spearman")  # calculate the correlation matrix
    pval = df.corr(method=lambda x, y: spearmanr(x, y)[1]) - np.eye(
        *rho.shape
    )  # calculate the p-value
    # return the number of significant level
    p = pval.applymap(lambda x: (len([i for t in [0.01, 0.05, 0.1] if x <= t])))
    result = rho.values.tolist()
    for i in range(rho.shape[0]):
        for j in range(rho.shape[1]):
            result[i][j] = [float(rho[i][j]), float(p[i][j])]
    return result, 200


# === Mutual Information ===
def entropy_discrete(x, base=2):
    """
    Computes the entropy of a discrete random variable

    Parameters:
    -----------

    x: List or array of one variable.
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats

    Return:
    -------

    Output: A float: The value of the entropy
    """
    _, count = np.unique(x, return_counts=True, axis=0)
    probability = count.astype(float) / len(x)
    # Removing the elements which have 0 probability/weight to avoid log(0)
    probability = probability[probability > 0.0]
    return np.sum(-1 * probability * np.log(probability)) / np.log(base)


def entropy_discrete_xy(x, y, base=2):
    """
    Computes the entropy of the joint distribution of two discrete random variables

    Parameters:
    -----------
    x,y : Two random variables samples of the same length
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats

    Returns:
    --------

    Output: The value of the entropy: a float

    """
    assert len(x) == len(y), "The two provided samples should be of the same length"
    xy = np.c_[x, y]
    # construction of point :
    # Example :
    # (x,y)
    # [[1. 2.]
    # [2. 4.]
    # [3. 5.]]
    return entropy_discrete(xy, base)


def discrete_mutual_information(x, y, base=2):
    """
    Computes the mutual information of two discrete random variables: x,y

    Parameters:
    -----------

    x,y: Two random variable samples of the same length
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats

    Returns:
    -------

    Output: The value of the mutual information
    """
    assert len(x) == len(y), "The two provided samples should be of the same length"
    return (
        entropy_discrete(x, base)
        + entropy_discrete(y, base)
        - entropy_discrete_xy(x, y, base)
    )


def continuous_mutual_information(x, y, k=1, base=2):
    """
    Computes the mutual information between two continuous random variables

    Parameters:
    -----------
    x,y: Data: lists or numpy arrays
    k: the number of neighbors to consider
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats

    Returns:
    --------

    Output: the mutual information
    """
    x, y = np.asarray(x), np.asarray(y)
    x, y = x.reshape(x.shape[0], -1), y.reshape(y.shape[0], -1)
    x = x + 1e-10 * np.random.random_sample(x.shape)
    y = y + 1e-10 * np.random.random_sample(y.shape)
    xy = np.c_[x, y]
    x_tree = cKDTree(x)
    y_tree = cKDTree(y)
    xy_tree = cKDTree(xy)
    # query with k=k+1 to return the nearest neighbor, not counting the data point itself
    dist, _ = xy_tree.query(xy, k=k + 1, p=np.inf)
    epsilon = dist[:, -1]

    # for each point, count the number of neighbors
    # whose distance in the x-subspace is strictly < epsilon
    # repeat for the y subspace
    n = len(x)
    nx = np.empty(n, dtype=np.int)
    ny = np.empty(n, dtype=np.int)
    for ii in range(n):
        if epsilon[ii] <= 1e-10:
            nx[ii] = len(x_tree.query_ball_point(x_tree.data[ii], r=1e-9, p=np.inf)) - 1
            ny[ii] = len(y_tree.query_ball_point(y_tree.data[ii], r=1e-9, p=np.inf)) - 1
        else:
            nx[ii] = (
                len(
                    x_tree.query_ball_point(
                        x_tree.data[ii], r=epsilon[ii] - 1e-9, p=np.inf
                    )
                )
                - 1
            )
            ny[ii] = (
                len(
                    y_tree.query_ball_point(
                        y_tree.data[ii], r=epsilon[ii] - 1e-9, p=np.inf
                    )
                )
                - 1
            )

    mi = (
        digamma(k) - np.mean(digamma(nx + 1) + digamma(ny + 1)) + digamma(n)
    ) / np.log(
        base
    )  # version (1) in krakow scientific paper

    return mi


def mixed_mutual_information(c, d, n_neighbors, base=10):
    """
    Compute mutual information between continuous and discrete variables.

    Parameters
    ----------
    c : ndarray, shape (n_samples,)
        Samples of a continuous random variable.
    d : ndarray, shape (n_samples,)
        Samples of a discrete random variable.
    n_neighbors : int
        Number of nearest neighbors to search for each point
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats


    Returns:
    --------
    Output: The mutual information value
    """
    from sklearn.neighbors import NearestNeighbors

    n_samples = c.shape[0]
    c = c.reshape((-1, 1))

    radius = np.empty(n_samples)
    label_counts = np.empty(n_samples)
    k_all = np.empty(n_samples)
    nn = NearestNeighbors()
    for label in np.unique(d):
        mask = d == label
        count = np.sum(mask)
        if count > 1:
            k = min(n_neighbors, count - 1)
            nn.set_params(n_neighbors=k)
            nn.fit(c[mask])
            r = nn.kneighbors()[0]
            # print(r)
            radius[mask] = np.nextafter(r[:, -1], 0)
            # print(radius)
            k_all[mask] = k
        label_counts[mask] = count

    # Ignore points with unique labels.
    mask = label_counts > 1
    n_samples = np.sum(mask)
    label_counts = label_counts[mask]
    k_all = k_all[mask]
    c = c[mask]
    radius = radius[mask]

    nn.set_params(algorithm="kd_tree")
    nn.fit(c)
    ind = nn.radius_neighbors(radius=radius, return_distance=False)
    m_all = np.array([i.size for i in ind])

    mi = (
        digamma(n_samples)
        + np.mean(digamma(k_all))
        - np.mean(digamma(label_counts))
        - np.mean(digamma(m_all + 1))
    )

    return mi / log(base)


def normalise_function(normalise, mutual_information, entropy_X, entropy_Y):
    """
    normalize the mutual information coefficient
    Parameters:
    -----------
    normalize: the choice of normalize function : takes either 'max' or 'min' or 'square root' or 'mean' or 'none'
    mutual_information: mutual information coefficient
    entropy_X: the entropy of the first variable
    entropy_Y: the entropy of the second variable
    Returns:
    -------
    Output:
    The value of the normalized mutual information coefficient
    """
    if normalise == "none":
        ratio = 1
    elif normalise == "max":
        ratio = max(entropy_X, entropy_Y)
    elif normalise == "min":
        ratio = min(entropy_X, entropy_Y)
    elif normalise == "square root":
        ratio = sqrt(np.abs(entropy_X * entropy_Y))
    elif normalise == "mean":
        ratio = (entropy_X + entropy_Y) / 2
    else:
        raise NotImplementedError(
            "Variable 'normalise' takes only 'max' or 'min' or 'square root' or 'mean' or 'none'"
        )

    return mutual_information / ratio


def continuous_iterate_function(list_continuous, k=3, base=3, normalise="none"):
    """
      Parameters:
     -----------
    list_continuous: list of list of the continuous variables
    k: the number of neighbors to consider
     base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats
     normalise: the choice of normalize function : takes either 'max' or 'min' or 'square root' or 'mean' or 'none'

     Returns:
     -------
     Output:
     an array of the mutual information between the continuous variables
    """
    continuous = np.eye(len(list_continuous), len(list_continuous)).tolist()
    for i in range(len(continuous)):
        for j in range(i, len(continuous)):
            continuous[i][j] = continuous[j][i] = normalise_function(
                normalise,
                continuous_mutual_information(
                    list_continuous[i], list_continuous[j], k=k, base=base
                ),
                continuous_mutual_information(
                    list_continuous[i], list_continuous[i], k=k, base=base
                ),
                continuous_mutual_information(
                    list_continuous[j], list_continuous[j], k=k, base=base
                ),
            )
    return continuous


def discrete_iterate_function(list_discrete, base=10, normalise="none"):
    """
     Parameters:
     -----------
    list_discrete: list of list of the discrete variables
    k: the number of neighbors to consider
     base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats
     normalise: the choice of normalize function : takes either 'max' or 'min' or 'square root' or 'mean' or 'none'

     Returns:
     -------
     Output:
     an array of the mutual information between the discrete variables
    """
    discrete = np.eye(len(list_discrete), len(list_discrete)).tolist()
    for i in range(len(discrete)):
        for j in range(i, len(discrete)):
            discrete[i][j] = discrete[j][i] = normalise_function(
                normalise,
                discrete_mutual_information(
                    list_discrete[i], list_discrete[j], base=base
                ),
                entropy_discrete(list_discrete[i], base=base),
                entropy_discrete(list_discrete[j], base=base),
            )
    return discrete


def mixed_iterate_function(
    list_continuous, list_discrete, base=10, k=3, normalise="none"
):
    """
     Parameters:
    -----------
    list_continuous: list of list of the continuous variables
    list_discrete: list of list of the discrete variables
    k: the number of neighbors to consider
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats
    normalise: the choice of normalize function : takes either 'max' or 'min' or 'square root' or 'mean' or 'none'

    Returns:
    -------
    Output:
    an array of the mutual information between the all variables: the continuous and the discrete ones
    """
    mixed = np.eye(len(list_continuous), len(list_discrete)).tolist()
    for i in range(len(list_continuous)):
        for j in range(len(list_discrete)):
            mixed[i][j] = normalise_function(
                normalise,
                mixed_mutual_information(
                    np.array(list_continuous[i]),
                    np.array(list_discrete[j]),
                    n_neighbors=k,
                    base=base,
                ),
                continuous_mutual_information(
                    list_continuous[i], list_continuous[i], k=k, base=base
                ),
                entropy_discrete(list_discrete[j], base=base),
            )
    mixed = pd.DataFrame(mixed)
    continuous = continuous_iterate_function(
        list_continuous, k=k, base=base, normalise=normalise
    )
    continuous = pd.DataFrame(continuous)
    discrete = discrete_iterate_function(list_discrete, base=base, normalise=normalise)
    discrete = pd.DataFrame(discrete)
    part1 = np.concatenate((continuous, mixed), axis=1)
    part2 = np.concatenate((mixed.T, discrete), axis=1)
    result = np.concatenate((part1, part2), axis=0)
    return result.tolist()


# @utils.traceLogLight
def mutualInformation(data):
    """
     the global matrix of mutual information
    Parameters:
    -----------
    list_continuous: list of list of the continuous variables, if there is no
    continuous variables, please send an empty list of list [[]]
    list_discrete: list of list of the discrete variables,if there is no discrete
    variables, please send an empty list of list [[]]
    k: the number of neighbors to consider
    base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats
    normalise: the choice of normalize function : takes either 'max' or 'min'
    or 'square root' or 'mean' or 'none'

    Returns:
    -------
    Output:
    an array of the mutual information between the variables: the continuous
    ones only, the discrete ones only or the continuous and the discrete ones
    """
    k = data["k"]
    list_continuous = data["list_continuous"]
    list_discrete = data["list_discrete"]

    if k >= len(list_continuous) + len(list_discrete):
        return "k must be lower than the number of variables", 403

    if "base" in data:
        base = data["base"]
    else:
        base = 2

    if "normalise" in data:
        normalise = data["normalise"]
        acceptedNormalise = ["max", "min", "square root", "mean", "none"]

        if normalise not in acceptedNormalise:
            return (
                "normalise need to be either 'max' or 'min' or 'square root' or 'mean' or 'none'",
                403,
            )
    else:
        normalise = "max"

    # Calculate mutual information between features
    if list_continuous != [[]] and list_discrete == [[]]:
        return continuous_iterate_function(
            list_continuous, k=k, base=base, normalise=normalise
        )
    elif list_continuous == [[]] and list_discrete != [[]]:
        return discrete_iterate_function(list_discrete, base=base, normalise=normalise)
    elif list_continuous != [[]] and list_discrete != [[]]:
        return mixed_iterate_function(
            list_continuous, list_discrete, base=base, k=k, normalise=normalise
        )
    else:
        return "The lists are empty", 403


# === Mutual Information higher dimension ===
def averageDigamma(points, dvec):
    """
    This part finds number of neighbors in some radius in the marginal space

    Parameters:
    ----------

    points: the data observed
    dvec: A distance vector between points

    Returns:
    --------
    Output: expectation value of <psi(nx)>

    """

    N = len(points)
    tree = ss.cKDTree(points)
    avg = 0.0
    for i in range(N):
        dist = dvec[i]
        # subtlety, we don't include the boundary point,
        # but we are implicitly adding 1 to kraskov definition because center point is included
        num_points = len(tree.query_ball_point(points[i], dist - 1e-15, p=float("inf")))
        avg += digamma(num_points) / N
    return avg


# @utils.traceLogLight
def higherDimensionMutualInformation(data):
    """
    This function calculates the mutual information between several continuous
    variables (3, 4 variables). It takes as input a list of lists [[variable1],
    [variable2], [variable3], ...], the number K, and the base, either 2 or 10
    (the unit of information is respectively bits or nats).

    It returns the mutual information between the different variables.

    Regarding its representation in the tool, we can simply create a small window
    where we select the variables, K, and the base, and display only the result.
    Alternatively, in your 3D plot window, we can add the result of the mutual
    information of the 3 variables below the graph.

    The mutual information estimator by Kraskov et al.
    ith row of X represents ith dimension of the data, e.g. X = [[1.0,3.0,3.0],[0.1,1.2,5.4]],
    if X has two dimensions and we have three samples
    Parameters:
    ----------
        X: list of list of the variables : it could take more than 2 variables
        k: the number of neighbors to consider
        base: The base in which the entropy value is represented, i.e 2 for bits, 10 for nats

    Returns:
    --------
        Output: the mutual information between the variables
    """

    X = data["X"]
    k = data["k"]
    if k >= len(X):
        return "k must be < to len(X)", 403

    if "base" in data:
        base = data["base"]
    else:
        base = 2

    # adding small noise to X, e.g., x<-X+noise
    x = []
    for i in range(len(X)):
        tem = []
        for j in range(len(X[i])):
            tem.append([X[i][j] + 1e-10 * nr.rand(1)[0]])
        x.append(tem)

    points = []
    for j in range(len(x[0])):
        tem = []
        for i in range(len(x)):
            tem.append(x[i][j][0])
        points.append(tem)
    tree = ss.cKDTree(points)
    dvec = []
    for i in range(len(x)):
        dvec.append([])
    for point in points:
        # Find k-nearest neighbors in joint space, p=inf means max norm
        knn = tree.query(point, k + 1, p=float("inf"))
        points_knn = []
        for i in range(len(x)):
            dvec[i].append(float("-inf"))
            points_knn.append([])
        for j in range(k + 1):
            for i in range(len(x)):
                points_knn[i].append(points[knn[1][j]][i])

        # Find distances to k-nearest neighbors in each marginal space
        for i in range(k + 1):
            for j in range(len(x)):
                if dvec[j][-1] < fabs(points_knn[j][i] - points_knn[j][0]):
                    dvec[j][-1] = fabs(points_knn[j][i] - points_knn[j][0])

    ret = 0.0
    for i in range(len(x)):
        ret -= averageDigamma(x[i], dvec[i])
    ret += (
        digamma(k)
        - (float(len(x)) - 1.0) / float(k)
        + (float(len(x)) - 1.0) * digamma(len(x[0]))
    )
    if base == 2:
        mul = 1 / log(2)  # scaling factor from nats to bits
        ret *= mul
    return ret

    pass


# === Mutual Information matrix & Mutual Information higher dimension ===
def mutualAndHigherInformation(data):
    """
    calculate the mutual information estimator by Kraskov et al.
    and the global matrix of mutual information
    """

    k = data["k"]
    list_continuous = data["list_continuous"]
    list_discrete = data["list_discrete"]
    columns = list_continuous + list_discrete
    if "base" in data:
        base = data["base"]
    else:
        base = 2

    if "normalise" in data:
        normalise = data["normalise"]
    else:
        normalise = "max"

    if k >= len(columns):
        return "k need to be < len(X)", 403

    # higherDimensionMutualInformation
    print("higherDimensionMutualInformation")
    hdmi = higherDimensionMutualInformation(
        {"k": k, "base": base, "X": list_continuous + list_discrete}
    )

    # mutualInformation
    print("mutualInformation")
    mi = mutualInformation(
        {
            "k": k,
            "base": base,
            "list_continuous": list_continuous,
            "list_discrete": list_discrete,
            "normalise": normalise,
        }
    )

    return {"higherDimensionMutualInformation": hdmi, "mutualInformation": mi}, 200
