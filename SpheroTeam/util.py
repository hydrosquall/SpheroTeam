# General Python Helper Functions
import json


def readJsonFile(filename):
    '''
        Read a JSON file into a python dict
    '''

    with open(filename) as data_file:
        data = json.load(data_file)
    return data
