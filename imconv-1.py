#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# imconv-1                                                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program converts images to simple pixel formats, validates simple pixel #
# formats and converts simple pixel formats to images.                         #
#                                                                              #
# 2015 Will Breaden Madden, w.bm@cern.ch                                       #
#                                                                              #
# Subject to ATLAS Data Access Policy, this software is released under the     #
# terms of the GNU General Public License version 3 (GPLv3).                   #
#                                                                              #
# For a copy of the ATLAS Data Access Policy, see                              #
# DOI: 10.7483/OPENDATA.ATLAS.T9YR.Y7MZ or http://opendata.cern.ch/record/413. #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# http://www.gnu.org/licenses/.                                                #
#                                                                              #
################################################################################

Usage:
    program [options]

Options:
    -h, --help                   display help message
    --version                    display version and exit
    -v, --verbose                verbose logging
    -u, --username=USERNAME      username
    --inputimage=FILENAME        input image file
    --outputpixels=FILENAME      output pixels -- ASCII format
    --inputpixels=FILENAME       input pixels -- ASCII format
    --outputimage=FILENAME       output image file
    --outputimagewidth=NUMBER    width of output image in pixels [default: 2379]
    --convertImageToPixels       mode to convert image to pixels
    --validatepixels             mode to validate pixels
    --convertPixelsToImage       mode to convert pixels to image
"""

name    = "imconv-1"
version = "2015-06-22T1453Z"

import smuggle # http://cern.ch/go/PG8f
import os
import sys
import logging
import urllib
import imp
import time
import PIL
import re
import ast
docopt = smuggle.smuggle(
    moduleName = "docopt",
    URL = "https://rawgit.com/docopt/docopt/master/docopt.py"
)
technicolor = smuggle.smuggle(
    moduleName = "technicolor",
    URL = "https://rawgit.com/wdbm/technicolor/master/technicolor.py"
)
shijian = smuggle.smuggle(
    moduleName = "shijian",
    URL = "https://rawgit.com/wdbm/shijian/master/shijian.py"
)
pyprel = smuggle.smuggle(
    moduleName = "pyprel",
    URL = "https://rawgit.com/wdbm/pyprel/master/pyprel.py"
)

@shijian.timer
def main(options):

    global program
    program = Program(options = options)

    # access options and arguments
    input_image_filename         = options["--inputimage"]
    output_pixels_filename       = options["--outputpixels"]
    input_pixels_filename        = options["--inputpixels"]
    output_image_filename        = options["--outputimage"]
    output_image_width           = int(options["--outputimagewidth"])
    mode_convert_image_to_pixels = bool(options["--convertImageToPixels"])
    mode_validate_pixels         = bool(options["--validatepixels"])
    mode_convert_pixels_to_image = bool(options["--convertPixelsToImage"])

    log.info("")

    if mode_convert_image_to_pixels is True:
        log.info("convert image to pixels")
        # Access the input image.
        log.info("access input image")
        input_image = PIL.Image.open(input_image_filename)
        log.info("input image mode: {imageMode}".format(imageMode = image.mode))
        log.info("input image size: {imageSize}".format(imageSize = image.size))
        pixels = list(input_image.getdata())
        pixels_text = str(pixels)
        # Create and save the output pixels.
        output_pixels_file = open(output_pixels_filename, "w")
        output_pixels_file.truncate()
        log.info("save output pixels {outputPixelsFilename}".format(
            outputPixelsFilename = output_pixels_filename
        ))
        output_pixels_file.write(pixels_text)
        output_pixels_file.close()
    elif mode_validate_pixels is True:
        log.info("validate pixels")
        # Access input pixels.
        log.info("access input pixels")
        with open(input_pixels_filename) as input_pixels_file:
            text = input_pixels_file.read()
        parts = text[2:-2].split("), (")
        log.info("validate pixels")
        for n, part in enumerate(parts):
            if not re.match(r"^\d+, \d+, \d+, \d+$", part):
                print("tuple {tuple_index} malformed: {tuple}".format(
                    tuple_index = n,
                    tuple = part
                )) 
    elif mode_convert_pixels_to_image is True:
        log.info("convert pixels to image")
        # Access input pixels.
        log.info("access input pixels")
        input_pixels_file = open(input_pixels_filename)
        pixels = input_pixels_file.read()
        pixels = ast.literal_eval(pixels)
        # Determine the image height by determining the maximum number of image
        # widths are possible with the available pixel data.
        log.info("determine output image dimensions")
        imageMode = "RGBA"
        imageWidth = output_image_width # e.g. 2379
        imageHeight = int(len(pixels)/imageWidth) # e.g. 2196
        imageSize = (imageWidth, imageHeight)
        print("output image mode: {imageMode}".format(imageMode = imageMode))
        print("output image size: {imageSize}".format(imageSize = imageSize))
        # Create and save the output image.
        log.info("create output image")
        output_image_file = Image.new(imageWidth, imageHeight)
        output_image_file.putdata(pixels)
        log.info("save output image {outputImageFilename}".format(
            outputImageFilename = output_image_filename
        ))
        output_image_file.save(output_image_filename)
    else:
        log.info("no operation selected\n")
        print(__doc__)

    log.info("")

    program.terminate()

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
        log.info("time statistics report:\n{report}".format(
            report = shijian.clocks.report()
        ))
        log.info("terminate {name}".format(
            name = self.name
        ))
        pyprel.printLine()
        sys.exit()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)