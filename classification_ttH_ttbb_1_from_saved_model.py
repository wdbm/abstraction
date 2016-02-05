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
    --data=FILENAME          input ROOT data file [default: output_ttH.root]
"""
from __future__ import division

name    = "classification_ttH_ttbb_1_from_saved_model"
version = "2016-02-05T1623Z"
logo    = name

import docopt
import logging
import os
import sys
import time

import propyte
import pyprel
import shijian
import datavision
import abstraction
import ROOT

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
    ROOT_filename  = options["--data"]

    log.info("load classification model")

    classifier = abstraction.Classification(
        load_from_directory = "abstraction_classifier_ttH_ttbb_300000_50_200_400_50_300"
        #load_from_directory = "abstraction_classifier_ttH_ttbb_300000_50_150_250_300_400"
        #load_from_directory = "abstraction_classifier"
    )

    # Access data.
    data = abstraction.load_HEP_data(
        ROOT_filename            = ROOT_filename,
        tree_name                = "nominal",
        maximum_number_of_events = 5000
    )
    # Add class labels.
    if "ttH" in ROOT_filename:
        class_value = 1
    if "ttbb" in ROOT_filename:
        class_value = 0
    for index in data.indices():
        data.variable(index = index, name = "class", value = class_value)
    # Preprocess all data.
    data.preprocess_all()
    # Convert the datavision dataset to an abstraction dataset.
    dataset = abstraction.convert_HEP_datasets_from_datavision_datasets_to_abstraction_datasets(
        datasets = data
    )
    # Classify data and add the results to the datavision dataset.
    results = list(classifier._model.predict(dataset.features()))
    for count, index in enumerate(data.indices()):
        data.variable(index = index, name = "abstraction1", value = results[count])

    log.info(data.table())

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
