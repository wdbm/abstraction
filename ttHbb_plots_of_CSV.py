#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# ttHbb_plots_of_CSV                                                           #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program accesses a CSV file generates plots from it.                    #
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
    -h, --help                   display help message
    --version                    display version and exit
    -v, --verbose                verbose logging
    -s, --silent                 silent
    -u, --username=USERNAME      username

    --infile=FILENAME            CSV input file                 [default: output.csv]

    --histogramcomparisons=BOOL  generate histogram comparisons [default: true]
    --scattermatrix=BOOL         generate scatter matrix        [default: true]
"""

from __future__ import division
import docopt
import os

import datavision
import matplotlib.pyplot as plt
import pandas as pd
import propyte
import pyprel
import shijian

name    = "ttHbb_plots_of_CSV"
version = "2017-04-14T1848Z"
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

    filename_CSV  = options["--infile"]

    make_histogram_comparisons = options["--histogramcomparisons"].lower() == "true"
    make_scatter_matrix        = options["--scattermatrix"].lower() == "true"

    if not os.path.isfile(os.path.expandvars(filename_CSV)):
        log.error("file {filename} not found".format(
            filename = filename_CSV
        ))
        program.terminate()

    log.info("read CSV from {filename}".format(filename = filename_CSV))
    data = pd.read_csv(filename_CSV)

    number_of_columns          = data.shape[1]
    indices_of_feature_columns = range(0, number_of_columns -1)

    feature_names = list(data.columns)

    data_class_0 = data.loc[data["class"] == 0]
    data_class_1 = data.loc[data["class"] == 1]

    print("")
    log.info("basic feature characteristics")
    print("")

    table_contents = [[
        "feature",
        "minimum value in class 0",
        "minimum value in class 1",
        "maximum value in class 0",
        "maximum value in class 1",
        "mean value in class 0",
        "mean value in class 1"
    ]]

    for feature_name in feature_names:

        values_class_0 = list(data_class_0[feature_name])
        values_class_1 = list(data_class_1[feature_name])

        table_contents.append([
            feature_name,
            min(values_class_0),
            min(values_class_1),
            max(values_class_0),
            max(values_class_1),
            sum(values_class_0)/len(values_class_0),
            sum(values_class_1)/len(values_class_1)
        ])

    print(
        pyprel.Table(
            contents = table_contents
        )
    )

    if make_histogram_comparisons:

        for feature_name in feature_names:

            filename = shijian.propose_filename(
                filename = feature_name + "_ttbb_ttH.png"
            )
            log.info("save histogram {filename}".format(filename = filename))
            datavision.save_histogram_comparison_matplotlib(
                values_1      = list(data_class_0[feature_name]),
                values_2      = list(data_class_1[feature_name]),
                label_1       = "ttbb",
                label_2       = "ttH",
                label_ratio_x = "frequency",
                label_y       = "",
                title         = feature_name,
                filename      = filename,
                directory     = "comparisons"
            )

    if make_scatter_matrix:

        filename = "scatter_matrix_ttbb_ttH.jpg"
        log.info("save scatter matrix {filename}".format(filename = filename))
        scatter_matrix = pd.scatter_matrix(
            data,
            figsize  = [15, 15],
            marker   = ".",
            s        = 0.2,
            diagonal = "kde"
        )
        for ax in scatter_matrix.ravel():
            ax.set_xlabel(
                ax.get_xlabel(),
                fontsize = 15,
                rotation = 90
            )
            ax.set_ylabel(
                ax.get_ylabel(),
                fontsize = 15,
                rotation = 0,
                labelpad = 60
            )
            ax.get_xaxis().set_ticks([])
            ax.get_yaxis().set_ticks([])
        plt.savefig(filename, dpi = 700)

    print("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
