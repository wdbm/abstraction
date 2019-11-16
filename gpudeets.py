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
    -h, --help               display help message
    --version                display version and exit

    --graphpower             power graph display
    --graphtemperature       temperature graph display
    --table                  table display

    --CSV_logging=BOOL       log to CSV file            [default: false]
    --filepath_CSV=FILEPATH  filepath for CSV logging   [default: gpudeets.csv]

    --interval=INT           time between each loop (s) [default: 10]
"""

import datetime
import docopt
import logging
import os
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import datavision
import pandas as pd
import pyprel
import subprocess
import technicolor

name    = "gpudeets"
version = "2018-02-24T1606Z"

log = logging.getLogger(name)
log.addHandler(technicolor.ColorisingStreamHandler())
log.setLevel(logging.INFO)

def main(options):

    graph_power       =     options["--graphpower"]
    graph_temperature =     options["--graphtemperature"]
    table             =     options["--table"]
    CSV_logging       =     options["--CSV_logging"].lower() == "true"
    filepath_CSV      =     options["--filepath_CSV"]
    interval          = int(options["--interval"])

    if CSV_logging: log.info("logging to CSV " + filepath_CSV)

    command_general     = "nvidia-smi "                     \
                              "--query-gpu="                \
                                  "name,"                   \
                                  "temperature.gpu,"        \
                                  "power.draw,"             \
                                  "memory.used,"            \
                                  "memory.total,"           \
                                  "utilization.gpu "        \
                              "--format="                   \
                                  "csv,"                    \
                                  "noheader"

    command_power       = "nvidia-smi "                     \
                              "--query-gpu=power.draw "     \
                              "--format=csv,noheader"

    command_temperature = "nvidia-smi "                     \
                              "--query-gpu=temperature.gpu "\
                              "--format=csv,noheader"

    measurements = []
    try:
        while True:
            if not graph_power and not graph_temperature:
                timestamp          = datetime.datetime.utcnow()
                timestamp_string   = timestamp.strftime("%Y-%m-%dT%H%M%SZ")
                result             = subprocess.check_output(command_general.split(' ')).decode('utf-8')
                data               = [datum.strip() for datum in result.split(",")]
                temperature        = str(data[1])
                temperature_string = temperature + " °C"
                power_draw         = str(data[2])
                utilization        = str(data[3])
                memory_used        = str(data[4])
                memory_total       = str(data[5])
                if table:
                    print(pyprel.Table(
                    contents = [[
                                   timestamp_string,
                                   temperature_string,
                                   utilization,
                                   memory_used,
                                   memory_total,
                                   power_draw
                               ]]
                    ))
                if CSV_logging:
                    df = pd.DataFrame(columns = [
                        "datetime",
                        "temperature_C",
                        "power_draw_W",
                        "utilization_MiB",
                        "memory_used_MiB",
                        "memory_total_percentage"
                    ])
                    df = df.append(
                        {
                            "datetime"               : timestamp,
                            "temperature_C"          : temperature,
                            "power_draw_W"           : power_draw[:-2],
                            "utilization_MiB"        : utilization[:-4],
                            "memory_used_MiB"        : memory_used[:-4],
                            "memory_total_percentage": memory_total[:-2]
                        },
                        ignore_index=True
                    )
                    log.info(timestamp_string + " log to CSV " + filepath_CSV)
                    df.to_csv(filepath_CSV, header=not os.path.isfile(filepath_CSV), index=False, mode="a")
                else:
                    temperature_string = temperature_string.rjust(5)
                    power_draw         = power_draw.rjust(8)
                    utilization        = utilization.rjust(8)
                    memory_used        = memory_used.rjust(8)
                    memory_total       = memory_total.rjust(5)
                    print(
                        "|{timestamp_string}|{temperature_string}|{power_draw}"\
                        "|{utilization}|{memory_used}|{memory_total}|".format(
                        timestamp_string   = timestamp_string,
                        temperature_string = temperature_string,
                        power_draw         = power_draw,
                        utilization        = utilization,
                        memory_used        = memory_used,
                        memory_total       = memory_total
                    ))
                time.sleep(interval)
            elif graph_power or graph_temperature:
                if graph_power:
                    result = subprocess.check_output(command_power.split(' ')).decode('utf-8')
                    result = result.strip().strip(" W")
                elif graph_temperature:
                    result = subprocess.check_output(command_temperature.split(' ')).decode('utf-8')
                measurements.append(float(result.strip()))
                measurements = measurements[-20:]
                y = measurements
                x = range(0, len(y))
                plot = datavision.TTYFigure()
                tmp = plot.plot(x, y, marker="_o")
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
