import pandas as pd
import numpy as np
import pathlib as plb
from os import path
import dabest as db
import matplotlib.pyplot as plt

def getting_location_collumns_compound(row, folder_of_loc_files, dict):
    name_c = row['Compound']
    compound_name = name_c.lower()
    file_name = row['File Name']
    well_name = row['WellNo']
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    location = folder_of_loc_files.joinpath(loc_file)
        
    if location.is_file():
        location_file = pd.read_csv(location)
        x_pos = location_file['X']
        x_pos_list = x_pos.tolist()
        
        if compound_name not in dict:
            dict[compound_name] = x_pos_list
            
        else:
            dict[compound_name].extend(x_pos_list)
            
    else:
        pass
        
    

def do_data_visualisation_compound(filename, location_filesfolder, control_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    control = control_name.lower()
    list = []
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
        

    
    
def getting_location_collumns_strain(row, folder_of_loc_files, dict):
    name_s = row['Strain']
    strain_name = name_s.lower()
    file_name = row['File Name']
    well_name = row['WellNo']
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    location = folder_of_loc_files.joinpath(loc_file)
        
    if location.is_file():
        location_file = pd.read_csv(location)
        x_pos = location_file['X']
        x_pos_list = x_pos.tolist()
        
        if strain_name not in dict:
            dict[strain_name] = x_pos_list
            
        else:
            dict[strain_name].extend(x_pos_list)
            
    else:
        pass
        
    

def do_data_visualisation_strain(filename, location_filesfolder, control_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    control = control_name.lower()
    list = []
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)

    
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    
def getting_location_collumns_timelapse(row, folder_of_loc_files, dict):
    time = str(row['Time Points'])
    file_name = row['File Name']
    well_name = row['WellNo']
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    location = folder_of_loc_files.joinpath(loc_file)
        
    if location.is_file():
        location_file = pd.read_csv(location)
        x_pos = location_file['X']
        x_pos_list = x_pos.tolist()
        
        if time not in dict:
            dict[time] = x_pos_list
            
        else:
            dict[time].extend(x_pos_list)
            
    else:
        pass
        
    

def do_data_visualisation_timelapse(filename, location_filesfolder, control_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_timelapse(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    control = str(control_name)
    list = []
    for key in dict.keys():
        if key != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    

        
    ############################################shared control color#############################################
    
def do_data_visualisation_compound_color(filename, location_filesfolder, control_name, color_key):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    control = control_name.lower()
    list = []
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(custom_palette=color_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    
    
    
def do_data_visualisation_strain_color(filename, location_filesfolder, control_name, color_key):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    control = control_name.lower()
    list = []
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)

    
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(custom_palette=color_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    
    
def do_data_visualisation_timelapse_color(filename, location_filesfolder, control_name, color_key):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_timelapse(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    control = str(control_name)
    list = []
    for key in dict.keys():
        if key != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(custom_palette=color_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
     ######################unpaired two group estimation plot##############################
     
def do_data_visualisation_compound_2_group(filename, location_filesfolder, control_name, test_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    control = control_name.lower()
    test = test_name.lower()
    
    new_object = db.load(data_frame, idx= (control, test))
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    
    
def do_data_visualisation_strain_2_group(filename, location_filesfolder, control_name, test_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    control = control_name.lower()
    test = test_name.lower()
    
    new_object = db.load(data_frame, idx= (control, test))
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Mean differene (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
        
        
    ##################Multi Two Group Estimation Plot ##################################

        
def do_data_visualisation_compound_multi2_group(filename, location_filesfolder, c1, t1, c2, t2, c3, t3, c4, t4):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    c1 = c1.lower()
    t1 = t1.lower()
    c2 = c2.lower()
    t2 = t2.lower()
    c3 = c3.lower()
    t3 = t3.lower()
    c4 = c4.lower()
    t4 = t4.lower()
    list = []
    
    if c1 != 'control1' and t1 != 'test1':
        tuple1 = (c1, t1)
        list.append(tuple1)
    if c2 != 'control2' and t2 != 'test2':
        tuple2 = (c2, t2)
        list.append(tuple2)
    if c3 != 'control3' and t3 != 'test3':
        tuple3 = (c3, t3)
        list.append(tuple3)
    if c4 != 'control4' and t4 != 'test4':
        tuple4 = (c4, t4)
        list.append(tuple4)
    
    last_tuple = tuple(list)

    
    new_object = db.load(data_frame, idx= last_tuple)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    

def do_data_visualisation_strain_multi2_group(filename, location_filesfolder, c1, t1, c2, t2, c3, t3, c4, t4):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict)
    
    df = pd.DataFrame.from_dict(dict, orient='index')
    data_fr = df.transpose()
    px_mm = 1200 / 25.4
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    c1 = c1.lower()
    t1 = t1.lower()
    c2 = c2.lower()
    t2 = t2.lower()
    c3 = c3.lower()
    t3 = t3.lower()
    c4 = c4.lower()
    t4 = t4.lower()
    list = []
    
    if c1 != 'control1' and t1 != 'test1':
        tuple1 = (c1, t1)
        list.append(tuple1)
    if c2 != 'control2' and t2 != 'test2':
        tuple2 = (c2, t2)
        list.append(tuple2)
    if c3 != 'control3' and t3 != 'test3':
        tuple3 = (c3, t3)
        list.append(tuple3)
    if c4 != 'control4' and t4 != 'test4':
        tuple4 = (c4, t4)
        list.append(tuple4)
    
    last_tuple = tuple(list)

    
    new_object = db.load(data_frame, idx= last_tuple)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    


    
        
    



