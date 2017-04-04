#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# ttHbb_preprocess_CSV_file                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program accesses a CSV file and preprocesses the data in it to attempt  #
# to make it suitable for machine learning algorithms.                         #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
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

    --infile=FILENAME        CSV input file  [default: output.csv]
    --outfile=FILENAME       CSV output file [default: output_preprocessed.csv]
"""

from __future__ import division
import docopt
import os

import pandas as pd
import propyte
import sklearn.preprocessing

name    = "ttHbb_preprocess_CSV_file"
version = "2017-04-04T1647Z"
logo    = name

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

    print("")

    filename_CSV_input  = options["--infile"]
    filename_CSV_output = options["--outfile"]

    if not os.path.isfile(os.path.expandvars(filename_CSV_input)):
        log.error("file {filename} not found".format(
            filename = filename_CSV_input
        ))
        program.terminate()

    log.info("read CSV from {filename}".format(filename = filename_CSV_input))
    data = pd.read_csv(filename_CSV_input)

    scaler = sklearn.preprocessing.MinMaxScaler(feature_range = (-1, 1))

    number_of_columns          = data.shape[1]
    indices_of_feature_columns = range(0, number_of_columns -1)

    # scale feature columns
    log.info("scale features")
    data[indices_of_feature_columns] = scaler.fit_transform(data[indices_of_feature_columns])

    log.info("save scaled CSV to {filename}".format(filename = filename_CSV_output))
    data.to_csv(filename_CSV_output, index = False, header = False)

    print("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
