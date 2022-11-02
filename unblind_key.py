import pandas as pd
import numpy as np
import pathlib as plb




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
    b = pd.read_csv(values['_to_unblind_'], index_col=0)
    results_folder = plb.Path(values['-results_folder-'])
    bkey = pd.read_csv(values['key_file'])
    bkey_dict = dict(zip(bkey['Blind'], bkey['Actual']))
    condition = values['_conditions_']

    if values['_data_2UB_'] == 'Metadata sheet':
        md = solve_metadata(bkey_dict, b, condition)
        md.to_csv(results_folder.joinpath(values['-metadata_name-'] + '.csv')) 
    elif values['_data_2UB_'] == 'Image analysis summary':
        if condition == 'Strain name':
            b['UB_Strain'] =  [bkey_dict[x] for x in b['Strain']]
        elif condition == 'Test compound':
            b['UB_Compound'] =  [bkey_dict[x] for x in b['Compound']]
        b.to_csv(results_folder.joinpath(values['-metadata_name-'] + '.csv'))


 

