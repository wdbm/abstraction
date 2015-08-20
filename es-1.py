#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# es-1                                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program generates dreams.                                               #
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
    -h, --help                 display help message
    --version                  display version and exit
    -v, --verbose              verbose logging
    -u, --username=USERNAME    username
    --inputImage=FILENAME      input image filename
                               [default: input.png]
    --outputImage=FILENAME     output image filename
                               [default: output.png]
    --recursiveZoom            recursive zoom mode
    --gpu                      engage GPU mode
"""

name    = "es-1"
version = "2015-08-20T1504Z"
logo    = "\n" + name

from cStringIO import StringIO
import numpy as np
import scipy.ndimage as nd
import PIL.Image
from google.protobuf import text_format
import caffe
import os
import sys
import time
import logging
import docopt
import technicolor
import shijian
import pyprel

@shijian.timer
def preprocess(net, image):
    '''
    convert to Caffe input image layout
    '''
    return np.float32(np.rollaxis(image, 2)[::-1]) - net.transformer.mean["data"]

@shijian.timer
def deprocess(net, image):
    '''
    convert from Caffe input image layout
    '''
    return np.dstack((image + net.transformer.mean["data"])[::-1])

@shijian.timer
def objective_L2(dst):
    dst.diff[:] = dst.data 

@shijian.timer
def make_step(
    net,
    step_size = 1.5,
    end       = "inception_4c/output", 
    jitter    = 32,
    clip      = True,
    objective = objective_L2
    ):
    '''
    basic gradient ascent step
    '''

    src = net.blobs["data"]
    dst = net.blobs[end]

    ox, oy = np.random.randint(- jitter, jitter + 1, 2)
    # Apply jitter shift.
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2)

    # Specify the optimisation objective.
    net.forward(end = end)
    objective(dst)
    net.backward(start = end)
    g = src.diff[0]
    # Apply normalised ascent step to the input image.
    src.data[:] += step_size / np.abs(g).mean() * g
    # Unshift the image.
    src.data[0] = np.roll(np.roll(src.data[0], - ox, - 1), -oy, -2)
            
    if clip:
        bias = net.transformer.mean["data"]
        src.data[:] = np.clip(src.data, -bias, 255-bias)  

@shijian.timer
def deepdream(
    net,
    base_image,
    iter_n       = 10,
    octave_n     = 4,
    octave_scale = 1.4, 
    end          = "inception_4c/output",
    clip         = True,
    **step_params
    ):
    '''
    an ascent through different scales called "octaves"
    '''    
    # Prepare base images for all octaves.
    octaves = [preprocess(net, base_image)]
    for i in xrange(octave_n-1):
        octaves.append(
            nd.zoom(
                octaves[-1], (1, 1.0 / octave_scale, 1.0 / octave_scale),
                order = 1
            )
        )

    src = net.blobs["data"]
    # Allocate image for network-produced details.
    detail = np.zeros_like(octaves[-1])
    for octave, octave_base in enumerate(octaves[::-1]):
        h, w = octave_base.shape[-2:]
        if octave > 0:
            # Upscale details from the previous octave.
            h1, w1 = detail.shape[-2:]
            detail = nd.zoom(
                detail,
                (1, 1.0 * h / h1, 1.0 * w/w1),
                order = 1
            )
        # Resize the network input image size.
        src.reshape(1, 3, h, w)
        src.data[0] = octave_base+detail
        for i in xrange(iter_n):
            make_step(net, end = end, clip = clip, **step_params)
            
            # visualisation
            vis = deprocess(net, src.data[0])
            # If clipping is disabled, adjust image contrast.
            if not clip:
                vis = vis*(255.0 / np.percentile(vis, 99.98))

            log.info("octave: {octave}, index: {index}, blob/layer: {end}, dimensions: {shape}".format(
                octave = octave,
                index  = i,
                end    = end,
                shape  = vis.shape,
            ))
            
        # Extract details produced on the current octave.
        detail = src.data[0] - octave_base
    # Return the resulting image.
    return deprocess(net, src.data[0])

@shijian.timer
def main(options):

    global program
    program = Program(options = options)

    # access options and arguments
    inputImageFilename  = options["--inputImage"]
    outputImageFilename = options["--outputImage"]
    recursiveZoom       = bool(options["--recursiveZoom"])
    GPU_mode            = bool(options["--gpu"])

    log.info("")

    if GPU_mode is True:
        log.info("engage GPU mode")
        caffe.set_mode_gpu()
        # If multiple devices exist, select GPU.
        caffe.set_device(0)
    else:
        log.info("engage CPU mode")

    # Load GoogLeNet model trained on ImageNet dataset.
    log.info("load model")
    username = os.getenv("USER")
    model_path = "/home/{username}/caffe/models/bvlc_googlenet/".format(
        username = username
    )
    net_fn     = model_path + "deploy.prototxt"
    param_fn   = model_path + "bvlc_googlenet.caffemodel"

    # Patch the model to enable computation of gradients.
    model = caffe.io.caffe_pb2.NetParameter()
    text_format.Merge(open(net_fn).read(), model)
    model.force_backward = True
    open("tmp.prototxt", "w").write(str(model))

    net = caffe.Classifier(
        "tmp.prototxt",
        param_fn,
        mean = np.float32([104.0, 116.0, 122.0]),
        channel_swap = (2,1,0)
    )

    log.info("access {filename}".format(
        filename = inputImageFilename,
    ))
    inputImage = np.float32(PIL.Image.open(inputImageFilename))

    log.info("generate")
    
    if recursiveZoom is not True:
        outputImage = deepdream(net, inputImage, end = "inception_4c/output")
        outputImage = np.uint8(outputImage)
        log.info("save {filename}".format(
            filename = outputImageFilename,
        ))
        PIL.Image.fromarray(outputImage, "RGB").save(outputImageFilename, "PNG")
    else:
        os.makedirs("frames")
        frame = inputImage
        frame_i = 0

        h, w = frame.shape[:2]
        s = 0.05 # scale coefficient
        for i in xrange(100):
            frame = deepdream(net, frame, end = "inception_4c/output")
            outputFilename = "frames/{index}.jpg".format(index = frame_i)
            PIL.Image.fromarray(np.uint8(frame)).save(outputFilename)
            frame = nd.affine_transform(
                frame,
                [1-s, 1 - s, 1],
                [h*s / 2,w*s / 2, 0],
                order = 1
            )
            frame_i += 1

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
