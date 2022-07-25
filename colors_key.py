import pandas as pd
import numpy as np
import pathlib as plb
from os import path


def dict_color_key(filename):
    dict = {}
    file = pd.read_csv(filename)
    for index, row in file.iterrows():
        dict[(row['Variable Name:']).lower()] = row['Variable Color:']
    return dict
    




