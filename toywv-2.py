#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# toywv-2                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This toy program converts a natural language text expression to a word       #
# vector and then converts the resultant word vector to a natural language     #
# text expression by selecting from a set of existing dictionary of pairs of   #
# natural language expressions and word vectors.                               #
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

Usage:
    program [options]

Options:
    -h, --help                Show this help message.
    --version                 Show the version and exit.
    -v, --verbose             Show verbose logging.
    -u, --username=USERNAME   username
    --expression=TEXT         text expression to convert to word vector
                              [default: All those moments will be lost in time.]
    --wordvectormodel=NAME    word vector model
                              [default: Brown_corpus.wvm]
"""

name    = "toywv-2"
version = "2015-10-12T2209Z"

import os
import sys
import subprocess
import time
import datetime
import logging
import technicolor
import inspect
import docopt
import shijian
import dataset
import abstraction
from gensim.models import Word2Vec
import math
import numpy
import pyprel

def main(options):

    global program
    program = Program(options = options)

    # Define a dictionary of natural language expressions and word vectors.
    storedExpressions = {
        "This is a test.":
            numpy.array([
                -0.3828682,  -0.36397889,  0.46676171,
                 0.32530552,  0.20376287, -0.41326976,
                -0.58228827,  0.05073506, -0.29834735,
                 0.62523258,  0.48247468,  0.63565594,
                 0.61466146, -0.05790123,  0.49383548,
                 0.17871667,  0.26640224, -0.05172781,
                -0.43991241,  0.8027305,   0.13174312,
                -0.70332521, -0.56575418, -0.21705133,
                -0.93002945,  0.04151381, -0.15113404,
                 0.06264834,  0.03022593, -0.00822711,
                -0.23755306, -0.9215641,   0.21348992,
                 0.38396335,  0.3020944,  -0.08034055,
                -0.36891997, -0.86551458, -1.02402425,
                 0.03633916,  0.34436008,  0.43058148,
                -0.32728755,  0.50974292, -0.31518513,
                -0.63085675, -0.40564051,  0.30009648,
                -0.06426927, -0.6588546,   0.06724164,
                 0.08611558, -0.13476974,  0.43107161,
                -0.26038069,  0.03187743,  0.05931987,
                 0.28155532,  0.3636784,  -0.76867509,
                -0.2253349,  -0.77433741,  0.01924273,
                 0.63751495,  0.03874384,  0.28651205,
                 0.14867969, -0.2256701 ,  0.23747981,
                 0.12383705,  0.27097231, -0.06902695,
                 0.06664967,  0.05863822, -0.06882346,
                 0.59539717,  0.08472043, -0.13579898,
                -0.31311297, -0.68136102,  0.33296993,
                 0.26578408, -0.55723149,  0.38583612,
                -0.18033087, -0.50730389,  0.39173275,
                 0.57567608, -0.42063141,  0.22387385,
                 0.473548,    0.41959459,  0.34881225,
                 0.1939103,  -0.54997987,  0.30737191,
                -0.6659264,   0.0437102,  -0.11230323,
                -0.13493723
            ],
                dtype = numpy.float32
        ),
        "All those moments will be lost in time.":
            numpy.array([
                -1.19203818e+00, -2.22961619e-01,  6.69643760e-01,
                 3.70975524e-01, -6.15832031e-01, -4.36573088e-01,
                -6.77924156e-01,  6.26985192e-01,  1.36510044e-01,
                 1.09196387e-01,  7.61598766e-01,  7.17226386e-01,
                -1.08178332e-01, -1.00655735e+00,  7.45964348e-01,
                 1.64966106e-01,  5.85332870e-01, -3.83911550e-01,
                -6.85201228e-01,  1.31213856e+00,  8.04567218e-01,
                -1.28810382e+00, -2.52677381e-01, -9.27993536e-01,
                -4.17307138e-01, -4.56952095e-01, -7.27599859e-01,
                 7.54008472e-01,  6.67124987e-04,  2.75971144e-01,
                 2.75658131e-01, -6.79417193e-01, -1.73686996e-01,
                 8.78942013e-01,  4.39480424e-01, -6.37802243e-01,
                -6.99860230e-02, -7.99779966e-02, -7.58146644e-02,
                 8.09784770e-01, -3.71645451e-01,  1.04973994e-01,
                -1.34749603e+00,  2.96185315e-01,  5.85593104e-01,
                -1.40544206e-01, -3.77467513e-01,  3.46597135e-01,
                 2.56733745e-01,  4.04421866e-01,  1.57907709e-01,
                 3.00843865e-01, -5.41967154e-01,  5.51929235e-01,
                -1.69145897e-01,  4.42785203e-01, -2.69805342e-02,
                 1.31654418e+00,  3.19460958e-01,  5.08862257e-01,
                 3.44371676e-01, -6.95496798e-01,  4.88163918e-01,
                 2.55316138e-01,  5.03436685e-01,  9.24195647e-02,
                -2.38671958e-01, -8.97032142e-01, -3.73697281e-03,
                 2.99875826e-01,  1.65674359e-01,  2.01489821e-01,
                 1.58179402e-02,  1.30668238e-01, -1.56954467e-01,
                -2.88258016e-01,  6.76668346e-01, -3.77742261e-01,
                 2.20978767e-01, -6.34561360e-01,  8.33457410e-01,
                -2.13193640e-01, -6.35235757e-02,  1.89480215e-01,
                 6.02166615e-02, -6.64785147e-01,  1.07347333e+00,
                 6.22629285e-01, -4.63467717e-01, -1.13483839e-01,
                 3.43968630e-01,  2.75979757e-01, -1.28710240e-01,
                 1.50670230e+00, -3.10248852e-01,  3.29222828e-01,
                 1.64443821e-01, -7.78683364e-01, -9.80837345e-02,
                -1.07415296e-01
            ],
                dtype = numpy.float32
            ),
        "All those moments were lost in time.":
            numpy.array([
                -0.94025505, -0.45476836,  0.41891485,
                 1.06683254, -0.49607083, -0.60043317,
                -0.55656326,  0.05368682,  0.20896676,
                 0.19261286,  0.51067233,  0.01298623,
                -0.67276001, -0.51130211,  0.61433661,
                 0.03579944,  0.4515644 , -0.19222273,
                -0.3919456,   0.65209424,  0.98329031,
                -0.78390068, -0.0611292 , -0.88086104,
                 0.25153416, -0.16051427, -0.33223695,
                 0.86147106, -0.19569418, -0.21456225,
                 0.27583197, -0.65764415, -0.76533222,
                 0.78306556,  0.84534264, -0.26408321,
                 0.04312199, -0.00636051,  0.1322974,
                 0.72321951, -0.01186696,  0.40505514,
                -0.87730938,  0.58147532,  0.89738142,
                -0.16748536, -0.38406748, -0.12007161,
                 0.49123141,  0.48998365,  0.15616624,
                 0.52637529, -0.66329396,  0.10376941,
                -0.33025965,  0.04188792,  0.30536407,
                 0.38240519,  0.01627355,  1.23012972,
                 0.46352714, -0.74617827,  0.43505573,
                -0.16246299,  0.34668511, -0.02247265,
                -0.34742412, -0.64483654, -0.2243523,
                 0.04222834,  0.42057285,  0.22310457,
                 0.36833102, -0.05716853, -0.44688487,
                -0.51298815,  0.61859602, -0.21154809,
                -0.08168469, -0.15004104,  0.21371906,
                 0.21713886,  0.21935812,  0.04912762,
                 0.02854752, -0.55747426,  0.70036995,
                 0.20306921, -0.46556181, -0.10637223,
                 0.60909081,  0.55366743, -0.22907487,
                 1.13089538,  0.34430629,  0.35133895,
                 0.085365,   -0.58662325, -0.13062993,
                -0.04200239
            ],
                dtype = numpy.float32
            ),
        "All those moments are lost in time.":
            numpy.array([
                -0.78943789, -0.30322614,  0.3780162,
                 0.80896467, -0.42042252, -0.64176518,
                -0.51211309, -0.1537444,  -0.04233316,
                 0.07710438,  0.66949254,  0.37771451,
                -0.74869132, -0.55132926,  0.53695548,
                -0.11229508,  0.6673997,  -0.34724045,
                -0.42173663,  0.7451877,   1.01433206,
                -0.85418928, -0.31583607, -0.6812892,
                 0.42722669, -0.43322188, -0.35293943,
                 0.7662127 , -0.30090365, -0.13694993,
                -0.04172039, -0.65059775, -0.62617165,
                 0.71341687,  0.82349646, -0.31194365,
                 0.00356466, -0.32218212,  0.15857732,
                 0.82880032,  0.0566355 ,  0.43106011,
                -1.01921201,  0.51658779,  0.8068108,
                -0.09396499, -0.37920368, -0.08726061,
                 0.29975161,  0.25999272,  0.23571083,
                 0.24800834, -0.73045135,  0.19150458,
                -0.19696848, -0.11186107,  0.1336731,
                 0.33246318,  0.22474274,  1.15420532,
                 0.39482915, -0.70385826,  0.54841375,
                -0.03638301,  0.54499787,  0.02484709,
                -0.2070619 , -0.69282937, -0.21465099,
                 0.11578664,  0.22713676,  0.21237181,
                 0.2007356,   0.14489903, -0.37357002,
                -0.50091666,  0.59818357, -0.36113665,
                 0.06037673, -0.26377741,  0.31544513,
                -0.23714744, -0.01429842,  0.17592101,
                -0.16280818, -0.58340323,  0.63590413,
                 0.31803992, -0.47035503, -0.17544734,
                 0.66008455,  0.77849454, -0.04235193,
                 1.29202402,  0.12573826,  0.20377615,
                -0.08164676, -0.41151166, -0.1280518,
                 0.02905136
            ],
                dtype = numpy.float32),
    }

    model_word2vec = abstraction.load_word_vector_model(
        fileName = program.wordVectorModel
    )

    workingExpressionNL = program.expression

    # Convert the expression to a word vector.
    workingExpressionWV =\
        abstraction.convert_sentence_string_to_word_vector(
            sentenceString = workingExpressionNL,
            model_word2vec = model_word2vec
        )
    log.info(
        "word vector representation of expression \"{workingExpressionNL}\":"
        "\n{workingExpressionWV}".format(
            workingExpressionNL = workingExpressionNL,
            workingExpressionWV = workingExpressionWV
        )
    )

    # Define table headings.
    tableContents = [[
        "working expression natural language",
        "stored expression natural language",
        "absolute magnitude difference between working amd stored expression "
        "word vectors",
        "angle between working and stored expression word vectors"
    ]]

    # Compare the expression word vector representation to existing word
    # vectors.
    magnitude_differences   = []
    angles                  = []
    storedExpressionsNLList = []
    magnitude_workingExpressionWV = magnitude(workingExpressionWV)
    for storedExpressionNL in storedExpressions:
        storedExpressionWV = storedExpressions[storedExpressionNL]
        magnitude_storedExpressionWV = magnitude(storedExpressionWV)
        magnitude_difference_workingExpressionWV_storedExpressionWV = abs(
            magnitude_workingExpressionWV - magnitude_storedExpressionWV
        )
        angle_workingExpressionWV_storedExpressionWV = angle(
            workingExpressionWV,
            storedExpressionWV
        )
        # Store comparison results in lists.
        magnitude_differences.append(
            magnitude_difference_workingExpressionWV_storedExpressionWV
        )
        angles.append(
            angle_workingExpressionWV_storedExpressionWV
        )
        storedExpressionsNLList.append(
            storedExpressionNL
        )
        # Build table.
        tableContents.append([
            str(workingExpressionNL),
            str(storedExpressionNL),
            str(magnitude_difference_workingExpressionWV_storedExpressionWV),
            str(angle_workingExpressionWV_storedExpressionWV)]
        )

    # Record table.
    print(
        pyprel.Table(
            contents = tableContents
        )
    )

    log.info("")

    index_minimum_magnitude_differences =\
        magnitude_differences.index(min(magnitude_differences))
    index_minimum_angles = angles.index(min(angles))
    index_minimum_match_width = len(angles) / 4
    if abs(
        index_minimum_magnitude_differences - index_minimum_angles
    ) < index_minimum_match_width:
        log.info("translation: {translationExpressionNL}".format(
            translationExpressionNL =\
                storedExpressionsNLList[index_minimum_angles]
        ))
    else:
        log.error("unable to translate")
    
    log.info("")

    program.terminate()

def ensure_file_existence(fileName):
    log.debug("ensure existence of file {fileName}".format(
        fileName = fileName
    ))
    if not os.path.isfile(os.path.expandvars(fileName)):
        log.error("file {fileName} does not exist".format(
            fileName = fileName
        ))
        program.terminate()
        raise(Exception)
    else:
        log.debug("file {fileName} found".format(
            fileName = fileName
        ))

def dot_product(v1, v2):
  return(sum((a*b) for a, b in zip(v1, v2)))

def magnitude(v):
    return(numpy.linalg.norm(v))
    #return(math.sqrt(dot_product(v, v)))

def angle(v1, v2):
    cosine = dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
    cosine = 1 if cosine > 1 else cosine
    return(math.acos(cosine))

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # internal options
        self.displayLogo           = True

        # clock
        global clock
        clock = shijian.Clock(name = "program run time")

        # name, version, logo
        if "name" in globals():
            self.name              = name
        else:
            self.name              = None
        if "version" in globals():
            self.version           = version
        else:
            self.version           = None
        if "logo" in globals():
            self.logo              = logo
        elif "logo" not in globals() and hasattr(self, "name"):
            self.logo              = pyprel.renderBanner(
                                         text = self.name.upper()
                                     )
        else:
            self.displayLogo       = False
            self.logo              = None

        # options
        self.options               = options
        self.userName              = self.options["--username"]
        self.verbose               = self.options["--verbose"]
        self.expression            = self.options["--expression"]
        self.wordVectorModel       = self.options["--wordvectormodel"]

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")

        # logging
        global log
        log = logging.getLogger(__name__)
        logging.root.addHandler(technicolor.ColorisingStreamHandler())

        # logging level
        if self.verbose:
            logging.root.setLevel(logging.DEBUG)
        else:
            logging.root.setLevel(logging.INFO)

        # logging level
        if self.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        self.engage()

    def engage(
        self
        ):
        pyprel.printLine()
        # logo
        if self.displayLogo:
            log.info(pyprel.centerString(text = self.logo))
            pyprel.printLine()
        # engage alert
        if self.name:
            log.info("initiate {name}".format(
                name = self.name
            ))
        # version
        if self.version:
            log.info("version: {version}".format(
                version = self.version
            ))
        log.info("initiation time: {time}".format(
            time = clock.startTime()
        ))

    def terminate(
        self
        ):
        clock.stop()
        log.info("termination time: {time}".format(
            time = clock.stopTime()
        ))
        log.info("time full report:\n{report}".format(
            report = shijian.clocks.report(style = "full")
        ))
        log.info("time statistics report:\n{report}".format(
            report = shijian.clocks.report()
        ))
        log.info("terminate {name}".format(
            name = self.name
        ))
        pyprel.printLine()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
