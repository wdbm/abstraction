#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# split_SUSY_100k                                                              #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program splits the SUSY Data Set to signal and background files.        #
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
    -h, --help                        display help message
    --version                         display version and exit
    -v, --verbose                     verbose logging
    -s, --silent                      silent
    -u, --username=USERNAME           username
    --data=FILENAME                   input data file
                                      [default: SUSY_100k.csv]
    --signal=FILENAME                 output signal data file
                                      [default: SUSY_100k_signal.csv]
    --background=FILENAME             output background data file
                                      [default: SUSY_100k_background.csv]
    --maximumeventssignal=NUMBER      maximum number of signal events saved
                                      [default: none]
    --maximumeventsbackground=NUMBER  maximum number of signal events saved
                                      [default: none]
"""

name    = "split_SUSY_100k"
version = "2017-03-02T2256Z"
logo    = None

import csv
import docopt
import logging
import os
import sys
import time

def main(options):

    filename_input_data             = options["--data"]
    filename_output_data_signal     = options["--signal"]
    filename_output_data_background = options["--background"]
    maximum_events_signal           = options["--maximumeventssignal"]
    maximum_events_background       = options["--maximumeventsbackground"]
    if options["--maximumeventssignal"].lower() == "none":
        maximum_events_signal = None
    else:
        maximum_events_signal = int(options["--maximumeventssignal"])

    if options["--maximumeventsbackground"].lower() == "none":
        maximum_events_background = None
    else:
        maximum_events_background = int(options["--maximumeventsbackground"])

    print("input data file: {filename}".format(
        filename = filename_input_data
    ))

    data = [line.rstrip("\n") for line in open(filename_input_data)]
    data_signal     = []
    data_background = []

    for line in data:
        line_list = line.split(",")
        classification_event = float(line_list[0])            
        if classification_event == 1:
            if maximum_events_signal is None:
                data_signal.append(line_list[1:])
            elif len(data_signal) < maximum_events_signal:
                data_signal.append(line_list[1:])

    for line in data:
        line_list = line.split(",")
        classification_event = float(line_list[0])            
        if classification_event == 0:
            if maximum_events_background is None:
                data_background.append(line_list[1:])
            elif len(data_background) < maximum_events_background:
                data_background.append(line_list[1:])

    print("")
    print("number of lines in input data:             {number_of_lines}".format(
        number_of_lines = len(data)
    ))
    print("number of lines in output signal data:     {number_of_lines}".format(
        number_of_lines = len(data_signal)
    ))
    print("number of lines in output background data: {number_of_lines}".format(
        number_of_lines = len(data_background)
    ))

    print("")
    print("save signal data to file {filename}".format(
        filename = filename_output_data_signal
    ))
    with open(filename_output_data_signal, "w") as file_output_data_signal:
        writer = csv.writer(file_output_data_signal)
        writer.writerows(data_signal)
    print("save background data to file {filename}".format(
        filename = filename_output_data_background
    ))
    with open(filename_output_data_background, "w") as file_output_data_background:
        writer = csv.writer(file_output_data_background)
        writer.writerows(data_background)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
