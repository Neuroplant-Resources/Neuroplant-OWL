import pandas as pd
import numpy as np
import pathlib as plb
from os import path


def dict_key_compound(filename):
    dic = {}
    file = pd.read_csv(filename)
    for index, row in file.iterrows():
        dic[(row['Compound Blinded Name:'])] = (row['Compound Actual Name:'])
        # add .trim()
    return dic
    
def dict_key_strain(filename):
    dic = {}
    file = pd.read_csv(filename)
    for index, row in file.iterrows():
        dic[(row['Strain Blinded Name:'])] = (row['Strain Actual Name:'])
        # add .trim()
    return dic
    
    
def unblind(char1, char2, di, data, input_text):
    if str(char1) in di.keys():
        data[input_text + char2] = data[input_text + char2].replace([char1],di[char1])


def solve_compound_names(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    di = dict_key_compound(filename2)
    for index, row in data.iterrows():
        unblind((row['Compound Well A']), 'A', di, data, 'Compound Well ')
        unblind((row['Compound Well B']), 'B', di, data, 'Compound Well ')
        unblind((row['Compound Well C']), 'C', di, data, 'Compound Well ')
        unblind((row['Compound Well D']), 'D', di, data, 'Compound Well ')
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))


def solve_strain_names(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    di = dict_key_strain(filename2)
    for index, row in data.iterrows():
        unblind(row['Strain Well A'], 'A', di, data, 'Strain Well ')
        unblind(row['Strain Well B'], 'B', di, data, 'Strain Well ')
        unblind(row['Strain Well C'], 'C', di, data, 'Strain Well ')
        unblind(row['Strain Well D'], 'D', di, data, 'Strain Well ')
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))

def solve_both_strain_and_compound_names(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    di_c = dict_key_compound(filename2)
    di_s = dict_key_strain(filename2)
    for index, row in data.iterrows():
        unblind(row['Compound Well A'], 'A', di_c, data, 'Compound Well ')
        unblind(row['Compound Well B'], 'B', di_c, data, 'Compound Well ')
        unblind(row['Compound Well C'], 'C', di_c, data, 'Compound Well ')
        unblind(row['Compound Well D'], 'D', di_c, data, 'Compound Well ')
        unblind(row['Strain Well A'], 'A', di_s, data, 'Strain Well ')
        unblind(row['Strain Well B'], 'B', di_s, data, 'Strain Well ')
        unblind(row['Strain Well C'], 'C', di_s, data, 'Strain Well ')
        unblind(row['Strain Well D'], 'D', di_s, data, 'Strain Well ')
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))
 
 
 
 
 
 
 ##############batch results file######################################
 
def solve_compound_names_batchres(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    di = dict_key_compound(filename2)
    for index, row in data.iterrows():
        one = row['Compound']
        if one in di.keys():
            data['Compound'] = data['Compound'].replace([one], di[one])
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))


def solve_strain_names_batchres(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    di = dict_key_strain(filename2)
    for index, row in data.iterrows():
        one = row['Strain']
        if one in di.keys():
            data['Strain'] = data['Strain'].replace([one], di[one])
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))

def solve_both_strain_and_compound_names_batchres(filename1, filename2, resultfolder, title):
    results_folder = plb.Path(resultfolder)
    data = pd.read_csv(filename1)
    di_c = dict_key_compound(filename2)
    di_s = dict_key_strain(filename2)
    for index, row in data.iterrows():
        one = row['Compound']
        one = row['Strain']
        if one in di_c.keys():
            data['Compound'] = data['Compound'].replace([one], di[one])
        if one in di_s.keys():
            data['Strain'] = data['Strain'].replace([one], di[one])
    data.to_csv(path_or_buf= results_folder.joinpath(title +'.csv'))
    
    

#if __name__ == '__main__':
#    solve_compound_names('test-metadata.csv', 'test-key.csv')
#    copy_of_original_input_metadata('test-metadata.csv')
#    data.to_csv(path_or_buf= results_folder.joinpath('copy.csv'))


