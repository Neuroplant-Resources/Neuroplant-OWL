import pandas as pd
import pathlib as plb



def add_PlateID(row, metadata):
    slotID = row['WellNo'][0]
    slotID = int(slotID)


    pid = metadata.loc[
        (metadata['Image ID']==row['File Name']) & 
        (metadata['Scanner Slot:']==slotID)].get('Plate ID', default = "Plate ID column not matched")

    if len(pid) == 0:
        return 'No data'
        pass
    else:
        return pid.values[0]

    


def add_Compound(row, metadata):
    wellID = row['WellNo'][1]
    well_val = 'Compound Well ' + wellID 

    compound = metadata.loc[metadata['Plate ID']==row['Plate ID']].get(well_val, default = "Compound column not matched")
 
    if len(compound) == 0:
        return 'No data'
        pass
    elif isinstance(compound, str):
        return compound
    else:
        return compound.values[0]


def add_Strain(row, metadata):
    wellID = row['WellNo'][1]
    well_val = 'Strain Well ' + wellID 

    strain = metadata.loc[metadata['Plate ID']==row['Plate ID']].get(well_val, default = "Strain column not matched")


    if len(strain) == 0:
        return 'No data'
        pass
    elif isinstance(strain, str):
        return strain
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

