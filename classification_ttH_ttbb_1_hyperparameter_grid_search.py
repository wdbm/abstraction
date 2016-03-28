#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# classification_ttH_ttbb_1_hyperparameter_grid_search                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is for classification training on ttH and ttbb HEP MC           #
# events.                                                                      #
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
    --datattH=FILENAME       input ROOT data file [default: output_ttH.root]
    --datattbb=FILENAME      input ROOT data file [default: output_ttbb.root]
    --plot=BOOL              plot variables       [default: true]
"""
from __future__ import division

name    = "classification_ttH_ttbb_1_hyperparameter_grid_search"
version = "2016-03-28T1816Z"
logo    = name

import docopt
import logging
import matplotlib
import os
import sys
import time

import abstraction
import datavision
import propyte
import pyprel
import shijian
from sklearn import metrics
from sklearn import cross_validation

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

    # access options and arguments
    ROOT_filename_ttH  = options["--datattH"]
    ROOT_filename_ttbb = options["--datattbb"]
    engage_plotting    = string_to_bool(options["--plot"])

    log.info("ttH data file: {filename}".format(
        filename = ROOT_filename_ttH
    ))
    log.info("ttbb data file: {filename}".format(
        filename = ROOT_filename_ttbb
    ))

    # Access data for event classes ttbb and ttH.

    data_ttbb = abstraction.load_HEP_data(
        ROOT_filename            = ROOT_filename_ttbb,
        tree_name                = "nominal",
        maximum_number_of_events = None
    )

    data_ttH = abstraction.load_HEP_data(
        ROOT_filename            = ROOT_filename_ttH,
        tree_name                = "nominal",
        maximum_number_of_events = None
    )

    if engage_plotting is True:

        # Plot the loaded datasets.

        for variable_name in data_ttbb.variables():
            log.info("plot ttbb versus ttH comparison of {variable_name}".format(
                variable_name = variable_name
            ))
            datavision.save_histogram_comparison_matplotlib(
                values_1      = data_ttbb.values(name = variable_name),
                values_2      = data_ttH.values(name = variable_name),
                label_1       = variable_name + "_ttbb",
                label_2       = variable_name + "_ttH",
                normalize     = True,
                label_ratio_x = "frequency",
                label_y       = "",
                title         = variable_name + "_ttbb_ttH",
                filename      = variable_name + "_ttbb_ttH.png"
            )

    # upcoming: consider data ordering

    # Preprocess all data (to be updated).

    data_ttbb.preprocess_all()
    data_ttH.preprocess_all()

    # Add class labels to the data sets, 0 for ttbb and 1 for ttH.

    for index in data_ttbb.indices():
        data_ttbb.variable(index = index, name = "class", value = 0)

    for index in data_ttH.indices():
        data_ttH.variable(index = index, name = "class", value = 1)

    # Convert the data sets to a simple list format with the first column
    # containing the class label.
    _data = []
    for index in data_ttbb.indices():
        _data.append([
            data_ttbb.variable(index = index, name = "el_1_pt"),
            data_ttbb.variable(index = index, name = "el_1_eta"),
            data_ttbb.variable(index = index, name = "el_1_phi"),
            data_ttbb.variable(index = index, name = "jet_1_pt"),
            data_ttbb.variable(index = index, name = "jet_1_eta"),
            data_ttbb.variable(index = index, name = "jet_1_phi"),
            data_ttbb.variable(index = index, name = "jet_1_e"),
            data_ttbb.variable(index = index, name = "jet_2_pt"),
            data_ttbb.variable(index = index, name = "jet_2_eta"),
            data_ttbb.variable(index = index, name = "jet_2_phi"),
            data_ttbb.variable(index = index, name = "jet_2_e"),
            data_ttbb.variable(index = index, name = "met"),
            data_ttbb.variable(index = index, name = "met_phi"),
            data_ttbb.variable(index = index, name = "nJets"),
            data_ttbb.variable(index = index, name = "Centrality_all"),
            #data_ttbb.variable(index = index, name = "Mbb_MindR")
        ])
        _data.append([
            data_ttbb.variable(name = "class")
        ])
    for index in data_ttH.indices():
        _data.append([
            data_ttH.variable(index = index, name = "el_1_pt"),
            data_ttH.variable(index = index, name = "el_1_eta"),
            data_ttH.variable(index = index, name = "el_1_phi"),
            data_ttH.variable(index = index, name = "jet_1_pt"),
            data_ttH.variable(index = index, name = "jet_1_eta"),
            data_ttH.variable(index = index, name = "jet_1_phi"),
            data_ttH.variable(index = index, name = "jet_1_e"),
            data_ttH.variable(index = index, name = "jet_2_pt"),
            data_ttH.variable(index = index, name = "jet_2_eta"),
            data_ttH.variable(index = index, name = "jet_2_phi"),
            data_ttH.variable(index = index, name = "jet_2_e"),
            data_ttH.variable(index = index, name = "met"),
            data_ttH.variable(index = index, name = "met_phi"),
            data_ttH.variable(index = index, name = "nJets"),
            data_ttH.variable(index = index, name = "Centrality_all"),
            #data_ttH.variable(index = index, name = "Mbb_MindR")
        ])
        _data.append([
            data_ttH.variable(name = "class")
        ])
    dataset = abstraction.Dataset(data = _data)

    log.info("")

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

    epochs       = [100, 100000]
    architecture = [200, 300, 300, 200]

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
                pyprel.print_line()
                grid_search_map["epoch"].append(epoch)
                grid_search_map["hidden_nodes"].append(hidden_nodes)
                grid_search_map["score_training"].append(score_training)
                grid_search_map["score_test"].append(score_test)

                # save current grid search map
                shijian.export_object(
                    grid_search_map,
                    filename  = "grid_search_map.pkl",
                    overwrite = True
                )

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

def string_to_bool(x):
    return x.lower() in ("yes", "true", "t", "1")

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
