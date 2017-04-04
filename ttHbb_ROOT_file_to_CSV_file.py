#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# ttHbb_ROOT_file_to_CSV_file                                                  #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program accesses a ROOT file and saves variables of the ROOT file to a  #
# CSV file.                                                                    #
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
    -h, --help               Show this help message.
    --version                Show the version and exit.
    -v, --verbose            Show verbose logging.
    -s, --silent             silent
    -u, --username=USERNAME  username

    --fileroot=FILENAME      ROOT file                           [default: output.root]
    --filecsv=FILENAME       CSV file                            [default: output.csv]

    --selection=TEXT         channel selection (ejets, mujets)   [default: ejets]
    --classlabel=TEXT        class label for last column

    --tree=TEXT              tree name                           [default: nominal]
    --maxevents=INT          maximum number of events to collate [default: none]
"""

from __future__ import division
import csv
import docopt
import os
import textwrap

import abstraction
import propyte
with propyte.import_ganzfeld():
    from ROOT import *
import shijian

name    = "ttHbb_ROOT_file_to_CSV_file"
version = "2017-04-04T1227Z"
logo    = name

def select_event(
    event     = None,
    selection = "ejets"
    ):

    """
    Select a HEP event.
    """

    if selection == "ejets":
        # Require a number of leptons.
        # Require >= 4 jets.
        # Require a single large-R jet.
        if \
            0 < len(event.el_pt) < 2 and \
            event.nJets >= 4         and \
            event.nLjets >= 1:
            return True
        else:
            return False
    if selection == "mujets":
        # Require a number of leptons.
        # Require >= 4 jets.
        # Require a single large-R jet.
        if                               \
            0 < len(event.mu_pt) < 2 and \
            event.nJets >= 4         and \
            event.nLjets >= 1:
            return True
        else:
            return False

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

    filename_ROOT            = options["--fileroot"]
    filename_CSV             = options["--filecsv"]
    selection                = options["--selection"]
    class_label              = options["--classlabel"]
    name_tree                = options["--tree"]
    maximum_number_of_events = None if options["--maxevents"].lower() == "none"\
                                  else int(options["--maxevents"])

    if not os.path.isfile(os.path.expandvars(filename_ROOT)):
        log.error("file {filename} not found".format(
            filename = filename_ROOT
        ))
        program.terminate()

    if os.path.isfile(os.path.expandvars(filename_CSV)):
        log.warning("CSV file {filename} exists -- *append* data to file".format(
            filename = filename_CSV
        ))
        print("")
        append = True
    else:
        append = False

    file_ROOT                = abstraction.open_ROOT_file(filename_ROOT)
    tree                     = file_ROOT.Get(name_tree)
    number_of_events         = tree.GetEntries()

    file_CSV                 = open(filename_CSV, "a")
    writer                   = csv.writer(file_CSV, delimiter = ",")

    log.info(textwrap.dedent(
        """
        input ROOT file: {filename_ROOT}
        output CSV file: {filename_CSV}
        selection:       {selection}
        class label:     {class_label}
        """.format(
            filename_ROOT = filename_ROOT,
            filename_CSV  = filename_CSV,
            selection     = selection,
            class_label   = class_label
        )
    ))

    headings = [
        "eventNumber",
        "el_1_pt",
        "el_1_eta",
        "el_1_phi",
        "jet_1_pt",
        "jet_1_eta",
        "jet_1_phi",
        "jet_1_e",
        "jet_2_pt",
        "jet_2_eta",
        "jet_2_phi",
        "jet_2_e",
        "nJets",
        "nBTags",
        "nLjets",
        "ljet_m",
        "met_met",
        "met_phi",
        "Centrality_all",
        "Mbb_MindR",
        "ljet_tau21",
        "ljet_tau32",
        #"Aplan_bjets",
        "H4_all",
        "NBFricoNN_6jin4bin",
        "NBFricoNN_6jin3bex",
        "NBFricoNN_5jex4bin",
        "NBFricoNN_3jex3bex",
        "NBFricoNN_4jin3bex",
        "NBFricoNN_4jin4bin",
        "class"
    ]

    log.info("{number} variables to collate:\n\n{variables}".format(
        number    = len(headings),
        variables = ", ".join(headings)
    ))

    if not append:
        writer.writerow(headings)

    print("")
    log.info("save variables of events to CSV")
    print("")

    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    index_selected = 0
    for index, event in enumerate(tree):
        if select_event(
            event     = event,
            selection = "ejets"
            ):
            index_selected = index_selected + 1
            if                                           \
                maximum_number_of_events is not None and \
                index_selected > maximum_number_of_events:
                break
            line = [
                event.eventNumber,
                event.el_pt[0],
                event.el_eta[0],
                event.el_phi[0],
                event.jet_pt[0],
                event.jet_eta[0],
                event.jet_phi[0],
                event.jet_e[0],
                event.jet_pt[1],
                event.jet_eta[1],
                event.jet_phi[1],
                event.jet_e[1],
                event.nJets,
                event.nBTags,
                event.nLjets,
                event.ljet_m[0],
                event.met_met,
                event.met_phi,
                event.Centrality_all,
                event.Mbb_MindR,
                event.ljet_tau21[0],
                event.ljet_tau32[0],
                #event.Aplan_bjets,
                event.H4_all,
                event.NBFricoNN_6jin4bin,
                event.NBFricoNN_6jin3bex,
                event.NBFricoNN_5jex4bin,
                event.NBFricoNN_3jex3bex,
                event.NBFricoNN_4jin3bex,
                event.NBFricoNN_4jin4bin,
                class_label
            ]
            writer.writerow(line)
        print(progress.add_datum(fraction = index / number_of_events))

    print("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
