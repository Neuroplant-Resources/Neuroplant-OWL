import pandas as pd
import numpy as np
import pathlib as plb
from os import path
import dabest as db
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

#accessing the location files of each well, and putting the location values of each compound into a dictionary
def getting_location_collumns_compound(row, folder_of_loc_files, dict, list_qc_nopass):

    #name of the compound, filename, wellno on that row, in which each row is a well
    name_c = row['Compound']
    compound_name = name_c.lower()
    file_name = row['File Name']
    well_name = row['WellNo']
    
    #the name of the corresponding location file
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    
    #finding the location file in the given folder that contains it
    location = folder_of_loc_files.joinpath(loc_file)
    
    #checks if the well passes quality control
    if row['Passes QC'] == 'Y':
        if location.is_file():
        
            #converts the location file into a pandas data frame
            location_file = pd.read_csv(location)
            
            #gets the location of the worms, converts it into a list
            x_pos = location_file['X']
            x_pos_list = x_pos.tolist()
        
            #if the compound is not in the dictionary, creates its key and adds the locations as its value
            if compound_name not in dict:
                dict[compound_name] = x_pos_list
            
            #if the compound is in the dictionary, appends the locations to its value
            else:
                dict[compound_name].extend(x_pos_list)
            
        else:
            pass
    
    #if the well doesn't pass quality control, adds the wellno to the list of the wells that don't pass qc
    elif row['Passes QC'] == 'N':
        list_qc_nopass.append(well_name)
        
# function for converting the dictionary that has the variable as keys and the the corresponding locations as values into a data frame, and arranging the unit from pixel per inch to mm
def converting_dict_to_dataframe_and_ppi_to_mm(di):
   
    #converts the dictionary into a data frame
    df = pd.DataFrame.from_dict(di, orient='index')
    data_fr = df.transpose()
    
    #conversion factor from pixel per inch to mm
    px_mm = 1200 / 25.4
    
    #converts all location values in the data frame from ppi to mm, and orients them to the starting position of middle from left.
    data_frame = data_fr.apply(lambda x: -(x/px_mm)+32.5)
    
    return data_frame
    

# function for data visualisation of compound as independent variable
def do_data_visualisation_compound(filename, location_filesfolder, control_name):

    #creates the dictionary that will keep compound as key, and its value as all the location values of worms under that compound
    dict = {}
    
    #converts the batch results file from a csv to a pandas data frame
    batch_res = pd.read_csv(filename)
    
    #converts the folder that contains the location values from a string to a pathlib object
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    #the list for storing the well nos that don't pass qc
    list_doesnt_pass_qc = []
    
    #loops through all the rows in the batch results data frame
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict, list_doesnt_pass_qc)
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = control_name.lower()
    list = []
    
    #loops over all the compounds in the dictionary, to distinguish the control (can find a solution without a loop)
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
            
    #creates the list where the control is the first variable, then converts it into a tuple
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    #prints that wellnos that didn't pass qc
    print('wells that didnt pass quality control', list_doesnt_pass_qc)
    
    #loads the data frame and the tuple to dabest
    new_object = db.load(data_frame, idx= lili)
    
    #shared control visualisation
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
    #to show the plot
    plt.show()

        

    
#accessing the location files of each well, and putting the location values of each strain into a dictionary
def getting_location_collumns_strain(row, folder_of_loc_files, dict, list_qc_nopass):

    #name of the strain, filename, wellno on that row, in which each row is a well
    name_s = row['Strain']
    strain_name = name_s.lower()
    file_name = row['File Name']
    well_name = row['WellNo']
    
    #the name of the corresponding location file
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    
    #finding the location file in the given folder that contains it
    location = folder_of_loc_files.joinpath(loc_file)
    
    #checks if the well passes quality control
    if row['Passes QC'] == 'Y':
        if location.is_file():
        
            #converts the location file into a pandas data frame
            location_file = pd.read_csv(location)
            
            #gets the location of the worms, converts it into a list
            x_pos = location_file['X']
            x_pos_list = x_pos.tolist()
        
            #if the strain is not in the dictionary, creates its key and adds the locations as its value
            if strain_name not in dict:
                dict[strain_name] = x_pos_list
            
            #if the strain is in the dictionary, appends the locations to its value
            else:
                dict[strain_name].extend(x_pos_list)
            
        else:
            pass
            
    #if the well doesn't pass quality control, adds the wellno to the list of the wells that don't pass qc
    elif row['Passes QC'] == 'N':
        list_qc_nopass.append(well_name)
        
    

def do_data_visualisation_strain(filename, location_filesfolder, control_name):

    #creates the dictionary that will keep strain as key, and its value as all the location values of worms under that strain
    dict = {}
    
    #converts the batch results file from a csv to a pandas data frame
    batch_res = pd.read_csv(filename)
    
    #converts the folder that contains the location values from a string to a pathlib object
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    #the list for storing the well nos that don't pass qc
    list_nopass_qc = []
    
    #loops through all the rows in the batch results data frame
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict, list_nopass_qc)
    

    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = control_name.lower()
    list = []
    
    #loops over all the compounds in the dictionary, to distinguish the control (can find a solution without a loop)
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
            
    #creates the list where the control is the first variable, then converts it into a tuple
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)

    #prints that wellnos that didn't pass qc
    print('wells that didnt pass quality control', list_nopass_qc)
    
    #loads the data frame and the tuple to dabest
    new_object = db.load(data_frame, idx= lili)
    
    #shared control visualisation
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    #to show the plot
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


    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

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

    sns.set_theme()
    df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    print(df_for_lineplot_nan_removed)
    line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
    line.xaxis.set_major_locator(ticker.MultipleLocator(5))
    line.xaxis.set_major_formatter(ticker.ScalarFormatter())
    line.yaxis.set_major_locator(ticker.MultipleLocator(5))
    line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))

    plt.show()
  

#function for removing the unit writing from the time point
def turn_to_number(string):
    s2 = ''
    for char in string:
        if char.isdigit():
            s2 += char
        if not char.isdigit() and len(s2) != 0:
            return s2
    return s2
    
    
        
    ############################################shared control plots with color #############################################
    
def do_data_visualisation_compound_color(filename, location_filesfolder, control_name, color_key):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    list_doesnt_pass_qc = []
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict, list_doesnt_pass_qc)
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = control_name.lower()
    list = []
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    dict_colors = {}
    for color in color_key.keys():
        if color in new_list:
            color_match = color_key[color]
            dict_colors[color] = color_match
    
    
    print('wells that didnt pass quality control', list_doesnt_pass_qc)
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()

    
    
    
    
def do_data_visualisation_strain_color(filename, location_filesfolder, control_name, color_key):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    list_nopass_qc = []
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict, list_nopass_qc)
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = control_name.lower()
    list = []
    for key in dict.keys():
        if key.lower() != control:
            list.append(key)
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    dict_colors = {}
    for color in color_key.keys():
        if color in new_list:
            color_match = color_key[color]
            dict_colors[color] = color_match

    print('wells that didnt pass quality control', list_nopass_qc)
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()

    
    
    
def do_data_visualisation_timelapse_color(filename, location_filesfolder, control_name, color_key):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_timelapse(row, folder_of_loc_files, dict)
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
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
    
    dict_colors = {}
    for color in color_key.keys():
        if color in new_list:
            color_match = color_key[color]
            dict_colors[color] = color_match
    
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()
    
    
    
     ######################unpaired two group estimation plot##############################
     
def do_data_visualisation_compound_2_group(filename, location_filesfolder, control_name, test_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    list_doesnt_pass_qc = []
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_compound(row, folder_of_loc_files, dict, list_doesnt_pass_qc)
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = control_name.lower()
    test = test_name.lower()
    

    print('wells that didnt pass quality control', list_doesnt_pass_qc)
    new_object = db.load(data_frame, idx= (control, test))
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()

    
    
    
def do_data_visualisation_strain_2_group(filename, location_filesfolder, control_name, test_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)
    list_nopass_qc = []
    
    for index, row in batch_res.iterrows():
        getting_location_collumns_strain(row, folder_of_loc_files, dict, list_nopass_qc)
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = control_name.lower()
    test = test_name.lower()
    
    print('wells that didnt pass quality control', list_nopass_qc)
    new_object = db.load(data_frame, idx= (control, test))
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Mean differene (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    plt.show()

        
    ##################Multi Two Group Estimation Plot ##################################

        





def multi2group_dataviz_1(filename, location_filesfolder, strain_control, compound_1, compound_2):
    
    file = pd.read_csv(filename)
    folder = plb.Path(location_filesfolder)
    dict_1 = {}
    dict_2 = {}
    control_variable_1 = compound_1 + '_' + strain_control
    control_variable_2 = compound_2 + '_' + strain_control
    strains_list = [strain_control]
    multi2_list = [(control_variable_1, control_variable_2)]
    list_doesnt_pass_qc = []

    for index, row in file.iterrows():
        file_name = row['File Name']
        well = row['WellNo']
        location_file_name = 'loc_' + file_name + '_' + well + '.csv'
        locationfile = folder.joinpath(location_file_name)
        strain = row['Strain']
        compound = row['Compound']
        
        if row['Passes QC'] == 'Y':

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
#                    name_1 = compound_1 + '_' + strain
#                    name_2 = compound_2 + '_' + strain
#                    multi2_list.append((name_1, name_2))
                    strains_list.append(strain)
            else:
                pass
                
        elif row['Passes QC'] == 'N':
            list_doesnt_pass_qc.append(well)
        
                
                    
    data_frame_1 = converting_dict_to_dataframe_and_ppi_to_mm(dict_1)
    data_frame_2 = converting_dict_to_dataframe_and_ppi_to_mm(dict_2)

    
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

    list_for_dataviz = []
    for s in strains_list:
        n1 = compound_1 + '_' + s
        n2 = compound_2 + '_' + s
        if n1 in dict_1.keys() and n2 in dict_2.keys():
            tuple_to_add = (n1, n2)
            list_for_dataviz.append(tuple_to_add)
            
    tuple_for_dataviz = tuple(list_for_dataviz)
    #assumes that at least 1 well of control variable passes qc!
            
        
    

    tuple_for_multi2 = tuple(multi2_list)
    new_object = db.load(total_df, idx= tuple_for_dataviz)
    figure, axes = plt.subplots(nrows =1, ncols=2, figsize=(48, 8))
 #   if colors_key == 'Select file':
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    first.mean_diff.plot(ax=axes[0], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    second.mean_diff.plot(ax=axes[1], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#    else:
#        mm_refs_plot = new_object.mean_diff.plot(custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#        first.mean_diff.plot(ax=axes[0], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#        second.mean_diff.plot(ax=axes[1], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    print('wells that didnt pass quality control', list_doesnt_pass_qc)
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
    list_doesnt_pass_qc = []
    
    for index, row in file.iterrows():
        file_name = row['File Name']
        well = row['WellNo']
        location_file_name = 'loc_' + file_name + '_' + well + '.csv'
        locationfile = folder.joinpath(location_file_name)
        strain = row['Strain']
        compound = row['Compound']

        
        if row['Passes QC'] == 'Y':
        
    
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
#                    name_1 = strain_1 + '_' + compound
#                    name_2 = strain_2 + '_' + compound
#                    multi2_list.append((name_1, name_2))
                    compounds_list.append(compound)
            else:
                pass
        
        elif row['Passes QC'] == 'N':
            list_doesnt_pass_qc.append(well)

        
        
                
                    

    data_frame_1 = converting_dict_to_dataframe_and_ppi_to_mm(dict_1)
    data_frame_2 = converting_dict_to_dataframe_and_ppi_to_mm(dict_2)
    
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
    
    list_for_dataviz = []
    for c in compounds_list:
        n1 = strain_1 + '_' + c
        n2 = strain_2 + '_' + c
        if n1 in dict_1.keys() and n2 in dict_2.keys():
            tuple_to_add = (n1, n2)
            list_for_dataviz.append(tuple_to_add)
            
    tuple_for_dataviz = tuple(list_for_dataviz)
    #assumes that at least 1 well of control variable passes qc!


    tuple_for_multi2 = tuple(multi2_list)
    new_object = db.load(total_df, idx= tuple_for_dataviz)
    figure, axes = plt.subplots(nrows =1, ncols=2, figsize=(48, 8))
 #   if colors_key == 'Select file':
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    first.mean_diff.plot(ax=axes[0], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    second.mean_diff.plot(ax=axes[1], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#    else:
#        mm_refs_plot = new_object.mean_diff.plot(custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#        first.mean_diff.plot(ax=axes[0], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
#        second.mean_diff.plot(ax=axes[1], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    print('wells that didnt pass quality control', list_doesnt_pass_qc)
    plt.show()

##########restrict under a compound when plotting strain shared control#############################################

def data_viz_for_compound_under_1_strain(filename, location_filesfolder, compound_control, one_strain):

    #creates the dictionary that will keep compound as key, and its value as all the location values of worms under that compound
    dict = {}
    
    #converts the batch results file from a csv to a pandas data frame
    batch_res = pd.read_csv(filename)
    
    #converts the folder that contains the location values from a string to a pathlib object
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    #the list for storing the well nos that don't pass qc
    list_doesnt_pass_qc = []
    
    #loops through all the rows in the batch results data frame
    for index, row in batch_res.iterrows():
        if (row['Strain']).lower() == one_strain.lower():
            getting_location_collumns_compound(row, folder_of_loc_files, dict, list_doesnt_pass_qc)
            
    dict = {key + '_' + one_strain: value for key, value in dict.items()}
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = compound_control.lower() + '_' + one_strain
    list = []
    
    #loops over all the compounds in the dictionary, to distinguish the control (can find a solution without a loop)
    for key in dict.keys():
        if key.lower() != control.lower():
            list.append(key)
            
    #creates the list where the control is the first variable, then converts it into a tuple
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    #prints that wellnos that didn't pass qc
    print('wells that didnt pass quality control', list_doesnt_pass_qc)
    
    #loads the data frame and the tuple to dabest
    new_object = db.load(data_frame, idx= lili)
    
    #shared control visualisation
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
    #to show the plot
    plt.show()

            
def data_viz_for_strain_under_1_compound(filename, location_filesfolder, strain_control, one_compound):

    #creates the dictionary that will keep compound as key, and its value as all the location values of worms under that compound
    dict = {}
    
    #converts the batch results file from a csv to a pandas data frame
    batch_res = pd.read_csv(filename)
    
    #converts the folder that contains the location values from a string to a pathlib object
    folder_of_loc_files = plb.Path(location_filesfolder)
    
    #the list for storing the well nos that don't pass qc
    list_doesnt_pass_qc = []
    
    #loops through all the rows in the batch results data frame
    for index, row in batch_res.iterrows():
        if (row['Compound']).lower() == one_compound.lower():
            getting_location_collumns_strain(row, folder_of_loc_files, dict, list_doesnt_pass_qc)
            
    dict = {key + '_' + one_compound: value for key, value in dict.items()}
    
    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)
    
    control = strain_control.lower() + '_' + one_compound
    list = []
    
    #loops over all the compounds in the dictionary, to distinguish the control (can find a solution without a loop)
    for key in dict.keys():
        if key.lower() != control.lower():
            list.append(key)
            
    #creates the list where the control is the first variable, then converts it into a tuple
    new_list = [control]
    new_list.extend(list)
    lili = tuple(new_list)
    
    #prints that wellnos that didn't pass qc
    print('wells that didnt pass quality control', list_doesnt_pass_qc)
    
    #loads the data frame and the tuple to dabest
    new_object = db.load(data_frame, idx= lili)
    
    #shared control visualisation
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
    #to show the plot
    plt.show()
    
    
####data viz for timelapse under one compound######
def do_data_visualisation_timelapse_under_1compound(filename, location_filesfolder, control_name, compound_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)

    for index, row in batch_res.iterrows():
        if (row['Compound']).lower() == compound_name.lower():
            getting_location_collumns_timelapse(row, folder_of_loc_files, dict)


    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

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

    sns.set_theme()
    df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    print(df_for_lineplot_nan_removed)
    line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
    line.xaxis.set_major_locator(ticker.MultipleLocator(5))
    line.xaxis.set_major_formatter(ticker.ScalarFormatter())
    line.yaxis.set_major_locator(ticker.MultipleLocator(5))
    line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))

    plt.show()
    
    
    
####data viz for timelapse under one strain######
def do_data_visualisation_timelapse_under_1strain(filename, location_filesfolder, control_name, strain_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)

    for index, row in batch_res.iterrows():
        if (row['Strain']).lower() == strain_name.lower():
            getting_location_collumns_timelapse(row, folder_of_loc_files, dict)


    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

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

    sns.set_theme()
    df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    print(df_for_lineplot_nan_removed)
    line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
    line.xaxis.set_major_locator(ticker.MultipleLocator(5))
    line.xaxis.set_major_formatter(ticker.ScalarFormatter())
    line.yaxis.set_major_locator(ticker.MultipleLocator(5))
    line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))

    plt.show()
  
####data viz for timelapse under one strain and one compound######
def do_data_visualisation_timelapse_under_1compound_and_1strain(filename, location_filesfolder, control_name, compound_name, strain_name):
    dict = {}
    batch_res = pd.read_csv(filename)
    folder_of_loc_files = plb.Path(location_filesfolder)

    for index, row in batch_res.iterrows():
        if (row['Strain']).lower() == strain_name.lower() and (row['Compound']).lower() == compound_name.lower():
            getting_location_collumns_timelapse(row, folder_of_loc_files, dict)


    data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

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

    sns.set_theme()
    df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
    df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    print(df_for_lineplot_nan_removed)
    line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
    line.xaxis.set_major_locator(ticker.MultipleLocator(5))
    line.xaxis.set_major_formatter(ticker.ScalarFormatter())
    line.yaxis.set_major_locator(ticker.MultipleLocator(5))
    line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    new_object = db.load(data_frame, idx= lili)
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))

    plt.show()
  
  
    
    
####extra code for multi 2 group plots################
    
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
    
    
    
                    
    
                
                
                    

                
                    
        
        
        
        
        
        
    
    
    
    
    


    
        
    



