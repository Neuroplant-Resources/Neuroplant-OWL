import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib as plb
import seaborn as sns
from scipy import stats
import statistics

screen_metadata = metadata_path

ia_data = image_analysis_summary_results

for index, row in ia_data.iterrows():
    ia_data['Slot']= ia_data['WellNo'].astype(str).str[0]
    ia_data['Well']= ia_data['WellNo'].astype(str).str[1]

def add_pid(row, image_metdat):
    pid = image_metdat.loc[(image_metdat['Image ID']==row['File Name']) 
                           & (image_metdat['Scanner Slot:'].astype(str)==row['Slot'])]['Plate ID']
    return pid.values[0]

ia_data['Plate ID']=ia_data.apply(
    lambda row: add_pid(row, screen_metadata), axis=1)

def f(x):
    return {
        'A': 'Compound A',
        'B': 'Compound B',
        'C': 'Compound C',
        'D': 'Compound D',
    }[x]

def add_compound(row, image_metdat):
    well=row['Well']
    dat = image_metdat.loc[image_metdat['Plate ID']==row['Plate ID']][f(well)]
    return dat.values[0]

ia_data['Compound']=ia_data.apply(
    lambda row: add_compound(row, screen_metadata), axis=1)

ia_data.to_csv('results_path')

def main():
	make_GUI()

if __name__ == '__main__':
    main()