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

    --tree=TEXT              tree name                           [default: nominal_Loose]
    --maxevents=INT          maximum number of events to collate [default: none]
    --headings=BOOL          include headings at top of CSV file [default: true]
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
import pyprel
import shijian

name    = "ttHbb_ROOT_file_to_CSV_file"
version = "2017-04-21T0117Z"
logo    = name

def select_event(
    event     = None,
    selection = "ejets"
    ):

    """
    Select a HEP event.
    """

    if "ejets" in selection:
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
    #if "mujets" in selection:
    #    # Require a number of leptons.
    #    # Require >= 4 jets.
    #    # Require a single large-R jet.
    #    if                               \
    #        0 < len(event.mu_pt) < 2 and \
    #        event.nJets >= 4         and \
    #        event.nLjets >= 1:
    #        return True
    #    else:
    #        return False

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

    headings = [
        #"Aplan_bjets",
        "Aplan_jets",
        "Centrality_all",
        "ClassifBDTOutput_6jsplit",
        "ClassifBDTOutput_basic",
        "ClassifBDTOutput_withReco_6jsplit",
        "ClassifBDTOutput_withReco_basic",
        "ClassifHPLUS_Semilep_HF_BDT200_Output",
        "ClassifHPLUS_Semilep_HF_BDT225_Output",
        "ClassifHPLUS_Semilep_HF_BDT250_Output",
        "ClassifHPLUS_Semilep_HF_BDT275_Output",
        "ClassifHPLUS_Semilep_HF_BDT300_Output",
        "ClassifHPLUS_Semilep_HF_BDT350_Output",
        "ClassifHPLUS_Semilep_HF_BDT400_Output",
        "ClassifHPLUS_Semilep_HF_BDT500_Output",
        "ClassifHPLUS_Semilep_INC_BDT1000_Output",
        "ClassifHPLUS_Semilep_INC_BDT2000_Output",
        "ClassifHPLUS_Semilep_INC_BDT200_Output",
        "ClassifHPLUS_Semilep_INC_BDT225_Output",
        "ClassifHPLUS_Semilep_INC_BDT250_Output",
        "ClassifHPLUS_Semilep_INC_BDT275_Output",
        "ClassifHPLUS_Semilep_INC_BDT300_Output",
        "ClassifHPLUS_Semilep_INC_BDT350_Output",
        "ClassifHPLUS_Semilep_INC_BDT400_Output",
        "ClassifHPLUS_Semilep_INC_BDT500_Output",
        "ClassifHPLUS_Semilep_INC_BDT600_Output",
        "ClassifHPLUS_Semilep_INC_BDT700_Output",
        "ClassifHPLUS_Semilep_INC_BDT800_Output",
        "ClassifHPLUS_Semilep_INC_BDT900_Output",
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
        "FirstLjetM",
        "FirstLjetPt",
        "H1_all",
        "H4_all",
        "HhadT_nJets",
        "HhadT_nLjets",
        "HiggsbbM",
        "HiggsjjM",
        "HT_all",
        "HT_jets",
        "HT_ljets",
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
        "NBFricoNN_ljets",
        "nBjetOutsideLjet",
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
        "nJetOutsideLjet",
        "Njet_pt40",
        "Njet_pt40",
        "nJets",
        "nLjet_m100",
        "nLjet_m50",
        "nLjets",
        "nMuons",
        "nPrimaryVtx",
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

        "el1_charge",
        "el1_d0sig",
        "el1_delta_z0_sintheta",
        "el1_e",
        "el1_eta",
        "el1_phi",
        "el1_pt",
        "el1_topoetcone20",

        #"mu1_charge",
        #"mu1_d0sig",
        #"mu1_delta_z0_sintheta",
        #"mu1_e",
        #"mu1_eta",
        #"mu1_phi",
        #"mu1_pt",
        #"mu1_topoetcone20",

        "jet1_e",
        "jet1_eta",
        "jet1_jvt",
        "jet1_mv2c10",
        "jet1_mv2c20",
        "jet1_phi",
        "jet1_pt",
        "jet1_semilepMVAreco_recoBDT_cand",
        "jet1_semilepMVAreco_recoBDT_cand_6jsplit",
        "jet1_semilepMVAreco_recoBDT_withH_cand",
        "jet1_semilepMVAreco_recoBDT_withH_cand_6jsplit",

        "jet2_e",
        "jet2_eta",
        "jet2_jvt",
        "jet2_mv2c10",
        "jet2_mv2c20",
        "jet2_phi",
        "jet2_pt",
        "jet2_semilepMVAreco_recoBDT_cand",
        "jet2_semilepMVAreco_recoBDT_cand_6jsplit",
        "jet2_semilepMVAreco_recoBDT_withH_cand",
        "jet2_semilepMVAreco_recoBDT_withH_cand_6jsplit",

        "jet3_e",
        "jet3_eta",
        "jet3_jvt",
        "jet3_mv2c10",
        "jet3_mv2c20",
        "jet3_phi",
        "jet3_pt",
        "jet3_semilepMVAreco_recoBDT_cand",
        "jet3_semilepMVAreco_recoBDT_cand_6jsplit",
        "jet3_semilepMVAreco_recoBDT_withH_cand",
        "jet3_semilepMVAreco_recoBDT_withH_cand_6jsplit",

        "jet4_e",
        "jet4_eta",
        "jet4_jvt",
        "jet4_mv2c10",
        "jet4_mv2c20",
        "jet4_phi",
        "jet4_pt",
        "jet4_semilepMVAreco_recoBDT_cand",
        "jet4_semilepMVAreco_recoBDT_cand_6jsplit",
        "jet4_semilepMVAreco_recoBDT_withH_cand",
        "jet4_semilepMVAreco_recoBDT_withH_cand_6jsplit",

        #"ljet_C2",
        #"ljet_D2",
        #"ljet_e",
        #"ljet_eta",
        #"ljet_m",
        #"ljet_phi",
        #"ljet_pt",
        #"ljet_sd12",
        #"ljet_sd23",
        #"ljet_tau21",
        #"ljet_tau21_wta",
        #"ljet_tau32",
        #"ljet_tau32_wta",

        #"rcjet_d12",
        #"rcjet_d23",
        #"rcjet_e",
        #"rcjet_eta",
        #"rcjet_phi",
        #"rcjet_pt",
        "class"
    ]

    log.info("{number} variables to collate:\n\n{variables}".format(
        number    = len(headings),
        variables = ", ".join(headings)
    ))

    if not append and include_headings:
        writer.writerow(headings)

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
            selection = "ejets"
            ):
            index_selected = index_selected + 1
            if                                           \
                maximum_number_of_events is not None and \
                index_selected > maximum_number_of_events:
                break
            line = [
                #event.Aplan_bjets,
                event.Aplan_jets,
                event.Centrality_all,
                event.ClassifBDTOutput_6jsplit,
                event.ClassifBDTOutput_basic,
                event.ClassifBDTOutput_withReco_6jsplit,
                event.ClassifBDTOutput_withReco_basic,
                event.ClassifHPLUS_Semilep_HF_BDT200_Output,
                event.ClassifHPLUS_Semilep_HF_BDT225_Output,
                event.ClassifHPLUS_Semilep_HF_BDT250_Output,
                event.ClassifHPLUS_Semilep_HF_BDT275_Output,
                event.ClassifHPLUS_Semilep_HF_BDT300_Output,
                event.ClassifHPLUS_Semilep_HF_BDT350_Output,
                event.ClassifHPLUS_Semilep_HF_BDT400_Output,
                event.ClassifHPLUS_Semilep_HF_BDT500_Output,
                event.ClassifHPLUS_Semilep_INC_BDT1000_Output,
                event.ClassifHPLUS_Semilep_INC_BDT2000_Output,
                event.ClassifHPLUS_Semilep_INC_BDT200_Output,
                event.ClassifHPLUS_Semilep_INC_BDT225_Output,
                event.ClassifHPLUS_Semilep_INC_BDT250_Output,
                event.ClassifHPLUS_Semilep_INC_BDT275_Output,
                event.ClassifHPLUS_Semilep_INC_BDT300_Output,
                event.ClassifHPLUS_Semilep_INC_BDT350_Output,
                event.ClassifHPLUS_Semilep_INC_BDT400_Output,
                event.ClassifHPLUS_Semilep_INC_BDT500_Output,
                event.ClassifHPLUS_Semilep_INC_BDT600_Output,
                event.ClassifHPLUS_Semilep_INC_BDT700_Output,
                event.ClassifHPLUS_Semilep_INC_BDT800_Output,
                event.ClassifHPLUS_Semilep_INC_BDT900_Output,
                event.dEtajj_MaxdEta,
                event.dRbb_avg,
                event.dRbb_MaxM,
                event.dRbb_MaxPt,
                event.dRbb_min,
                event.dRbj_Wmass,
                event.dRHl_MaxdR,
                event.dRHl_MindR,
                event.dRjj_min,
                event.dRlepbb_MindR,
                event.dRlj_MindR,
                event.dRuu_MindR,
                event.FirstLjetM,
                event.FirstLjetPt,
                event.H1_all,
                event.H4_all,
                event.HhadT_nJets,
                event.HhadT_nLjets,
                event.HiggsbbM,
                event.HiggsjjM,
                event.HT_all,
                event.HT_jets,
                event.HT_ljets,
                event.Mbb_MaxM,
                event.Mbb_MaxPt,
                event.Mbb_MindR,
                event.Mbj_MaxPt,
                event.Mbj_MindR,
                event.Mbj_Wmass,
                event.met_met,
                event.met_phi,
                event.MHiggs,
                event.Mjj_HiggsMass,
                event.Mjjj_MaxPt,
                event.Mjj_MaxPt,
                event.Mjj_MindR,
                event.Mjj_MinM,
                event.mu,
                event.Muu_MindR,
                event.NBFricoNN_dil,
                event.NBFricoNN_ljets,
                event.nBjetOutsideLjet,
                event.nBTags,
                event.nBTags30,
                event.nBTags50,
                event.nBTags60,
                event.nBTags70,
                event.nBTags77,
                event.nBTags80,
                event.nBTags85,
                event.nBTags90,
                event.nBTagsFlatBEff_30,
                event.nBTagsFlatBEff_40,
                event.nBTagsFlatBEff_50,
                event.nBTagsFlatBEff_60,
                event.nBTagsFlatBEff_70,
                event.nBTagsFlatBEff_77,
                event.nBTagsFlatBEff_85,
                event.nElectrons,
                event.nHFJets,
                event.NHiggs_30,
                event.nJetOutsideLjet,
                event.Njet_pt40,
                event.Njet_pt40,
                event.nJets,
                event.nLjet_m100,
                event.nLjet_m50,
                event.nLjets,
                event.nMuons,
                event.nPrimaryVtx,
                event.pT_jet3,
                event.pT_jet5,
                event.pTuu_MindR,
                event.SecondLjetM,
                event.SecondLjetPt,
                event.semilepMVAreco_b1higgsbhadtop_dR,
                event.semilepMVAreco_bbhiggs_dR,
                event.semilepMVAreco_BDT_output,
                event.semilepMVAreco_BDT_output_6jsplit,
                event.semilepMVAreco_BDT_output_truthMatchPattern,
                event.semilepMVAreco_BDT_withH_output,
                event.semilepMVAreco_BDT_withH_output_6jsplit,
                event.semilepMVAreco_BDT_withH_output_truthMatchPattern,
                event.semilepMVAreco_hadWb1Higgs_mass,
                event.semilepMVAreco_higgsbhadtop_withH_dR,
                event.semilepMVAreco_higgsbleptop_mass,
                event.semilepMVAreco_higgsbleptop_withH_dR,
                event.semilepMVAreco_higgslep_dR,
                event.semilepMVAreco_higgsleptop_dR,
                event.semilepMVAreco_higgs_mass,
                event.semilepMVAreco_higgsq1hadW_mass,
                event.semilepMVAreco_higgsttbar_withH_dR,
                event.semilepMVAreco_leptophadtop_dR,
                event.semilepMVAreco_leptophadtop_withH_dR,
                event.semilepMVAreco_Ncombinations,
                event.semilepMVAreco_nuApprox_recoBDT,
                event.semilepMVAreco_nuApprox_recoBDT_6jsplit,
                event.semilepMVAreco_nuApprox_recoBDT_withH,
                event.semilepMVAreco_nuApprox_recoBDT_withH_6jsplit,
                event.semilepMVAreco_ttH_Ht_withH,
                event.ttHF_mva_discriminant,

                #event.el_charge[0],
                event.el_d0sig[0],
                event.el_delta_z0_sintheta[0],
                event.el_e[0],
                event.el_eta[0],
                event.el_phi[0],
                event.el_pt[0],
                event.el_topoetcone20[0],

                #event.mu_charge[0],
                #event.mu_d0sig[0],
                #event.mu_delta_z0_sintheta[0],
                #event.mu_e[0],
                #event.mu_eta[0],
                #event.mu_phi[0],
                #event.mu_pt[0],
                #event.mu_topoetcone20[0],

                event.jet_e[0],
                event.jet_eta[0],
                event.jet_jvt[0],
                event.jet_mv2c10[0],
                event.jet_mv2c20[0],
                event.jet_phi[0],
                event.jet_pt[0],
                event.jet_semilepMVAreco_recoBDT_cand[0],
                event.jet_semilepMVAreco_recoBDT_cand_6jsplit[0],
                event.jet_semilepMVAreco_recoBDT_withH_cand[0],
                event.jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[0],

                event.jet_e[1],
                event.jet_eta[1],
                event.jet_jvt[1],
                event.jet_mv2c10[1],
                event.jet_mv2c20[1],
                event.jet_phi[1],
                event.jet_pt[1],
                event.jet_semilepMVAreco_recoBDT_cand[1],
                event.jet_semilepMVAreco_recoBDT_cand_6jsplit[1],
                event.jet_semilepMVAreco_recoBDT_withH_cand[1],
                event.jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[1],

                event.jet_e[2],
                event.jet_eta[2],
                event.jet_jvt[2],
                event.jet_mv2c10[2],
                event.jet_mv2c20[2],
                event.jet_phi[2],
                event.jet_pt[2],
                event.jet_semilepMVAreco_recoBDT_cand[2],
                event.jet_semilepMVAreco_recoBDT_cand_6jsplit[2],
                event.jet_semilepMVAreco_recoBDT_withH_cand[2],
                event.jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[2],

                event.jet_e[3],
                event.jet_eta[3],
                event.jet_jvt[3],
                event.jet_mv2c10[3],
                event.jet_mv2c20[3],
                event.jet_phi[3],
                event.jet_pt[3],
                event.jet_semilepMVAreco_recoBDT_cand[3],
                event.jet_semilepMVAreco_recoBDT_cand_6jsplit[3],
                event.jet_semilepMVAreco_recoBDT_withH_cand[3],
                event.jet_semilepMVAreco_recoBDT_withH_cand_6jsplit[3],

                #event.ljet_C2,
                #event.ljet_D2,
                #event.ljet_e,
                #event.ljet_eta,
                #event.ljet_m,
                #event.ljet_phi,
                #event.ljet_pt,
                #event.ljet_sd12,
                #event.ljet_sd23,
                #event.ljet_tau21,
                #event.ljet_tau21_wta,
                #event.ljet_tau32,
                #event.ljet_tau32_wta,

                #event.rcjet_d12,
                #event.rcjet_d23,
                #event.rcjet_e,
                #event.rcjet_eta,
                #event.rcjet_phi,
                #event.rcjet_pt,

                class_label
            ]
            if detail:
                log.info("event variable details:")
                table_contents = [["variable value", "variable type"]]
                for variable in line:
                    table_contents.append([str(variable), str(type(variable))])
                print(
                    pyprel.Table(
                        contents = table_contents,
                    )
                )
                detail = False
            writer.writerow(line)
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
