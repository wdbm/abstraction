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

    --selection=TEXT         channel selection (ejets, mujets)   [default: all]
    --classlabel=TEXT        class label for last column

    --tree=TEXT              tree name                           [default: nominal_Loose]
    --maxevents=INT          maximum number of events to collate [default: none]
    --headings=BOOL          include headings at top of CSV file [default: true]
"""

from __future__ import division
import csv
import docopt
import math
import os
import textwrap

import abstraction
import propyte
with propyte.import_ganzfeld():
    from ROOT import *
import pyprel
import shijian

name    = "ttHbb_ROOT_file_to_CSV_file"
version = "2017-06-14T2057Z"
logo    = name

def select_event(
    event                             = None,
    selection                         = "all",
    required_variables                = None,
    ensure_required_variables_present = False,
    verbose                           = True
    ):

    """
    Select a HEP event.
    """

    if required_variables is None:
        required_variables = [
            "Aplan_bjets",
            "Aplan_jets",
            "Centrality_all",
            "ClassifBDTOutput_6jsplit",
            "ClassifBDTOutput_basic",
            "ClassifBDTOutput_withReco_6jsplit",
            "ClassifBDTOutput_withReco_basic",
            "ClassifHPLUS_Semilep_HF_BDT200_Output",
            "dEtajj_MaxdEta",
            "dRbb_avg",
            "dRbb_MaxM",
            "dRbb_MaxPt",
            "dRbb_min",
            "dRbj_Wmass",
            "dRHl_MaxdR",
            "dRHl_MindR",
            "dRjj_min",
            "dRlepbb_MindR",
            "dRlj_MindR",
            "dRuu_MindR",
            "H1_all",
            "H4_all",
            "HhadT_nJets",
            "HiggsbbM",
            "HiggsjjM",
            "HT_all",
            "HT_jets",
            "Mbb_MaxM",
            "Mbb_MaxPt",
            "Mbb_MindR",
            "Mbj_MaxPt",
            "Mbj_MindR",
            "Mbj_Wmass",
            "met_met",
            "met_phi",
            "MHiggs",
            "Mjj_HiggsMass",
            "Mjjj_MaxPt",
            "Mjj_MaxPt",
            "Mjj_MindR",
            "Mjj_MinM",
            "mu",
            "Muu_MindR",
            "NBFricoNN_dil",
            "nBTags",
            "nBTags30",
            "nBTags50",
            "nBTags60",
            "nBTags70",
            "nBTags77",
            "nBTags80",
            "nBTags85",
            "nBTags90",
            "nBTagsFlatBEff_30",
            "nBTagsFlatBEff_40",
            "nBTagsFlatBEff_50",
            "nBTagsFlatBEff_60",
            "nBTagsFlatBEff_70",
            "nBTagsFlatBEff_77",
            "nBTagsFlatBEff_85",
            "nElectrons",
            "nHFJets",
            "NHiggs_30",
            "Njet_pt40",
            "Njet_pt40",
            "nJets",
            "nMuons",
            "nPrimaryVtx",
            "pT_jet3",
            "pT_jet5",
            "pTuu_MindR",
            "semilepMVAreco_b1higgsbhadtop_dR",
            "semilepMVAreco_bbhiggs_dR",
            "semilepMVAreco_BDT_output",
            "semilepMVAreco_BDT_output_6jsplit",
            "semilepMVAreco_BDT_output_truthMatchPattern",
            "semilepMVAreco_BDT_withH_output",
            "semilepMVAreco_BDT_withH_output_6jsplit",
            "semilepMVAreco_BDT_withH_output_truthMatchPattern",
            "semilepMVAreco_hadWb1Higgs_mass",
            "semilepMVAreco_higgsbhadtop_withH_dR",
            "semilepMVAreco_higgsbleptop_mass",
            "semilepMVAreco_higgsbleptop_withH_dR",
            "semilepMVAreco_higgslep_dR",
            "semilepMVAreco_higgsleptop_dR",
            "semilepMVAreco_higgs_mass",
            "semilepMVAreco_higgsq1hadW_mass",
            "semilepMVAreco_higgsttbar_withH_dR",
            "semilepMVAreco_leptophadtop_dR",
            "semilepMVAreco_leptophadtop_withH_dR",
            "semilepMVAreco_Ncombinations",
            "semilepMVAreco_nuApprox_recoBDT",
            "semilepMVAreco_nuApprox_recoBDT_6jsplit",
            "semilepMVAreco_nuApprox_recoBDT_withH",
            "semilepMVAreco_nuApprox_recoBDT_withH_6jsplit",
            "semilepMVAreco_ttH_Ht_withH",
            #"ttHF_mva_discriminant",
            "el_d0sig[0]",
            "el_delta_z0_sintheta[0]",
            "el_e[0]",
            "el_eta[0]",
            "el_phi[0]",
            "el_pt[0]",
            "el_topoetcone20[0]",
            #"mu_d0sig[0]",
            #"mu_delta_z0_sintheta[0]",
            #"mu_e[0]",
            #"mu_eta[0]",
            #"mu_phi[0]",
            #"mu_pt[0]",
            "mu_topoetcone20[0]",
            "jet_e[0]",
            "jet_eta[0]",
            "jet_jvt[0]",
            "jet_mv2c10[0]",
            "jet_mv2c20[0]",
            "jet_phi[0]",
            "jet_pt[0]",
            "jet_semilepMVAreco_recoBDT_cand[0]",
            "jet_semilepMVAreco_recoBDT_cand_6jsplit[0]",
            "jet_semilepMVAreco_recoBDT_withH_cand[0]",
            "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[0]",
            "jet_e[1]",
            "jet_eta[1]",
            "jet_jvt[1]",
            "jet_mv2c10[1]",
            "jet_mv2c20[1]",
            "jet_phi[1]",
            "jet_pt[1]",
            "jet_semilepMVAreco_recoBDT_cand[1]",
            "jet_semilepMVAreco_recoBDT_cand_6jsplit[1]",
            "jet_semilepMVAreco_recoBDT_withH_cand[1]",
            "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[1]",
            "jet_e[2]",
            "jet_eta[2]",
            "jet_jvt[2]",
            "jet_mv2c10[2]",
            "jet_mv2c20[2]",
            "jet_phi[2]",
            "jet_pt[2]",
            "jet_semilepMVAreco_recoBDT_cand[2]",
            "jet_semilepMVAreco_recoBDT_cand_6jsplit[2]",
            "jet_semilepMVAreco_recoBDT_withH_cand[2]",
            "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[2]",
            "jet_e[3]",
            "jet_eta[3]",
            "jet_jvt[3]",
            "jet_mv2c10[3]",
            "jet_mv2c20[3]",
            "jet_phi[3]",
            "jet_pt[3]",
            "jet_semilepMVAreco_recoBDT_cand[3]",
            "jet_semilepMVAreco_recoBDT_cand_6jsplit[3]",
            "jet_semilepMVAreco_recoBDT_withH_cand[3]",
            "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[3]"
        ]

    if ensure_required_variables_present and not all([hasattr(event, variable) for variable in required_variables]):

        return False

    #for variable in required_variables:
    #    if not hasattr(event, variable):
    #        print("missing {variable}".format(variable = variable))

    # By default, do not pass.
    conditions = [False]

    if selection == "ejets":

        conditions = [
            event.nElectrons == 1,                      # Require 1 electron.
            event.nJets >= 4,                           # Require >= 4 jets.
            #event.nLjets >= 1                          # Require a single large-R jet.
        ]

    elif selection == "mujets":

        conditions = [
            event.nMuons == 1,                          # Require 1 muon.
            event.nJets >= 4,                           # Require >= 4 jets.
            #event.nLjets >= 1                          # Require a single large-R jet.
        ]

    if selection == "ejets_5JE4BI":

        conditions = [
            event.nElectrons == 1,                      # Require 1 electron.
            event.nJets == 5,                           # Require 5 jets.
            event.nBTags >= 4                           # Require >= 4 b tags.
            #event.nLjets >= 1                          # Require a single large-R jet.
        ]

    if selection == "ejets_6JI4BI":

        conditions = [
            event.nElectrons == 1,                      # Require 1 electron.
            event.nJets >= 6,                           # Require >=6 jets.
            event.nBTags >= 4                           # Require >= 4 b tags.
            #event.nLjets >= 1                          # Require a single large-R jet.
        ]

    elif selection == "all":

        conditions = [
            event.nElectrons == 1 or event.nMuons == 1, # Require 1 electron or 1 muon.
            event.nJets >= 4,                           # Require >= 4 jets.
            #event.nLjets >= 1                          # Require a single large-R jet.
        ]

    if all(conditions):

        if verbose:
            log.info("event number {event_number} passed selection {selection}".format(
                event_number = event.eventNumber,
                selection    = selection
            ))

        return True

    else:

        return False

class Variable_ttHbb(object):

    """
    name:       name used to save to CSV etc.
    value:      variable value extracted from event
    impude:     bool, engage (default) or disengage imputation processing
    imputation: dictionary where keys are detected missing values and values are
                impude values or labels for detected missing values
    """

    def __init__(
        self,
        name                    = None,
        value                   = None,
        event                   = None,
        impude                  = True,
        imputation_value_global = None#-4
        ):

        self._name                    = name
        self._value                   = value
        self._event                   = event
        self._impude                  = impude
        self._imputation_value_global = imputation_value_global
        self._imputation              = {
                                             0:   self._imputation_value_global,
                                            -1:   self._imputation_value_global,
                                            -2:   self._imputation_value_global,
                                            -3:   self._imputation_value_global,
                                            -9:   self._imputation_value_global,
                                            -999: self._imputation_value_global,
                                            None: self._imputation_value_global
                                        }

        if self._value is None:
            self._value = shijian.get_attribute(
                object_instance          = self._event,
                name                     = self._name,
                imputation_default_value = self._imputation_value_global
            )

        if self._impude:
            self.impude()

    def name(
        self
        ):

        return self._name

    def value(
        self
        ):

        return self._value

    def impude(
        self
        ):

        if\
            self._impude and\
            any(element in self._name for element in [
                "Aplan_jets",
                "Aplan_bjets",
                "Centrality_all",
                "ClassifBDTOutput_6jsplit",
                "ClassifBDTOutput_basic",
                "ClassifBDTOutput_withReco_6jsplit",
                "ClassifBDTOutput_withReco_basic",
                "ClassifHPLUS_Semilep_HF_BDT200_Output",
                "dEtajj_MaxdEta",
                "dRbb_avg",
                "dRbb_MaxM",
                "dRbb_MaxPt",
                "dRbb_min",
                "dRbj_Wmass",
                "dRHl_MaxdR",
                "dRHl_MindR",
                "dRjj_min",
                "dRlepbb_MindR",
                "dRlj_MindR",
                "dRuu_MindR",
                "H4_all",
                "HhadT_nJets",
                "HiggsbbM",
                "HiggsjjM",
                "HT_all",
                "HiggsbbM",
                "HT_all",
                "Mbb_MaxM",
                "Mbb_MaxPt",
                "Mbb_MindR",
                "Mbj_MaxPt",
                "Mbj_MindR",
                "Mbj_Wmass",
                "MHiggs",
                "Mjj_HiggsMass",
                "Mjj_MinM",
                "NBFricoNN_dil",
                "NBFricoNN_ljets",
                "pT_jet3",
                "pT_jet5",
                "pTuu_MindR",
                "SecondLjetM",
                "SecondLjetPt",
                "semilepMVAreco_b1higgsbhadtop_dR",
                "semilepMVAreco_bbhiggs_dR",
                "semilepMVAreco_BDT_output",
                "semilepMVAreco_BDT_output_6jsplit",
                "semilepMVAreco_BDT_output_truthMatchPattern",
                "semilepMVAreco_BDT_withH_output",
                "semilepMVAreco_BDT_withH_output_6jsplit",
                "semilepMVAreco_BDT_withH_output_truthMatchPattern",
                "semilepMVAreco_hadWb1Higgs_mass",
                "semilepMVAreco_higgsbhadtop_withH_dR",
                "semilepMVAreco_higgsbleptop_mass",
                "semilepMVAreco_higgsbleptop_withH_dR",
                "semilepMVAreco_higgslep_dR",
                "semilepMVAreco_higgsleptop_dR",
                "semilepMVAreco_higgs_mass",
                "semilepMVAreco_higgsq1hadW_mass",
                "semilepMVAreco_higgsttbar_withH_dR",
                "semilepMVAreco_leptophadtop_dR",
                "semilepMVAreco_leptophadtop_withH_dR",
                "semilepMVAreco_Ncombinations",
                "semilepMVAreco_nuApprox_recoBDT",
                "semilepMVAreco_nuApprox_recoBDT_6jsplit",
                "semilepMVAreco_nuApprox_recoBDT_withH",
                "semilepMVAreco_nuApprox_recoBDT_withH_6jsplit",
                "semilepMVAreco_ttH_Ht_withH",
                "ttHF_mva_discriminant",
                "jet1_semilepMVAreco_recoBDT_cand",
                "jet1_semilepMVAreco_recoBDT_cand_6jsplit",
                "jet1_semilepMVAreco_recoBDT_withH_cand",
                "jet1_semilepMVAreco_recoBDT_withH_cand_6jsplit",
                "jet2_jvt",
                "jet2_semilepMVAreco_recoBDT_cand",
                "jet2_semilepMVAreco_recoBDT_cand_6jsplit",
                "jet2_semilepMVAreco_recoBDT_withH_cand",
                "jet2_semilepMVAreco_recoBDT_withH_cand_6jsplit",
                "jet3_semilepMVAreco_recoBDT_cand",
                "jet3_semilepMVAreco_recoBDT_cand_6jsplit",
                "jet3_semilepMVAreco_recoBDT_withH_cand",
                "jet3_semilepMVAreco_recoBDT_withH_cand_6jsplit",
                "jet4_jvt",
                "jet4_semilepMVAreco_recoBDT_cand",
                "jet4_semilepMVAreco_recoBDT_cand_6jsplit",
                "jet4_semilepMVAreco_recoBDT_withH_cand",
                "jet4_semilepMVAreco_recoBDT_withH_cand_6jsplit",
                "el_d0sig",
                "el_delta_z0_sintheta",
                "el_e",
                "el_eta",
                "el_phi",
                "el_pt",
                "el_topoetcone20",
                "ljet_C2",
                "ljet_D2",
                "ljet_e",
                "ljet_eta",
                "ljet_m",
                "ljet_phi",
                "ljet_pt",
                "ljet_sd12",
                "ljet_sd23",
                "ljet_tau21",
                "ljet_tau21_wta",
                "ljet_tau32",
                "ljet_tau32_wta"
            ]):
                if self._value is None:
                    self._value = self._imputation_value_global
                if isinstance(self._value, int) or isinstance(self._value, float):
                    if math.isnan(self._value):
                        self._value = self._imputation_value_global
                if self._value in self._imputation:
                    self._value = self._imputation[self._value]

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
    class_label              = int(options["--classlabel"])
    name_tree                = options["--tree"]
    maximum_number_of_events = None if options["--maxevents"].lower() == "none"\
                                  else int(options["--maxevents"])
    include_headings         = options["--headings"].lower() == "true"

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


    print("")
    log.info("save variables of events to CSV {filename}".format(
        filename = filename_CSV
    ))
    print("")

    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    index_selected = 0
    detail = True
    for index, event in enumerate(tree):
        if select_event(
            event     = event,
            selection = selection
            ):
            index_selected = index_selected + 1
            if                                           \
                maximum_number_of_events is not None and \
                index_selected > maximum_number_of_events:
                break
            line = [
                #Variable_ttHbb(event = event, name = "Aplan_bjets"),
                Variable_ttHbb(event = event, name = "Aplan_jets"), #
                Variable_ttHbb(event = event, name = "Centrality_all"), #
                #Variable_ttHbb(event = event, name = "ClassifBDTOutput_6jsplit"),
                #Variable_ttHbb(event = event, name = "ClassifBDTOutput_basic"),
                #Variable_ttHbb(event = event, name = "ClassifBDTOutput_withReco_6jsplit"),
                #Variable_ttHbb(event = event, name = "ClassifBDTOutput_withReco_basic"),
                #Variable_ttHbb(event = event, name = "ClassifHPLUS_Semilep_HF_BDT200_Output"),
                Variable_ttHbb(event = event, name = "dEtajj_MaxdEta"), #
                Variable_ttHbb(event = event, name = "dRbb_avg"), #
                #Variable_ttHbb(event = event, name = "dRbb_MaxM"),
                Variable_ttHbb(event = event, name = "dRbb_MaxPt"), #
                #Variable_ttHbb(event = event, name = "dRbb_min"),
                #Variable_ttHbb(event = event, name = "dRbj_Wmass"),
                #Variable_ttHbb(event = event, name = "dRHl_MaxdR"),
                #Variable_ttHbb(event = event, name = "dRHl_MindR"),
                #Variable_ttHbb(event = event, name = "dRjj_min"),
                #Variable_ttHbb(event = event, name = "dRlepbb_MindR"),
                #Variable_ttHbb(event = event, name = "dRlj_MindR"),
                #Variable_ttHbb(event = event, name = "dRuu_MindR"),
                Variable_ttHbb(event = event, name = "H1_all"), #
                #Variable_ttHbb(event = event, name = "H4_all"),
                #Variable_ttHbb(event = event, name = "HhadT_nJets"),
                #Variable_ttHbb(event = event, name = "HiggsbbM"),
                #Variable_ttHbb(event = event, name = "HiggsjjM"),
                #Variable_ttHbb(event = event, name = "HT_all"),
                #Variable_ttHbb(event = event, name = "HT_jets"),
                #Variable_ttHbb(event = event, name = "Mbb_MaxM"),
                #Variable_ttHbb(event = event, name = "Mbb_MaxPt"),
                Variable_ttHbb(event = event, name = "Mbb_MindR"), #
                #Variable_ttHbb(event = event, name = "Mbj_MaxPt"),
                #Variable_ttHbb(event = event, name = "Mbj_MindR"),
                #Variable_ttHbb(event = event, name = "Mbj_Wmass"),
                #Variable_ttHbb(event = event, name = "met_met"),
                #Variable_ttHbb(event = event, name = "met_phi"),
                #Variable_ttHbb(event = event, name = "MHiggs"),
                #Variable_ttHbb(event = event, name = "Mjj_HiggsMass"),
                #Variable_ttHbb(event = event, name = "Mjjj_MaxPt"),
                #Variable_ttHbb(event = event, name = "Mjj_MaxPt"),
                #Variable_ttHbb(event = event, name = "Mjj_MindR"),
                #Variable_ttHbb(event = event, name = "Mjj_MinM"),
                #Variable_ttHbb(event = event, name = "mu"),
                #Variable_ttHbb(event = event, name = "Muu_MindR"),
                #Variable_ttHbb(event = event, name = "NBFricoNN_dil"),
                #Variable_ttHbb(event = event, name = "nBTags"),
                #Variable_ttHbb(event = event, name = "nBTags30"),
                #Variable_ttHbb(event = event, name = "nBTags50"),
                #Variable_ttHbb(event = event, name = "nBTags60"),
                #Variable_ttHbb(event = event, name = "nBTags70"),
                #Variable_ttHbb(event = event, name = "nBTags77"),
                #Variable_ttHbb(event = event, name = "nBTags80"),
                #Variable_ttHbb(event = event, name = "nBTags85"),
                #Variable_ttHbb(event = event, name = "nBTags90"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_30"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_40"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_50"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_60"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_70"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_77"),
                #Variable_ttHbb(event = event, name = "nBTagsFlatBEff_85"),

                #Variable_ttHbb(event = event, name = "nElectrons"),
                #Variable_ttHbb(event = event, name = "nHFJets"),
                Variable_ttHbb(event = event, name = "NHiggs_30"), #
                #Variable_ttHbb(event = event, name = "Njet_pt40"),
                #Variable_ttHbb(event = event, name = "Njet_pt40"),
                #Variable_ttHbb(event = event, name = "nJets"),
                #Variable_ttHbb(event = event, name = "nMuons"),
                #Variable_ttHbb(event = event, name = "nPrimaryVtx"),

                #Variable_ttHbb(event = event, name = "pT_jet3"),
                Variable_ttHbb(event = event, name = "pT_jet5"), #
                #Variable_ttHbb(event = event, name = "pTuu_MindR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_b1higgsbhadtop_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_bbhiggs_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_BDT_output"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_BDT_output_6jsplit"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_BDT_output_truthMatchPattern"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_BDT_withH_output"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_BDT_withH_output_6jsplit"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_BDT_withH_output_truthMatchPattern"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_hadWb1Higgs_mass"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgsbhadtop_withH_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgsbleptop_mass"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgsbleptop_withH_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgslep_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgsleptop_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgs_mass"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgsq1hadW_mass"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_higgsttbar_withH_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_leptophadtop_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_leptophadtop_withH_dR"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_Ncombinations"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_nuApprox_recoBDT"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_nuApprox_recoBDT_6jsplit"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_nuApprox_recoBDT_withH"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_nuApprox_recoBDT_withH_6jsplit"),
                #Variable_ttHbb(event = event, name = "semilepMVAreco_ttH_Ht_withH"),
                #Variable_ttHbb(event = event, name = "ttHF_mva_discriminant"),

                #Variable_ttHbb(event = event, name = "el_d0sig[0]"),
                #Variable_ttHbb(event = event, name = "el_delta_z0_sintheta[0]"),
                #Variable_ttHbb(event = event, name = "el_e[0]"),
                #Variable_ttHbb(event = event, name = "el_eta[0]"),
                #Variable_ttHbb(event = event, name = "el_phi[0]"),
                #Variable_ttHbb(event = event, name = "el_pt[0]"),
                #Variable_ttHbb(event = event, name = "el_topoetcone20[0]"),

                #Variable_ttHbb(event = event, name = "mu_d0sig[0]"),
                #Variable_ttHbb(event = event, name = "mu_delta_z0_sintheta[0]"),
                #Variable_ttHbb(event = event, name = "mu_e[0]"),
                #Variable_ttHbb(event = event, name = "mu_eta[0]"),
                #Variable_ttHbb(event = event, name = "mu_phi[0]"),
                #Variable_ttHbb(event = event, name = "mu_pt[0]"),
                #Variable_ttHbb(event = event, name = "mu_topoetcone20[0]"),

                #Variable_ttHbb(event = event, name = "jet_e[0]"),
                #Variable_ttHbb(event = event, name = "jet_eta[0]"),
                #Variable_ttHbb(event = event, name = "jet_jvt[0]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c10[0]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c20[0]"),
                #Variable_ttHbb(event = event, name = "jet_phi[0]"),
                #Variable_ttHbb(event = event, name = "jet_pt[0]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand[0]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand_6jsplit[0]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand[0]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[0]"),

                #Variable_ttHbb(event = event, name = "jet_e[1]"),
                #Variable_ttHbb(event = event, name = "jet_eta[1]"),
                #Variable_ttHbb(event = event, name = "jet_jvt[1]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c10[1]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c20[1]"),
                #Variable_ttHbb(event = event, name = "jet_phi[1]"),
                #Variable_ttHbb(event = event, name = "jet_pt[1]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand[1]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand_6jsplit[1]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand[1]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[1]"),

                #Variable_ttHbb(event = event, name = "jet_e[2]"),
                #Variable_ttHbb(event = event, name = "jet_eta[2]"),
                #Variable_ttHbb(event = event, name = "jet_jvt[2]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c10[2]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c20[2]"),
                #Variable_ttHbb(event = event, name = "jet_phi[2]"),
                #Variable_ttHbb(event = event, name = "jet_pt[2]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand[2]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand_6jsplit[2]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand[2]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[2]"),

                #Variable_ttHbb(event = event, name = "jet_e[3]"),
                #Variable_ttHbb(event = event, name = "jet_eta[3]"),
                #Variable_ttHbb(event = event, name = "jet_jvt[3]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c10[3]"),
                #Variable_ttHbb(event = event, name = "jet_mv2c20[3]"),
                #Variable_ttHbb(event = event, name = "jet_phi[3]"),
                #Variable_ttHbb(event = event, name = "jet_pt[3]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand[3]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_cand_6jsplit[3]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand[3]"),
                #Variable_ttHbb(event = event, name = "jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[3]"),

                # large-R jets
                #Variable_ttHbb(event = event, name = "FirstLjetM"),
                #Variable_ttHbb(event = event, name = "FirstLjetPt"),
                #Variable_ttHbb(event = event, name = "HhadT_nLjets"),
                #Variable_ttHbb(event = event, name = "HT_ljets"),
                #Variable_ttHbb(event = event, name = "NBFricoNN_ljets"),
                #Variable_ttHbb(event = event, name = "nBjetOutsideLjet"),
                #Variable_ttHbb(event = event, name = "nJetOutsideLjet"),
                #Variable_ttHbb(event = event, name = "nLjet_m100"),
                #Variable_ttHbb(event = event, name = "nLjet_m50"),
                #Variable_ttHbb(event = event, name = "nLjets"),
                #Variable_ttHbb(event = event, name = "SecondLjetM"),
                #Variable_ttHbb(event = event, name = "SecondLjetPt"),
                #Variable_ttHbb(event = event, name = "ljet_C2[0]"),
                #Variable_ttHbb(event = event, name = "ljet_D2[0]"),
                #Variable_ttHbb(event = event, name = "ljet_e[0]"),
                #Variable_ttHbb(event = event, name = "ljet_eta[0]"),
                #Variable_ttHbb(event = event, name = "ljet_m[0]"),
                #Variable_ttHbb(event = event, name = "ljet_phi[0]"),
                #Variable_ttHbb(event = event, name = "ljet_pt[0]"),
                #Variable_ttHbb(event = event, name = "ljet_sd12[0]"),
                #Variable_ttHbb(event = event, name = "ljet_sd23[0]"),
                #Variable_ttHbb(event = event, name = "ljet_tau21[0]"),
                #Variable_ttHbb(event = event, name = "ljet_tau21_wta[0]"),
                #Variable_ttHbb(event = event, name = "ljet_tau32[0]"),
                #Variable_ttHbb(event = event, name = "ljet_tau32_wta[0]"),

                #rcjet_d12,
                #rcjet_d23,
                #rcjet_e,
                #rcjet_eta,
                #rcjet_phi,
                #rcjet_pt,

                Variable_ttHbb(name = "class", value = class_label)
            ]
            if detail:
                log.info("event variable details:")
                log.info("\nnumber of variables: {number}".format(number = len(line)))
                table_contents = [["variable value", "variable type"]]
                for variable in line:
                    table_contents.append([str(variable.name()), str(type(variable.value()))])
                print(
                    pyprel.Table(
                        contents = table_contents,
                    )
                )
                detail = False
            if include_headings and not append:
                headings = [variable.name() for variable in line]
                writer.writerow(headings)
                include_headings = False
            values = [variable.value() for variable in line]
            writer.writerow(values)
        print(progress.add_datum(fraction = index / number_of_events))

    print("")
    log.info("{number_selected} events of {number_total} passed selection".format(
        number_selected = index_selected,
        number_total    = index
    ))

    print("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
