#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# classification_ttH_ttbb_1_from_saved_model                                   #
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

name    = "classification_ttH_ttbb_1_from_saved_model"
version = "2016-01-20T1357Z"
logo    = name

import os
import sys
import time
import docopt
import logging
import propyte
import pyprel
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

    # Preprocess all data.

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

    log.info("load classification model")

    classifier = abstraction.Classification(
        load_from_directory = "abstraction_classifier"
    )

    log.info("split data for cross-validation")
    features_train, features_test, targets_train, targets_test =\
        cross_validation.train_test_split(
            dataset.features(),
            dataset.targets(),
            train_size = 0.7
        )

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

    table_contents = [["target", "prediction"]]
    for value_target, value_prediction in zip(
        dataset.targets(),
        list(classifier._model.predict(dataset.features()))
    ):
        row = [str(value_target[0]), str(value_prediction)]
        table_contents.append(row)
    print(pyprel.Table(
        contents              = table_contents,
        table_width_requested = 22
    ))

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
