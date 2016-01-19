#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# classification_ttH_ttbb_1                                                    #
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
"""
from __future__ import division

name    = "classification_ttH_ttbb_1"
version = "2016-01-19T1524Z"
logo    = name

import os
import sys
import time
import docopt
import logging
import propyte
import shijian
import datavision
import abstraction
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
    ROOT_filename_ttH = options["--datattH"]
    ROOT_filename_ttbb = options["--datattbb"]

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
            data_ttbb.variable(name = "el_1_pt"),
            data_ttbb.variable(name = "el_1_eta"),
            data_ttbb.variable(name = "el_1_phi"),
            data_ttbb.variable(name = "jet_1_pt"),
            data_ttbb.variable(name = "jet_1_eta"),
            data_ttbb.variable(name = "jet_1_phi"),
            data_ttbb.variable(name = "jet_1_e"),
            data_ttbb.variable(name = "jet_2_pt"),
            data_ttbb.variable(name = "jet_2_eta"),
            data_ttbb.variable(name = "jet_2_phi"),
            data_ttbb.variable(name = "jet_2_e"),
            data_ttbb.variable(name = "met"),
            data_ttbb.variable(name = "met_phi"),
            data_ttbb.variable(name = "nJets"),
            data_ttbb.variable(name = "Centrality_all"),
            #data_ttbb.variable(name = "Mbb_MindR")
        ])
        _data.append([
            data_ttbb.variable(name = "class")
        ])
    for index in data_ttH.indices():
        _data.append([
            data_ttH.variable(name = "el_1_pt"),
            data_ttH.variable(name = "el_1_eta"),
            data_ttH.variable(name = "el_1_phi"),
            data_ttH.variable(name = "jet_1_pt"),
            data_ttH.variable(name = "jet_1_eta"),
            data_ttH.variable(name = "jet_1_phi"),
            data_ttH.variable(name = "jet_1_e"),
            data_ttH.variable(name = "jet_2_pt"),
            data_ttH.variable(name = "jet_2_eta"),
            data_ttH.variable(name = "jet_2_phi"),
            data_ttH.variable(name = "jet_2_e"),
            data_ttH.variable(name = "met"),
            data_ttH.variable(name = "met_phi"),
            data_ttH.variable(name = "nJets"),
            data_ttH.variable(name = "Centrality_all"),
            #data_ttH.variable(name = "Mbb_MindR")
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
    log.info("define classification model")

    # define model

    classifier = abstraction.Classification(
        number_of_classes = 2,
        hidden_nodes      = [200, 300, 300, 300, 200],
        epochs            = 100
    )

    # train model

    log.info("fit classification model to dataset features and targets")
    classifier._model.fit(features_train, targets_train)
    #classifier.save()

    # predict and cross-validate training

    log.info("test trained classification model on training dataset")
    score = metrics.accuracy_score(
        classifier._model.predict(features_train),
        targets_train
    )
    log.info("prediction accuracy on training dataset: {percentage}".format(
        percentage = 100 * score
    ))
    log.info("accuracy of classifier on test dataset:")
    score = metrics.accuracy_score(
        classifier._model.predict(features_test),
        targets_test
    )
    log.info("prediction accuracy on test dataset: {percentage}".format(
        percentage = 100 * score
    ))

    log.info("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
