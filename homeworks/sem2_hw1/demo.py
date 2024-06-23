import time
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from algorithms.knn import KNN
from algorithms.nonparametric_regression import NPR
from metric_distances import MAE, MSE, rr, accuracy
from precompilation import train_test_split
import sklearn.datasets as skd

from utils import (
    visualize_comparison,
    freeze_random_seed,
    Colors,
    visualize_results,
    visualize_distribution
)

K_NEIGHBOURS = 5
POINTS_AMOUNT = 1000
BOUNDS = (-10, 10)
FIGSIZE = (16, 8)


def preporc_viz(counts: int, graph: str = '') -> None:
    if counts == 1:
        data = np.random.normal(size=1000)
        if graph == 'hist':
            figure, axis = plt.subplots(figsize=(16, 9))
            visualize_distribution([axis], data, graph,
                                   path_to_save="./homeworks/sem2_hw1/images/hist")
        elif graph == 'boxplot':
            figure, axis = plt.subplots(figsize=(16, 4))
            visualize_distribution([axis], data, graph,
                                   path_to_save="./homeworks/sem2_hw1/images/boxplot")
        elif graph == 'violin':
            figure, axis = plt.subplots(figsize=(16, 4))
            visualize_distribution([axis], data, graph,
                                   path_to_save="./homeworks/sem2_hw1/images/violin")
    elif counts == 2:
        mean = [2, 3]
        cov = [[1, 1], [1, 2]]
        space = 0.2
        abscissa, ordinates = np.random.multivariate_normal(mean, cov, size=1000).T
        figure = plt.figure(figsize=(8, 8))
        grid = plt.GridSpec(4, 4, wspace=space, hspace=space)

        axis_scatter = figure.add_subplot(grid[:-1, 1:])
        axis_hist_vert = figure.add_subplot(
            grid[:-1, 0],
            sharey=axis_scatter,
        )
        axis_hist_hor = figure.add_subplot(
            grid[-1, 1:],
            sharex=axis_scatter,
        )
        abcissa = np.reshape(abscissa, (len(abscissa), 1))
        ordinate = np.reshape(ordinates, (len(ordinates), 1))
        data = np.concatenate((abcissa, ordinate), axis=-1)
        visualize_distribution(
            [axis_scatter, axis_hist_hor, axis_hist_vert],
            data, graph, path_to_save="./homeworks/sem2_hw1/images/2Dprecomp"
        )


def get_demonstration(
    function: Callable[[np.ndarray], np.ndarray],
    regressors: list[NPR],
    path_to_save: str = '',
) -> None:
    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = function(abscissa)

    for regressor in regressors:
        regressor.fit(abscissa, ordinates)

    _, axes = plt.subplots(1, 1, figsize=(8, 8))
    for regressor in regressors:
        predictions = regressor.predict(abscissa)
        axes.set_title(type(regressor).__name__, fontweight='bold')
        abscissa_error = abscissa
        ordinates_error_low = ordinates - 10
        ordinates_error_up = ordinates + 10
        visualize_results(
            axes, abscissa, ordinates, predictions, abcissa_error=abscissa_error,
            ordinates_error_lower=ordinates_error_low,
            ordinates_error_upper=ordinates_error_up, path_to_save=path_to_save
        )

        print(f"MSE = {MSE(predictions, ordinates)}",
              f"MAE = {MAE(predictions, ordinates)}",
              f"rr = {rr(predictions, ordinates)}",
              sep='\n')

    plt.show()


def main() -> None:
    functions = [linear, linear_modulated]
    regressors = [NPR(5, "l1")]
    pathes_to_save = ["./homeworks/sem2_hw1/images/regression1.png",
                      "./homeworks/sem2_hw1/images/regression2.png"]
    for i, function in enumerate(functions):
        get_demonstration(function, regressors, path_to_save=pathes_to_save[i])


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


if __name__ == '__main__':
    preporc_viz(1, 'boxplot')
    freeze_random_seed()
    points, labels = skd.make_moons(n_samples=400, noise=0.3)
    points_train, points_test, labels_train, labels_test = train_test_split(
        features=points,
        targets=labels,
        shuf=True,
        train_ratio=0.8,
    )
    knn = KNN(2, 'l2')
    points_train = np.array([[1, 2], [2, 5], [3, 6], [3, 5], [4, 2], [4, 5], [2, 8], [6, 10],])
    labels_train = np.array([1, 0, 2, -1, 2, 7, 8, 9])
    points_test = np.array([[4, 5], [2, 4], [6, 7], [5, 6], [7, 9], [1, 2], [2, 3], [3, 4]])
    knn.fit(points_train, labels_train)
    prediction = knn.predict(points_test)

    labels_test = np.array([1, 0, 2, 4, 5, 7, 9, 10])
    visualize_comparison(
        points_test, prediction, labels_test, [color.value for color in Colors],
        path_to_save='./homeworks/sem2_hw1/images/knn.png'
    )
    accuracy_score = accuracy(prediction, labels_test)

    print(f"knn accuracy: {accuracy_score}")

    time.sleep(3)

    main()
