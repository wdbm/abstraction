#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# imconv-3                                                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program converts images to simple pixel formats, validates simple pixel #
# formats and converts simple pixel formats to simple pixel formats that are   #
# easy to edit and to images.                                                  #
#                                                                              #
# 2015 Will Breaden Madden, w.bm@cern.ch                                       #
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
    -h, --help                   display help message
    --version                    display version and exit
    -v, --verbose                verbose logging
    -u, --username=USERNAME      username
    --inputimage=FILENAME        input image file
    --outputpixels=FILENAME      output pixels -- ASCII format
    --inputpixels=FILENAME       input pixels -- ASCII format
    --outputimage=FILENAME       output image file
    --outputimagewidth=NUMBER    width of output image in pixels [default: 2379]
    --convertimagetopixels       mode to convert image to pixels
    --validatepixels             mode to validate pixels
    --convertpixelstoimage       mode to convert pixels to image
"""

name    = "imconv-3"
version = "2015-08-21T1543Z"

import os
import sys
import logging
import urllib
import imp
import time
from PIL import Image
import re
import ast
import docopt
import technicolor
import shijian
import pyprel

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
    mode_convert_image_to_pixels = bool(options["--convertimagetopixels"])
    mode_validate_pixels         = bool(options["--validatepixels"])
    mode_convert_pixels_to_image = bool(options["--convertpixelstoimage"])

    log.info("")

    if mode_convert_image_to_pixels is True:
        log.info("convert image to pixels")
        # Access the input image.
        log.info("access input image")
        input_image = Image.open(input_image_filename)
        log.info("input image mode: {imageMode}".format(imageMode = input_image.mode))
        log.info("input image size: {imageSize}".format(imageSize = input_image.size))
        pixels = list(input_image.getdata())
        pixels_text = str(pixels)
        # Add newlines.
        pixels_text = pixels_text.replace("), (", "),\n(")
        # Save the pixels.
        output_pixels_file = open(output_pixels_filename, "w")
        output_pixels_file.truncate()
        log.info("save output pixels {outputPixelsFilename}".format(
            outputPixelsFilename = output_pixels_filename
        ))
        output_pixels_file.write(pixels_text)
        output_pixels_file.close()
    
    elif mode_validate_pixels:
        log.info("validate pixels with newlines")
        # Access input pixels.
        log.info("access input pixels")
        with open(input_pixels_filename) as input_pixels_file:
            text = input_pixels_file.read()
        parts = text.split("\n")
        log.info("replace invalidate pixels")
        for n, part in enumerate(parts):
            # Create a temporary part for regex examination.
            tmp_part = part.strip("),").strip("(")
            if not re.match(r"^\d+, \d+, \d+, \d+$", tmp_part):
                log.info("tuple {tuple_index} malformed: {tuple} -- replacing with (0, 0, 0, 255)".format(
                    tuple_index = n,
                    tuple = tmp_part
                ))
                parts[n] = "(0, 0, 0, 255)"
        # Remove trailing commas.
        parts = [part.strip(",") for part in parts]
        pixels_text = str(parts)
        pixels_text = pixels_text.replace(")', '(", ")',\n'(")
        # Save the pixels.
        output_pixels_file = open(output_pixels_filename, "w")
        output_pixels_file.truncate()
        log.info("save output pixels {outputPixelsFilename}".format(
            outputPixelsFilename = output_pixels_filename
        ))
        output_pixels_file.write(pixels_text)
        output_pixels_file.close()

    elif mode_convert_pixels_to_image is True:
        log.info("convert pixels to image")
        # Access input pixels.
        log.info("access input pixels")
        input_pixels_file = open(input_pixels_filename)
        pixels = input_pixels_file.read()
        pixels = ast.literal_eval(pixels)
        #pixels = pixels[:10000]
        # Determine the image height by determining the maximum number of image
        # widths that are possible with the available pixel data.
        log.info("determine output image dimensions")
        imageMode = "RGBA"
        imageWidth = output_image_width # e.g. 2379
        imageHeight = int(len(pixels)/imageWidth) # e.g. 2196
        imageSize = (imageWidth, imageHeight)
        print type(imageSize)
        print("output image mode: {imageMode}".format(imageMode = imageMode))
        print("output image size: {imageSize}".format(imageSize = imageSize))

        pixels = [pixel.replace("))", ")").replace("((", "(").replace("),)", "), ") for pixel in pixels]

        # Convert list of pixel strings to list of pixel tuples.
        pixels = [ast.literal_eval(re.sub(r'\b0+\B', '', pixel)) for pixel in pixels]

        # Use only the number of pixels to make the image of the defined
        # dimensions.
        numberOfPixels = imageWidth * imageHeight
        pixels = pixels[:numberOfPixels]

        # Create and save the output image.
        log.info("create output image")
        #output_image_file = Image.new(imageMode, imageSize)
        output_image_file = Image.new("RGBA", (2379, 2069))

        log.info("number of pixels: {numberOfPixels}".format(numberOfPixels = len(pixels)))

        #for pixel in pixels:
        #    if str(type(pixel)) is not "<type 'tuple'>":
        #        print("not tuple: {pixel}".format(pixel = pixel))

        pixels = pixels[:4922151]

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
