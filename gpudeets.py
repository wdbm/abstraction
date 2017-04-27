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
    -h, --help      display help message
    --version       display version and exit
    --interval=INT  time between each loop (s) [default: 1]
    --table         table display
"""

name    = "gpudeets"
version = "2017-04-27T2058Z"

import datetime
import docopt
import time

import pyprel
import shijian

def main(options):

    interval = int(options["--interval"])
    table    = options["--table"]

    command = "nvidia-smi "              \
                  "--query-gpu="         \
                      "name,"            \
                      "temperature.gpu," \
                      "utilization.gpu," \
                      "memory.used,"     \
                      "memory.total,"    \
                      "pstate "          \
                  "--format="            \
                      "csv,"             \
                      "noheader"

    try:

        while True:

            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")
            result    = shijian.engage_command(command = command)
            data      = [datum.strip() for datum in result.split(",")]

            if table:

                temperature       = str(data[1] + " °C")
                utilization       = str(data[2])
                memory_used       = str(data[3])
                memory_total      = str(data[4])
                performance_state = str(data[5])

                print(pyprel.Table(
                contents = [[
                               timestamp,
                               temperature,
                               utilization,
                               memory_used,
                               memory_total,
                               performance_state
                           ]]
                ))

            else:

                temperature       = str(data[1] + " °C").rjust(7)
                utilization       = str(data[2]).rjust(5)
                memory_used       = str(data[3]).rjust(8)
                memory_total      = str(data[4]).rjust(8)
                performance_state = str(data[5]).rjust(2)

                print(
                    "|{timestamp}|{temperature}|{utilization}|{memory_used}|"\
                    "{memory_total}|{performance_state}|".format(
                    timestamp         = timestamp,
                    temperature       = temperature,
                    utilization       = utilization,
                    memory_used       = memory_used,
                    memory_total      = memory_total,
                    performance_state = performance_state
                ))

            time.sleep(interval)

    except KeyboardInterrupt:

        print("")

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
