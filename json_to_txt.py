#!/bin/python3

"""Convert json to txt """

import sys
import json

FILE = sys.argv[1]

with open(f"{FILE}.json", "r") as analysis_parameters:
    data = json.load(analysis_parameters)

with open(f"{FILE}.txt", "w") as analysis_parameters:
    for line in data.values():
        analysis_parameters.write(str(line) + '\n')
