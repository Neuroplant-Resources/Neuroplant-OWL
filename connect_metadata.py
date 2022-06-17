import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib as plb
import seaborn as sns
from scipy import stats
import statistics




def add_PlateID(row, metadata):
    slotID = row['WellNo'][0]
    slotID = int(slotID)


    pid = metadata.loc[
        (metadata['Image ID']==row['File Name']) & 
        (metadata['Scanner Slot:']==slotID)]['Plate ID']

    if len(pid) == 0:
        return 'No data'
        pass
    else:
        return pid.values[0]

    


def add_Compound(row, metadata):
    wellID = row['WellNo'][1]

    if wellID == 'A':
        compound = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Compound Well A']
    elif wellID == 'B':
        compound = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Compound Well B']
    elif wellID == 'C':
        compound = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Compound Well C']
    elif wellID == 'D':
        compound = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Compound Well D']
    #print(compound)

    if len(compound) == 0:
        return 'No data'
        pass
    else:
        return compound.values[0]


def add_Strain(row, metadata):
    wellID = row['WellNo'][1]
    if wellID == 'A':
        strain = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Strain Well A']
    elif wellID == 'B':
        strain = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Strain Well B']
    elif wellID == 'C':
        strain = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Strain Well C']
    elif wellID == 'D':
        strain = metadata.loc[metadata['Plate ID']==row['Plate ID']]['Strain Well D']

    if len(strain) == 0:
        return 'No data'
        pass
    else:
        return strain.values[0]    



def connect(md_path, results):

    md_file_path = plb.Path(md_path)
    md = pd.read_csv(md_file_path)

    results['Plate ID'] = results.apply(
    lambda row: add_PlateID(row, md), axis=1)

    results['Compound'] = results.apply(
    lambda row: add_Compound(row, md), axis=1)

    results['Strain'] = results.apply(
    lambda row: add_Strain(row, md), axis=1)

    return results

