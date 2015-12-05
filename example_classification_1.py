#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# example_classification_1                                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a classification example using the Iris flower data set.     #
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

name    = "example_classification_1"
version = "2015-12-05T0504Z"
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

    dataset = abstraction.Dataset(
        data =\
            [
            [5.1, 3.5, 1.4, 0.2], [0],
            [4.9, 3.0, 1.4, 0.2], [0],
            [4.7, 3.2, 1.3, 0.2], [0],
            [4.6, 3.1, 1.5, 0.2], [0],
            [5.0, 3.6, 1.4, 0.2], [0],
            [5.4, 3.9, 1.7, 0.4], [0],
            [4.6, 3.4, 1.4, 0.3], [0],
            [5.0, 3.4, 1.5, 0.2], [0],
            [4.4, 2.9, 1.4, 0.2], [0],
            [4.9, 3.1, 1.5, 0.1], [0],
            [5.4, 3.7, 1.5, 0.2], [0],
            [4.8, 3.4, 1.6, 0.2], [0],
            [4.8, 3.0, 1.4, 0.1], [0],
            [4.3, 3.0, 1.1, 0.1], [0],
            [5.8, 4.0, 1.2, 0.2], [0],
            [5.7, 4.4, 1.5, 0.4], [0],
            [5.4, 3.9, 1.3, 0.4], [0],
            [5.1, 3.5, 1.4, 0.3], [0],
            [5.7, 3.8, 1.7, 0.3], [0],
            [5.1, 3.8, 1.5, 0.3], [0],
            [5.4, 3.4, 1.7, 0.2], [0],
            [5.1, 3.7, 1.5, 0.4], [0],
            [4.6, 3.6, 1.0, 0.2], [0],
            [5.1, 3.3, 1.7, 0.5], [0],
            [4.8, 3.4, 1.9, 0.2], [0],
            [5.0, 3.0, 1.6, 0.2], [0],
            [5.0, 3.4, 1.6, 0.4], [0],
            [5.2, 3.5, 1.5, 0.2], [0],
            [5.2, 3.4, 1.4, 0.2], [0],
            [4.7, 3.2, 1.6, 0.2], [0],
            [4.8, 3.1, 1.6, 0.2], [0],
            [5.4, 3.4, 1.5, 0.4], [0],
            [5.2, 4.1, 1.5, 0.1], [0],
            [5.5, 4.2, 1.4, 0.2], [0],
            [4.9, 3.1, 1.5, 0.1], [0],
            [5.0, 3.2, 1.2, 0.2], [0],
            [5.5, 3.5, 1.3, 0.2], [0],
            [4.9, 3.1, 1.5, 0.1], [0],
            [4.4, 3.0, 1.3, 0.2], [0],
            [5.1, 3.4, 1.5, 0.2], [0],
            [5.0, 3.5, 1.3, 0.3], [0],
            [4.5, 2.3, 1.3, 0.3], [0],
            [4.4, 3.2, 1.3, 0.2], [0],
            [5.0, 3.5, 1.6, 0.6], [0],
            [5.1, 3.8, 1.9, 0.4], [0],
            [4.8, 3.0, 1.4, 0.3], [0],
            [5.1, 3.8, 1.6, 0.2], [0],
            [4.6, 3.2, 1.4, 0.2], [0],
            [5.3, 3.7, 1.5, 0.2], [0],
            [5.0, 3.3, 1.4, 0.2], [0],
            [7.0, 3.2, 4.7, 1.4], [1],
            [6.4, 3.2, 4.5, 1.5], [1],
            [6.9, 3.1, 4.9, 1.5], [1],
            [5.5, 2.3, 4.0, 1.3], [1],
            [6.5, 2.8, 4.6, 1.5], [1],
            [5.7, 2.8, 4.5, 1.3], [1],
            [6.3, 3.3, 4.7, 1.6], [1],
            [4.9, 2.4, 3.3, 1.0], [1],
            [6.6, 2.9, 4.6, 1.3], [1],
            [5.2, 2.7, 3.9, 1.4], [1],
            [5.0, 2.0, 3.5, 1.0], [1],
            [5.9, 3.0, 4.2, 1.5], [1],
            [6.0, 2.2, 4.0, 1.0], [1],
            [6.1, 2.9, 4.7, 1.4], [1],
            [5.6, 2.9, 3.6, 1.3], [1],
            [6.7, 3.1, 4.4, 1.4], [1],
            [5.6, 3.0, 4.5, 1.5], [1],
            [5.8, 2.7, 4.1, 1.0], [1],
            [6.2, 2.2, 4.5, 1.5], [1],
            [5.6, 2.5, 3.9, 1.1], [1],
            [5.9, 3.2, 4.8, 1.8], [1],
            [6.1, 2.8, 4.0, 1.3], [1],
            [6.3, 2.5, 4.9, 1.5], [1],
            [6.1, 2.8, 4.7, 1.2], [1],
            [6.4, 2.9, 4.3, 1.3], [1],
            [6.6, 3.0, 4.4, 1.4], [1],
            [6.8, 2.8, 4.8, 1.4], [1],
            [6.7, 3.0, 5.0, 1.7], [1],
            [6.0, 2.9, 4.5, 1.5], [1],
            [5.7, 2.6, 3.5, 1.0], [1],
            [5.5, 2.4, 3.8, 1.1], [1],
            [5.5, 2.4, 3.7, 1.0], [1],
            [5.8, 2.7, 3.9, 1.2], [1],
            [6.0, 2.7, 5.1, 1.6], [1],
            [5.4, 3.0, 4.5, 1.5], [1],
            [6.0, 3.4, 4.5, 1.6], [1],
            [6.7, 3.1, 4.7, 1.5], [1],
            [6.3, 2.3, 4.4, 1.3], [1],
            [5.6, 3.0, 4.1, 1.3], [1],
            [5.5, 2.5, 4.0, 1.3], [1],
            [5.5, 2.6, 4.4, 1.2], [1],
            [6.1, 3.0, 4.6, 1.4], [1],
            [5.8, 2.6, 4.0, 1.2], [1],
            [5.0, 2.3, 3.3, 1.0], [1],
            [5.6, 2.7, 4.2, 1.3], [1],
            [5.7, 3.0, 4.2, 1.2], [1],
            [5.7, 2.9, 4.2, 1.3], [1],
            [6.2, 2.9, 4.3, 1.3], [1],
            [5.1, 2.5, 3.0, 1.1], [1],
            [5.7, 2.8, 4.1, 1.3], [1],
            [6.3, 3.3, 6.0, 2.5], [2],
            [5.8, 2.7, 5.1, 1.9], [2],
            [7.1, 3.0, 5.9, 2.1], [2],
            [6.3, 2.9, 5.6, 1.8], [2],
            [6.5, 3.0, 5.8, 2.2], [2],
            [7.6, 3.0, 6.6, 2.1], [2],
            [4.9, 2.5, 4.5, 1.7], [2],
            [7.3, 2.9, 6.3, 1.8], [2],
            [6.7, 2.5, 5.8, 1.8], [2],
            [7.2, 3.6, 6.1, 2.5], [2],
            [6.5, 3.2, 5.1, 2.0], [2],
            [6.4, 2.7, 5.3, 1.9], [2],
            [6.8, 3.0, 5.5, 2.1], [2],
            [5.7, 2.5, 5.0, 2.0], [2],
            [5.8, 2.8, 5.1, 2.4], [2],
            [6.4, 3.2, 5.3, 2.3], [2],
            [6.5, 3.0, 5.5, 1.8], [2],
            [7.7, 3.8, 6.7, 2.2], [2],
            [7.7, 2.6, 6.9, 2.3], [2],
            [6.0, 2.2, 5.0, 1.5], [2],
            [6.9, 3.2, 5.7, 2.3], [2],
            [5.6, 2.8, 4.9, 2.0], [2],
            [7.7, 2.8, 6.7, 2.0], [2],
            [6.3, 2.7, 4.9, 1.8], [2],
            [6.7, 3.3, 5.7, 2.1], [2],
            [7.2, 3.2, 6.0, 1.8], [2],
            [6.2, 2.8, 4.8, 1.8], [2],
            [6.1, 3.0, 4.9, 1.8], [2],
            [6.4, 2.8, 5.6, 2.1], [2],
            [7.2, 3.0, 5.8, 1.6], [2],
            [7.4, 2.8, 6.1, 1.9], [2],
            [7.9, 3.8, 6.4, 2.0], [2],
            [6.4, 2.8, 5.6, 2.2], [2],
            [6.3, 2.8, 5.1, 1.5], [2],
            [6.1, 2.6, 5.6, 1.4], [2],
            [7.7, 3.0, 6.1, 2.3], [2],
            [6.3, 3.4, 5.6, 2.4], [2],
            [6.4, 3.1, 5.5, 1.8], [2],
            [6.0, 3.0, 4.8, 1.8], [2],
            [6.9, 3.1, 5.4, 2.1], [2],
            [6.7, 3.1, 5.6, 2.4], [2],
            [6.9, 3.1, 5.1, 2.3], [2],
            [5.8, 2.7, 5.1, 1.9], [2],
            [6.8, 3.2, 5.9, 2.3], [2],
            [6.7, 3.3, 5.7, 2.5], [2],
            [6.7, 3.0, 5.2, 2.3], [2],
            [6.3, 2.5, 5.0, 1.9], [2],
            [6.5, 3.0, 5.2, 2.0], [2],
            [6.2, 3.4, 5.4, 2.3], [2],
            [5.9, 3.0, 5.1, 1.8], [2]
            ]
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
    classifier = abstraction.Classification(
        number_of_classes = 3,
        hidden_nodes      = [10, 20, 10],
        epochs            = 500
    ).model()
    
    # define model

    log.info("fit classification model to dataset features and targets")
    classifier.fit(features_train, targets_train)
    
    # train model

    log.info("test trained classification model on training dataset")
    score = metrics.accuracy_score(
        classifier.predict(features_train),
        targets_train
    )

    # predict and cross-validate training

    log.info("prediction accuracy on training dataset: {percentage}".format(
        percentage = 100 * score
    ))
    log.info("accuracy of classifier on test dataset:")
    score = metrics.accuracy_score(
        classifier.predict(features_test),
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
