import pandas as pd
import numpy as np
import pathlib as plb
from os import path


def dict_timelapse_key(filename):
    dict = {}
    file = pd.read_csv(filename)
    for index, row in file.iterrows():
        dict[(row['File Name:']).lower()] = row['Time Point:']
    return dict
    

def timelapse_collumn_addition(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    dict = dict_timelapse_key(filename2)
    timepoints_list = []
    position = len(data.columns)
    for index, row in data.iterrows():
        name = row['File Name']
        time = dict[name.lower()]
        timepoints_list.append(time)
    data.insert(position, 'Time Points', timepoints_list)
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))


