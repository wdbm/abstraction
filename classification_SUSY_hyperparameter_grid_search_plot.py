#!/usr/bin/env python
# coding=utf-8

"""
################################################################################
#                                                                              #
# classification_SUSY_hyperparameter_grid_search_plot                          #
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
    -h, --help                 display help message
    --version                  display version and exit
    -v, --verbose              verbose logging
    -s, --silent               silent
    -u, --username=USERNAME    username
    --gridsearchfile=FILENAME  input grid search filename
                               [default: grid_search_map.pkl]
"""
from __future__ import division

name    = "classification_SUSY_hyperparameter_grid_search_plot"
version = "2016-02-03T1404Z"
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
import datavision

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
    grid_search_filename = options["--gridsearchfile"]

    # load grid search map
    grid_search_map = shijian.import_object(filename = grid_search_filename)

    number_of_entries = len(grid_search_map["epoch"])
    log.info("number of entries: {number_of_entries}".format(
        number_of_entries = number_of_entries
    ))

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
    log.info("\ngrid search map:\n")
    log.info(
        pyprel.Table(
            contents = table_contents,
        )
    )

    # parallel coordinates plot

    number_of_entries = len(grid_search_map["epoch"])
    datasets = []
    for index in range(0, number_of_entries):
        row = []
        architecture_padded = grid_search_map["hidden_nodes"][index] + [0] * (5 - len(grid_search_map["hidden_nodes"][index]))
        row.append(grid_search_map["epoch"][index])
        row.extend(architecture_padded)
        row.append(grid_search_map["score_training"][index])
        row.append(grid_search_map["score_test"][index])
        datasets.append(row)

    datavision.save_parallel_coordinates_matplotlib(
        datasets[::-1],
        filename = "parallel_coordinates.png"
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
    
    matplotlib.pyplot.legend(
        loc            = "center left",
        bbox_to_anchor = (1, 0.5),
        fontsize       = 10
    )

    matplotlib.pyplot.savefig(
        "hyperparameter_map.eps",
        bbox_inches = "tight",
        format      = "eps"
    )

    # find best-scoring models

    # Find the 15 best scores and plot them using parallel coordinates.
    best_models = sorted(zip(
        grid_search_map["score_test"],
        grid_search_map["score_training"],
        grid_search_map["hidden_nodes"]),
        reverse = True
    )[:15]
    datasets = []
    for model in best_models:
        row = []
        architecture_padded = model[2] + [0] * (5 - len(model[2]))
        row.extend(architecture_padded)
        row.append(model[1])
        row.append(model[0])
        datasets.append(row)

    datavision.save_parallel_coordinates_matplotlib(
        datasets,
        filename = "15_best_models_parallel_coordinates.png"
    )

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
    log.info("\nbest-scoring models:\n")
    log.info(
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
