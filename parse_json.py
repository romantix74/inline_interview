#!/usr/bin/env python

import json

input_json_file = "./input/eltexClass.json"
input_json = ""


def parsejson():

    with open(input_json_file) as f:
        input_json = f.read()
        
    data = json.loads(input_json)
    print(data["metric"])


if __name__ == '__main__':

    parsejson()