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
    -h, --help                 display help message
    --version                  display version and exit
    -v, --verbose              verbose logging
    -s, --silent               silent
    -u, --username=USERNAME    username
    --inputimage=FILENAME      input image file
    --outputpixels=FILENAME    output pixels -- ASCII format
    --inputpixels=FILENAME     input pixels -- ASCII format
    --outputimage=FILENAME     output image file
    --outputimagewidth=NUMBER  width of output image in pixels [default: 2379]
    --convertimagetopixels     mode to convert image to pixels
    --validatepixels           mode to validate pixels
    --convertPixelsToImage     mode to convert pixels to image
"""

name    = "imconv-1"
version = "2015-11-17T1259Z"
logo    = None

import os
import sys
import logging
import urllib
import imp
import time
import PIL
import re
import ast
import docopt
import technicolor
import shijian
import pyprel
import propyte

@shijian.timer
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

    # access options and arguments
    input_image_filename         = options["--inputimage"]
    output_pixels_filename       = options["--outputpixels"]
    input_pixels_filename        = options["--inputpixels"]
    output_image_filename        = options["--outputimage"]
    output_image_width           = int(options["--outputimagewidth"])
    mode_convert_image_to_pixels = bool(options["--convertimagetopixels"])
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

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
