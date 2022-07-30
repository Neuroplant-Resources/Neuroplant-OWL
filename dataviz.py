import pandas as pd
import numpy as np
import pathlib as plb
from os import path
import dabest as db
import matplotlib.pyplot as plt
import seaborn as sns

def getting_location_collumns_compound(row, folder_of_loc_files, dict):
    name_c = row['Compound']
    compound_name = name_c.lower()
    file_name = row['File Name']
    well_name = row['WellNo']
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    location = folder_of_loc_files.joinpath(loc_file)
    if row['Passes QC'] == 'Y':
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
    
    if row['Passes QC'] == 'Y':
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
    previous = 0
    for key in dict.keys():
        key2 = turn_to_number(key)
        if key != control:
            if int(previous) < int(key2):
                list.append(key)
            else:
                for i in range(len(list)):
                    num = turn_to_number(list[i])
                    if int(key2) < int(num):
                        list.insert(i, key)
                        break
                        
        if len(list) != 0:
            number = turn_to_number(list[(len(list)-1)])
            previous = number


    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)

    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
def turn_to_number(string):
    s2 = ''
    for char in string:
        if char.isdigit():
            s2 += char
        if not char.isdigit() and len(s2) != 0:
            return s2
    return s2
    
    
        
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
    previous = 0
    for key in dict.keys():
        key2 = turn_to_number(key)
        if key != control:
            if int(previous) < int(key2):
                list.append(key)
            else:
                for i in range(len(list)):
                    num = turn_to_number(list[i])
                    if int(key2) < int(num):
                        list.insert(i, key)
                        break
                        
        if len(list) != 0:
            number = turn_to_number(list[(len(list)-1)])
            previous = number


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

        
#def do_data_visualisation_compound_multi2_group(filename, location_filesfolder, c1, t1, c2, t2, c3, t3, c4, t4):
#    dict = {}
#    batch_res = pd.read_csv(filename)
#    folder_of_loc_files = plb.Path(location_filesfolder)
#
#    for index, row in batch_res.iterrows():
#        getting_location_collumns_compound(row, folder_of_loc_files, dict)
#
#    df = pd.DataFrame.from_dict(dict, orient='index')
#    data_fr = df.transpose()
#    px_mm = 1200 / 25.4
#    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
#
#    c1 = c1.lower()
#    t1 = t1.lower()
#    c2 = c2.lower()
#    t2 = t2.lower()
#    c3 = c3.lower()
#    t3 = t3.lower()
#    c4 = c4.lower()
#    t4 = t4.lower()
#    list = []
#
#    if c1 != 'control1' and t1 != 'test1':
#        tuple1 = (c1, t1)
#        list.append(tuple1)
#    if c2 != 'control2' and t2 != 'test2':
#        tuple2 = (c2, t2)
#        list.append(tuple2)
#    if c3 != 'control3' and t3 != 'test3':
#        tuple3 = (c3, t3)
#        list.append(tuple3)
#    if c4 != 'control4' and t4 != 'test4':
#        tuple4 = (c4, t4)
#        list.append(tuple4)
#
#    last_tuple = tuple(list)
#
#
#    new_object = db.load(data_frame, idx= last_tuple)
#    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#    plt.show()
#
#
#def do_data_visualisation_strain_multi2_group(filename, location_filesfolder, c1, t1, c2, t2, c3, t3, c4, t4):
#    dict = {}
#    batch_res = pd.read_csv(filename)
#    folder_of_loc_files = plb.Path(location_filesfolder)
#
#    for index, row in batch_res.iterrows():
#        getting_location_collumns_strain(row, folder_of_loc_files, dict)
#
#    df = pd.DataFrame.from_dict(dict, orient='index')
#    data_fr = df.transpose()
#    px_mm = 1200 / 25.4
#    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
#
#    c1 = c1.lower()
#    t1 = t1.lower()
#    c2 = c2.lower()
#    t2 = t2.lower()
#    c3 = c3.lower()
#    t3 = t3.lower()
#    c4 = c4.lower()
#    t4 = t4.lower()
#    list = []
#
#    if c1 != 'control1' and t1 != 'test1':
#        tuple1 = (c1, t1)
#        list.append(tuple1)
#    if c2 != 'control2' and t2 != 'test2':
#        tuple2 = (c2, t2)
#        list.append(tuple2)
#    if c3 != 'control3' and t3 != 'test3':
#        tuple3 = (c3, t3)
#        list.append(tuple3)
#    if c4 != 'control4' and t4 != 'test4':
#        tuple4 = (c4, t4)
#        list.append(tuple4)
#
#    last_tuple = tuple(list)
#
#
#    new_object = db.load(data_frame, idx= last_tuple)
#    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#    plt.show()




def multi2group_dataviz_1(filename, location_filesfolder, strain_control, compound_1, compound_2):
    
    file = pd.read_csv(filename)
    folder = plb.Path(location_filesfolder)
    dict_1 = {}
    dict_2 = {}
    control_variable_1 = compound_1 + '_' + strain_control
    control_variable_2 = compound_2 + '_' + strain_control
    strains_list = [strain_control]
    multi2_list = [(control_variable_1, control_variable_2)]

    for index, row in file.iterrows():
        file_name = row['File Name']
        well = row['WellNo']
        location_file_name = 'loc_' + file_name + '_' + well + '.csv'
        locationfile = folder.joinpath(location_file_name)
        strain = row['Strain']
        compound = row['Compound']


        
    
        if locationfile.is_file():
            
            if compound == compound_1:
                name = compound + '_' + strain
                locations = pd.read_csv(locationfile)
                location_values = locations['X']
                location_x_list = location_values.tolist()

                if name not in dict_1:
                    dict_1[name] = location_x_list
                else:
                    dict_1[name].extend(location_x_list)
                    
            elif compound == compound_2:
                name = compound + '_' + strain
                locations = pd.read_csv(locationfile)
                location_values = locations['X']
                location_x_list = location_values.tolist()

                
                if name not in dict_2:
                    dict_2[name] = location_x_list
                else:
                    dict_2[name].extend(location_x_list)
                    
            if strain not in strains_list:
                name_1 = compound_1 + '_' + strain
                name_2 = compound_2 + '_' + strain
                multi2_list.append((name_1, name_2))
            strains_list.append(strain)
        else:
            pass
        
                
                    

    df1 = pd.DataFrame.from_dict(dict_1, orient='index')
    data_fr1 = df1.transpose()
    px_mm = 1200 / 25.4
    data_frame_1 = data_fr1.apply(lambda x: -(x/px_mm)+32.5)

    df2 = pd.DataFrame.from_dict(dict_2, orient='index')
    data_fr2 = df2.transpose()
    px_mm = 1200 / 25.4
    data_frame_2 = data_fr2.apply(lambda x: -(x/px_mm)+32.5)
    
    total_df = pd.concat([data_frame_1, data_frame_2], axis = 1)


    list_1 = []
    list_2 = []


    for key_1 in dict_1.keys():
        if key_1 != control_variable_1:
            list_1.append(key_1)
    new_list_1 = [control_variable_1]
    new_list_1.extend(list_1)
    lili_1 = tuple(new_list_1)

    for key_2 in dict_2.keys():
        if key_2 != control_variable_2:
            list_2.append(key_2)
    new_list_2 = [control_variable_2]
    new_list_2.extend(list_2)
    lili_2 = tuple(new_list_2)


    first = db.load(total_df, idx= lili_1)
    second = db.load(total_df, idx= lili_2)
    first.mean_diff
    second.mean_diff

    

    tuple_for_multi2 = tuple(multi2_list)
    new_object = db.load(total_df, idx= tuple_for_multi2)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
    figure, axes = plt.subplots(nrows =1, ncols=2, figsize=(48, 8))
    first.mean_diff.plot(ax=axes[0], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    second.mean_diff.plot(ax=axes[1], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    
def multi2group_dataviz_2(filename, location_filesfolder, compound_control, strain_1, strain_2):
    
    file = pd.read_csv(filename, encoding= 'unicode_escape')
    folder = plb.Path(location_filesfolder)
    dict_1 = {}
    dict_2 = {}
    control_variable_1 = strain_1 + '_' + compound_control
    control_variable_2 = strain_2 + '_' + compound_control
    compounds_list = [compound_control]
    multi2_list = [(control_variable_1, control_variable_2)]

    for index, row in file.iterrows():
        file_name = row['File Name']
        well = row['WellNo']
        location_file_name = 'loc_' + file_name + '_' + well + '.csv'
        locationfile = folder.joinpath(location_file_name)
        strain = row['Strain']
        compound = row['Compound']


        
    
        if locationfile.is_file():
            
            if strain == strain_1:
                name = strain + '_' + compound
                locations = pd.read_csv(locationfile)
                location_values = locations['X']
                location_x_list = location_values.tolist()

                if name not in dict_1:
                    dict_1[name] = location_x_list
                else:
                    dict_1[name].extend(location_x_list)
                    
            elif strain == strain_2:
                name = strain + '_' + compound
                locations = pd.read_csv(locationfile)
                location_values = locations['X']
                location_x_list = location_values.tolist()

                
                if name not in dict_2:
                    dict_2[name] = location_x_list
                else:
                    dict_2[name].extend(location_x_list)
                    
            if compound not in compounds_list:
                name_1 = strain_1 + '_' + compound
                name_2 = strain_2 + '_' + compound
                multi2_list.append((name_1, name_2))
            compounds_list.append(compound)
        else:
            pass
        
                
                    

    df1 = pd.DataFrame.from_dict(dict_1, orient='index')
    data_fr1 = df1.transpose()
    px_mm = 1200 / 25.4
    data_frame_1 = data_fr1.apply(lambda x: -(x/px_mm)+32.5)

    df2 = pd.DataFrame.from_dict(dict_2, orient='index')
    data_fr2 = df2.transpose()
    px_mm = 1200 / 25.4
    data_frame_2 = data_fr2.apply(lambda x: -(x/px_mm)+32.5)
    
    total_df = pd.concat([data_frame_1, data_frame_2], axis = 1)


    list_1 = []
    list_2 = []


    for key_1 in dict_1.keys():
        if key_1 != control_variable_1:
            list_1.append(key_1)
    new_list_1 = [control_variable_1]
    new_list_1.extend(list_1)
    lili_1 = tuple(new_list_1)

    for key_2 in dict_2.keys():
        if key_2 != control_variable_2:
            list_2.append(key_2)
    new_list_2 = [control_variable_2]
    new_list_2.extend(list_2)
    lili_2 = tuple(new_list_2)

    first = db.load(total_df, idx= lili_1)
    second = db.load(total_df, idx= lili_2)
    first.mean_diff
    second.mean_diff

    

    tuple_for_multi2 = tuple(multi2_list)
    new_object = db.load(total_df, idx= tuple_for_multi2)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
    figure, axes = plt.subplots(nrows =1, ncols=2, figsize=(48, 8))
    first.mean_diff.plot(ax=axes[0], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    second.mean_diff.plot(ax=axes[1], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    

    
    
            
    
    
    
    
    
                    
    
                
                
                    

                
                    
        
        
        
        
        
        
    
    
    
    
    


    
        
    



