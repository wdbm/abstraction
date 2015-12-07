#!/usr/bin/env python
# coding=utf-8

"""
################################################################################
#                                                                              #
# classification_SUSY_hyperparameter_grid_search                               #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a classification example using the SUSY data set.            #
#                                                                              #
# copyright (C) 2015 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
"""
from __future__ import division

name    = "classification_SUSY_hyperparameter_grid_search"
version = "2015-12-07T0055Z"
logo    = name

import os
import sys
import time
import docopt
import logging
import pickle
import propyte
import pyprel
import shijian
import matplotlib
import matplotlib.pyplot
from sklearn import metrics
from sklearn import cross_validation
import abstraction

def composite_variable(x):
    k = len(x) + 1
    variable = 0
    for index, element in enumerate(x):
        variable += k**(index - 1) * element
    return variable

def main(options):

    global program
    program = propyte.Program(
        options = options,
        name    = name,
        version = version,
        logo    = logo
        )
    global log
    from propyte import log

    log.info("")

    # define dataset

    # Load the SUSY dataset (https://archive.ics.uci.edu/ml/datasets/SUSY). 
    # The first column is the class label (1 for signal, 0 for background),
    # followed by 18 features (8 low-level features and 10 high-level features):
    #
    # - lepton 1 pT
    # - lepton 1 eta
    # - lepton 1 phi
    # - lepton 2 pT
    # - lepton 2 eta
    # - lepton 2 phi
    # - missing energy magnitude
    # - missing energy phi
    # - MET_rel
    # - axial MET
    # - M_R
    # - M_TR_2
    # - R
    # - MT2
    # - S_R
    # - M_Delta_R
    # - dPhi_r_b
    # - cos(theta_r1)

    data = abstraction.access_SUSY_dataset_format_file("SUSY_100k.csv")

    dataset = abstraction.Dataset(
        data = data
    )

    # define data

    log.info("split data for cross-validation")
    features_train, features_test, targets_train, targets_test =\
        cross_validation.train_test_split(
            dataset.features(),
            dataset.targets(),
            train_size = 0.7
        )

    # grid search

    import itertools

    #epochs       = [10, 100, 1000, 10000, 100000]
    #architecture = [10, 15, 20]

    epochs       = [20, 30, 40]
    architecture = [10, 15, 10]

    grid_search_map = {}
    grid_search_map["epoch"]          = []
    grid_search_map["hidden_nodes"]   = []
    grid_search_map["score_training"] = []
    grid_search_map["score_test"]     = []

    # define progress
    count_total = 0
    for epoch in epochs:
        for nodes_count in xrange(1, len(architecture) + 1):
            combinations = itertools.product(architecture, repeat = nodes_count)
            for combination in combinations:
                count_total += 1
    count = 0
    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()

    for epoch in epochs:
        for nodes_count in xrange(1, len(architecture) + 1):
            combinations = itertools.product(architecture, repeat = nodes_count)
            for combination in combinations:
                hidden_nodes = list(combination)

                # define model

                log.info("define classification model")
                classifier = abstraction.Classification(
                    number_of_classes = 2,
                    hidden_nodes      = hidden_nodes,
                    epochs            = epoch
                )
                
                # train model
                
                log.info("fit model to dataset features and targets")
                classifier._model.fit(features_train, targets_train)
                #classifier.save()
                
                # predict and cross-validate training
                
                log.info("test trained model on training dataset")
                score_training = metrics.accuracy_score(
                    classifier._model.predict(features_train),
                    targets_train
                )
                score_test = metrics.accuracy_score(
                    classifier._model.predict(features_test),
                    targets_test
                )
                log.info("\ntraining-testing instance complete:")
                log.info("epoch:          {epoch}".format(
                    epoch = epoch
                ))
                log.info("architecture:   {architecture}".format(
                    architecture = hidden_nodes
                ))
                log.info("score training: {score_training}".format(
                    score_training = 100 * score_training
                ))
                log.info("score test:     {score_test}".format(
                    score_test = 100 * score_test
                ))
                pyprel.printLine()
                grid_search_map["epoch"].append(epoch)
                grid_search_map["hidden_nodes"].append(hidden_nodes)
                grid_search_map["score_training"].append(score_training)
                grid_search_map["score_test"].append(score_test)

                # save current grid search map
                pickle.dump(grid_search_map, open("grid_search_map.pkl", "wb"))

                count += 1
                print(progress.add_datum(fraction = (count + 1) / count_total))

    number_of_entries = len(grid_search_map["epoch"])

    # table

    table_contents = [
        ["epoch", "architecture", "score training", "score testing"]
    ]
    for index in range(0, number_of_entries):
        table_contents.append(
            [
                str(grid_search_map["epoch"][index]),
                str(grid_search_map["hidden_nodes"][index]),
                str(grid_search_map["score_training"][index]),
                str(grid_search_map["score_test"][index])
            ]
        )
    print("\ngrid search map:\n")
    print(
        pyprel.Table(
            contents = table_contents,
        )
    )

    # plot

    architectures = shijian.unique_list_elements(grid_search_map["hidden_nodes"])

    architecture_epoch_score = {}
    for architecture in architectures:
        architecture_epoch_score[str(architecture)] = []
        for index in range(0, number_of_entries):
            if grid_search_map["hidden_nodes"][index] == architecture:
                architecture_epoch_score[str(architecture)].append(
                    [
                        grid_search_map["epoch"][index],
                        grid_search_map["score_test"][index]
                    ]
                )
    
    figure = matplotlib.pyplot.figure()
    figure.set_size_inches(10, 10)
    axes = figure.add_subplot(1, 1, 1)
    axes.set_xscale("log")
    figure.suptitle("hyperparameter map", fontsize = 20)
    matplotlib.pyplot.xlabel("epochs")
    matplotlib.pyplot.ylabel("training test score")

    for key, value in architecture_epoch_score.iteritems():
        epochs     = [element[0] for element in value]
        score_test = [element[1] for element in value]
        matplotlib.pyplot.plot(epochs, score_test, label = key)
    
    matplotlib.pyplot.legend(loc = "center right")

    matplotlib.pyplot.savefig(
        "hyperparameter_map.eps",
        bbox_inches = "tight",
        format      = "eps"
    )

    # find best-scoring models

    # Find the 3 best scores.
    best_models = sorted(zip(
        grid_search_map["score_test"],
        grid_search_map["hidden_nodes"]),
        reverse = True
    )[:3]

    # table
    table_contents = [["architecture", "score testing"]]
    for model in best_models:
        table_contents.append([str(model[1]), str(model[0])])
    print("\nbest-scoring models:\n")
    print(
        pyprel.Table(
            contents = table_contents,
        )
    )

    log.info("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
