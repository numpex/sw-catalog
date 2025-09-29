#!/usr/bin/python

import urllib.request
import json
import os, tempfile
from pathlib import Path
import filecmp
from jsonschema import validate

if not os.path.exists("softwares"):
    os.makedirs("softwares")

# the list of fields to extract from the codemeta.json
fields = ['description', 'name', 'documentation', 'packages']

with open("software.txt", "r") as swfile:
    for line in swfile:
        xline = line.strip()
        # Get the codemeta.json for the software
        urllib.request.urlretrieve(xline, "codemeta.json")

        # generate the json description
        with open("codemeta.json", "r") as jsonfile:
            data = json.load(jsonfile)
            swname = data['name']
            fd, path = tempfile.mkstemp()
            with os.fdopen(fd, 'w') as tmp:
                tmp.write("\t{\n")
                for f in fields:
                    tmp.write("\t\t\"{}\": \"{}\",\n".format(f, data[f]))
                tmp.write("\t}\n")

        # compare to the existing one
        swpath = "softwares/" + swname + ".json"
        if (Path(swpath).exists()):
            print("Description for software '{}' exists.".format(swname))
            if filecmp.cmp(swpath, path):
                print("And it has not changed. No need to update it.")
                os.unlink(path)
            else:
                print("And it has changed. Needs to be updated".format(swname))
                os.rename(path, swpath)
        else:
            print("Description for software '{}' DOES NOT exist. Create it.".format(swname))
            os.rename(path, swpath)

        # delete codemeta json file
        os.unlink("codemeta.json")

