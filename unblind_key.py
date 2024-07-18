import pandas as pd
import pathlib as plb
import PySimpleGUI as sg




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
    
    missing = {}

    for index, row in mdat.iterrows():
        for w in wells:
            blind_header = x + w
            ub_header = ubx + w
            #print(ub_header)
            blinded = row[blind_header]
            ub = di.get(blinded)
            if ub != None:
                mdat.loc[index, ub_header] = ub
            else: 
                missing.update({blinded: [index, blind_header]})
    if missing:
        unmatched = ["Not matched: {}  Row: {} Column: {} ".format(key, missing[key][0], missing[key][1]) for key in missing]
        print(unmatched)        #print(str(unmatched).split(','))#.join('\n')
        s = '\n'.join([str(i) for i in unmatched])
        sg.PopupScrolled(s, title='Unmasked conditions')

               
    return mdat

def unblind(values):
    
    results_folder = plb.Path(values['-results_folder-'])
    bkey = pd.read_csv(values['key_file'])
    bkey_dict = dict(zip(bkey['Blind'], bkey['Actual']))
    condition = values['_conditions_']

    if values['_data_2UB_'] == 'Metadata sheet':
        b = pd.read_csv(values['_to_unblind_'])
        md = solve_metadata(bkey_dict, b, condition)
        md.to_csv(results_folder.joinpath(values['-metadata_name-'] + '.csv')) 
    elif values['_data_2UB_'] == 'Image analysis summary':
        b = pd.read_csv(values['_to_unblind_'], index_col=0)
        if condition == 'Strain name':
            b['UB_Strain'] =  [bkey_dict.get(x, 'Strain column not matched') for x in b['Strain']]
        elif condition == 'Test compound':
            b['UB_Compound'] =  [bkey_dict.get(x, 'Compound column not matched') for x in b['Compound']]
        b.to_csv(results_folder.joinpath(values['-metadata_name-'] + '.csv'))


 

