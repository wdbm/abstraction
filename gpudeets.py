#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# gpudeets                                                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program acquires and displays GPU details.                              #
#                                                                              #
# copyright (C) 2017 Will Breaden Madden, wbm@protonmail.ch                    #
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
    -h, --help          display help message
    --version           display version and exit
    --interval=INT      time between each loop (s) [default: 1]
    --graphpower        power graph display
    --graphtemperature  temperature graph display
    --table             table display
"""

name    = "gpudeets"
version = "2017-06-02T0050Z"

import datetime
import docopt
import time

import datavision
import pyprel
import shijian

def main(options):

    interval          = int(options["--interval"])
    graph_power       = options["--graphpower"]
    graph_temperature = options["--graphtemperature"]
    table             = options["--table"]

    command_general     = "nvidia-smi "                      \
                              "--query-gpu="                 \
                                  "name,"                    \
                                  "temperature.gpu,"         \
                                  "power.draw,"              \
                                  "memory.used,"             \
                                  "memory.total,"            \
                                  "utilization.gpu "         \
                              "--format="                    \
                                  "csv,"                     \
                                  "noheader"

    command_power       = "nvidia-smi "                      \
                              "--query-gpu=power.draw "      \
                              "--format=csv,noheader"

    command_temperature = "nvidia-smi "                      \
                              "--query-gpu=temperature.gpu " \
                              "--format=csv,noheader"

    measurements = []

    try:

        while True:

            if not graph_power and not graph_temperature:

                timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")
                result    = shijian.engage_command(command = command_general)
                data      = [datum.strip() for datum in result.split(",")]

                temperature  = str(data[1] + " °C")
                power_draw   = str(data[2])
                utilization  = str(data[3])
                memory_used  = str(data[4])
                memory_total = str(data[5])

                if table:

                    print(pyprel.Table(
                    contents = [[
                                   timestamp,
                                   temperature,
                                   utilization,
                                   memory_used,
                                   memory_total,
                                   power_draw
                               ]]
                    ))

                else:

                    temperature  = temperature.rjust(5)
                    power_draw   = power_draw.rjust(8)
                    utilization  = utilization.rjust(8)
                    memory_used  = memory_used.rjust(8)
                    memory_total = memory_total.rjust(5)

                    print(
                        "|{timestamp}|{temperature}|{power_draw}"\
                        "|{utilization}|{memory_used}|{memory_total}|".format(
                        timestamp    = timestamp,
                        temperature  = temperature,
                        power_draw   = power_draw,
                        utilization  = utilization,
                        memory_used  = memory_used,
                        memory_total = memory_total
                    ))

                time.sleep(interval)

            elif graph_power or graph_temperature:

                if graph_power:
                    result = shijian.engage_command(command = command_power)
                    result = result.strip().strip(" W")
                elif graph_temperature:
                    result = shijian.engage_command(command = command_temperature)
                measurements.append(float(result.strip()))
                measurements = measurements[-20:]

                y = measurements
                x = range(0, len(y))
                plot = datavision.TTYFigure()
                tmp = plot.plot(x, y, marker = "_o")
                print(tmp)

                time.sleep(interval)
                print(chr(27) + "[2J")

    except KeyboardInterrupt:

        print("")

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
