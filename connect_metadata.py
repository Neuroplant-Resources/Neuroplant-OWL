import pandas as pd
import pathlib as plb
import PySimpleGUI as sg


def add_PlateID(row, metadata):
    slotID = row['WellNo'][0]
    slotID = int(slotID)


    pid = metadata.loc[
        (metadata['Image ID']==row['File Name']) & 
        (metadata['Scanner Slot:']==slotID)].get('Plate ID')

    if len(pid) == 0:
        pid = 'No data'
        return pid
    else:
        print(pid.values[0])
        return pid.values[0]

    


def add_Compound(row, metadata):
    wellID = row['WellNo'][1]
    well_val = 'Compound Well ' + wellID

    if well_val in metadata.columns:
        compound = metadata.loc[metadata['Plate ID']==row['Plate ID']].get(well_val, default = "Compound column not matched")
     
        if len(compound) == 0:
            return 'No data entered'
            pass
        elif isinstance(compound, str):
            return compound
        else:
            return compound.values[0]
    else:
        return "No data"


def add_Strain(row, metadata):
    wellID = row['WellNo'][1]
    well_val = 'Strain Well ' + wellID 

    if well_val in metadata.columns:
        strain = metadata.loc[metadata['Plate ID']==row['Plate ID']].get(well_val, default = "Strain column not matched")


        if len(strain) == 0:
            return 'No data'
            pass
        elif isinstance(strain, str):
            return strain
        else:
            return strain.values[0]

    else:
        return "No Data"


def get_dat(metdat, rslt):

    if 'Plate ID' in metdat.columns:
        rslt['Plate ID'] = rslt.apply(
        lambda row: add_PlateID(row, metdat), axis=1)

        rslt['Compound'] = rslt.apply(
        lambda row: add_Compound(row, metdat), axis=1)

        rslt['Strain'] = rslt.apply(
        lambda row: add_Strain(row, metdat), axis=1)

        return rslt

    else:
        sg.popup('Plate ID column header not found. Check spelling. \nMetadata not connected.')
        return rslt


def connect(md_path, results):
    md_file_path = plb.Path(md_path)
    md = pd.read_csv(md_file_path)


    cols = ['Compound Well A', 'Compound Well B', 'Compound Well C', 'Compound Well D',
    'Strain Well A', 'Strain Well B', 'Strain Well C', 'Strain Well D']

    missing = []


    for c in cols:
        if c not in list(md.columns):
            missing.append(c)
        else:
            continue


    if len(c) > 0:
        sg.popup('"'+ str(missing) + '" column header(s) do not match. \nColumn(s) will not be imported')
        imprtd = get_dat(md, results)
    else:
        imprtd = get_dat(md, results)

    return imprtd
