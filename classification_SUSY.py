#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# classification_SUSY                                                          #
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

name    = "classification_SUSY"
version = "2015-12-05T0646Z"
logo    = name

import os
import sys
import time
import docopt
import logging
import propyte
from sklearn import metrics
from sklearn import cross_validation
import abstraction

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
    log.info("define classification model")

    # define model

    classifier = abstraction.Classification(
        number_of_classes = 2,
        hidden_nodes      = [20, 30, 20],
        epochs            = 500
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
