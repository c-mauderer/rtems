#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser(
    description=(
        "Simple Doxygen filter for RTEMS to rename groups in HALs.\n"
    ))

parser.add_argument(
    "input",
    help="Input file to filter",
    type=argparse.FileType('r')
)

args = parser.parse_args()

class filter:
    def __init__(self, regex_string, prefix):
        self.regex = re.compile(regex_string)
        self.prefix = prefix

FILTERS = (
    filter(r"/bsps/arm/stm32h7/hal/.*$", "RTEMSBSPsARMSTM32H7HAL"),
    filter(r"/bsps/arm/stm32h7/include/stm32h7.*$", "RTEMSBSPsARMSTM32H7HAL"),
    filter(r"/bsps/arm/stm32u5/hal/.*$", "RTEMSBSPsARMSTM32U5HAL"),
    filter(r"/bsps/arm/stm32u5/include/stm32u5.*$", "RTEMSBSPsARMSTM32U5HAL"),
    filter(r"/bsps/arm/imxrt/mcux-sdk/.*$", "RTEMSBSPsARMIMXRTMCUXSDK"),
    )

for f in FILTERS:
    if f.regex.search(args.input.name) is not None:
        for line in args.input:
            line = re.sub(r"([@\\]defgroup\s+)(\w+)", f"\\1{f.prefix}\\2", line)
            # FIXME: ingroup can have multiple groups!
            line = re.sub(r"([@\\]ingroup\s+)(\w+)", f"\\1{f.prefix}\\2", line)
            line = re.sub(r"([@\\]addtogroup\s+)(\w+)", f"\\1{f.prefix}\\2", line)
            print(line, end="")
        sys.exit(0)

for line in args.input:
    print(line, end="")
