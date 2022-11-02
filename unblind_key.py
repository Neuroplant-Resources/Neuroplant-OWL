import pandas as pd
import numpy as np
import pathlib as plb
from os import path

wells = ['A', 'B', 'C', 'D']



def dict_key(bkey_fpath):
    bkey = pd.read_csv(bkey_fpath)
    comp_dict = dict(zip(bkey['Compound blind'], bkey['Compound']))
    strain_dict = dict(zip(bkey['Strain blind'], bkey['Strain']))
    return comp_dict, strain_dict
    

def solve_metadata(di, mdat, v):

    wells = ['A', 'B', 'C', 'D']

    if v == 'Strain name':
        x = 'Strain Well '
        ubx = 'UB Strain Well '
    elif v == 'Test compound':
        x = 'Compound Well '
        ubx = 'UB Compound Well '
    
    for index, row in mdat.iterrows():
        for w in wells:
            blind_header = x + w
            ub_header = ubx + w
            blinded = row[blind_header]
            mdat.loc[index, ub_header] = di[blinded]
    return mdat

def unblind(values):
    b = pd.read_csv(values['_to_unblind_'])
    results_folder = plb.Path(values['-results_folder-'])
    bkey = pd.read_csv(values['key_file'])
    bkey_dict = dict(zip(bkey['Blind'], bkey['Actual']))
    condition = values['_conditions_']

    if values['_data_2UB_'] == 'Metadata sheet':
        md = solve_metadata(bkey_dict, b, condition)
        md.to_csv(results_folder.joinpath(values['-metadata_name-'] + '.csv')) 
    elif values['_data_2UB_'] == 'Image analysis summary':
        print('Ooops')
 
 
 ##############batch results file######################################
 
def solve_compound_names_batchres(filename1, filename2, resultfolder, title):
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


