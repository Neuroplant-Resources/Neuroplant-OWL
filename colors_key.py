import pandas as pd
import numpy as np
import pathlib as plb
from os import path


def dict_color_key(filename):
    dict = {}
    file = pd.read_csv(filename)
    for index, row in file.iterrows():
        name = row['Variable Name:']
        if isinstance(name, int):
            dict[name] = row['Variable Color:']
        else:
            dict[name.lower()] = row['Variable Color:']
    return dict
    


def dict_color_key_mutli2(filename):
    dict = {}
    file = pd.read_csv(filename)
    for index, row in file.iterrows():
        dict[row['Variable Name:']] = row['Variable Color:']
    return dict

