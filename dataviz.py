import pandas as pd
import numpy as np
import pathlib as plb
from os import path
import os
import dabest as db
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import PySimpleGUI as sg


        
# function for converting the dictionary that has the variable as keys and the the corresponding locations as values into a data frame, and arranging the unit from pixel per inch to mm
def converting_ppi_to_mm(di):
    
    #conversion factor from pixel per inch to mm
    px_mm = 1200 / 25.4
    
    #converts all location values in the data frame from ppi to mm, and orients them to the starting position of middle from left.
    df = di.apply(lambda x: -(x/px_mm)+32.5)
    
    return df
    
    
#accessing the location files of each well, and putting the location values of each strain into a dictionary
def getting_location_collumns(row, folder_of_loc_files, c, dic):

    #name of the strain, filename, wellno on that row, in which each row is a well
    cname = row[c].lower()
    file_name = row['File Name']
    well_name = row['WellNo']
    
    #the name of the corresponding location file
    loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    
    #finding the location file in the given folder that contains it
    location = folder_of_loc_files.joinpath(loc_file)
    
    if location.is_file():
    
        #converts the location file into a pandas data frame
        location_file = pd.read_csv(location)
        
        #gets the location of the worms, converts it into a list
        x_pos = location_file['X']

        x_pos_list = x_pos.tolist()
    
        #if the strain is not in the dictionary, creates its key and adds the locations as its value
        if cname not in dic:
            dic[cname] = x_pos_list
        
        #if the strain is in the dictionary, appends the locations to its value
        else:
            dic[cname].extend(x_pos_list)
            #dic[cname].reset_index(inplace=True, drop=True)
    else:
        
        pass
            
    
    return dic
            

#2 group estimation plot for compound as independent variable
def do_dv_tg(vals):

    #creates the dictionary that will keep compound as key, and its value as all the location values of worms under that compound
    dc = {}
    
    #converts the batch results file from a csv to a pandas data frame
    batch_res = pd.read_csv(vals['_tg_sum_'])
    
    #converts the folder that contains the location values from a string to a pathlib object
    folder_of_loc_files = plb.Path(vals['_tg_loc_'])
    
    # #the list for storing the well nos that don't pass qc
    # list_doesnt_pass_qc = []
    
    # #keeping track of the number of wells that pass quality control
    # number_of_wells_that_pass_qc = 0
    cond = vals['_IV_cond_']

    #control variable
    control = vals['_control_name_'].lower()
    
    test = vals['-test_name-'].lower()

    batch_res[cond] = batch_res[cond].apply(str.lower)
    filtered = batch_res[(batch_res[cond] == control) | (batch_res[cond] == test)]
    
    # #loops through all the rows in the batch results data frame
    for index, row in filtered.iterrows():
    #     #adding compounds as keys and locations of the worms as values to the dictionary
        dc = getting_location_collumns(row, folder_of_loc_files, cond, dc)
    
    #converting the dictionary into a data frame where collumn titles are time points and converting the location units from pixel per inch to mm
    d = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dc.items() ]))
    df = converting_ppi_to_mm(d)
    

    #loads the data frame and the tuple to dabest
    new_object = db.load(df, idx= (control, test))
    
    #two group estimation plot
    mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
    #showing the plot

    plt.show()
    
#data visualisation for strain shared control estimation plot
def do_data_visualisation(vals, ck):

    condition = vals['_IV_sc_']
    
    #converts the batch results file from a csv to a pandas data frame
    batch_res = pd.read_csv(vals['_sumfile_sc_'])
    
    #converts the folder that contains the location values from a string to a pathlib object
    folder_of_loc_files = plb.Path(vals['_locfile_sc_'])
    
    #creates the dictionary that will keep strain as key, and its value as all the location values of worms under that strain

    dc = {}
    print(vals['_qc_'])
    #loops through all the rows in the batch results data frame
    if vals['_qc_'] == True:
        for index, row in batch_res.iterrows():
            if row['Passes QC'] == 'N':
                continue
            elif row['Passes QC'] == 'Y':
                dc = getting_location_collumns(row, folder_of_loc_files, condition, dc)
        #adding strains as keys and locations of the worms as values to the dictionary
    elif vals['_qc_'] == False:
        for index, row in batch_res.iterrows():
            
            dc = getting_location_collumns(row, folder_of_loc_files, condition, dc)



    #converting the dictionary into a data frame where collumn titles are time points and converting the location units from pixel per inch to mm
    d = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dc.items() ]))
    #d = pd.DataFrame.from_dict(dc)
    print(d)
    data_frame = converting_ppi_to_mm(d)    
    control = vals['_control_sc_'].lower()

    condition_list = data_frame.columns.tolist()
    condition_list = [x.lower() for x in condition_list]

    if len(condition_list) <= 1:
        sg.popup('You do not have enough conditions to plot. Recheck your data and parameters')
    else:
        condition_list.remove(control)
        condition_list.insert(0, control)


    
    #loads the data frame and the tuple to dabest
        new_object = db.load(data_frame, idx= condition_list)
        
        # #if no colors key is attached
        
        if ck.empty:
            
             #shared control visualisation
             mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
        else:

            colors = ck.apply(lambda x: x.astype(str).str.lower())
            cols = colors.columns
            cdict = colors.set_index(cols[0])[cols[1]].to_dict()
            print(cdict)       
        
            try:
                mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', custom_palette=cdict, contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
            except ValueError:
                
                d = {k: v or 'red' for (k, v) in cdict.items()}
                #c = {k: v for k, v in cdict.items() if v}
                mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', custom_palette=d, contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        #saving the pdf of the plot
        save_path = plb.Path(vals['_save_loc_sc_'])
        title = vals['_fname_sc_'] + '.' + vals['_filetype_sc_'].lower()
        plt.savefig(save_path.joinpath(title))


    
# #accesing the location files of each well, putting the locations into a dictionary where time points are keys and the corresponding values are the locations of worms under that time point
# def getting_location_collumns_timelapse(row, folder_of_loc_files, dict, number_of_wells_that_pass_qc):

#     #name of the time point, filename, wellno on that row, in which each row is a well
#     time = str(row['Time Points'])
#     file_name = row['File Name']
#     well_name = row['WellNo']
    
#     #the name of the corresponding location file
#     loc_file = 'loc_' + file_name + '_' + well_name + '.csv'
    
#     #finding the location file in the given folder that contains it
#     location = folder_of_loc_files.joinpath(loc_file)
        
#     if location.is_file():
    
#         #incrementing the number of wells that pass quality control since this well is being used in data visualisation
#         number_of_wells_that_pass_qc += 1
    
#         #converts the location file into a pandas data frame, accesing the location values and converting them to a list
#         location_file = pd.read_csv(location)
#         x_pos = location_file['X']
#         x_pos_list = x_pos.tolist()
        
#         #if the time point is not in the dictionary, creates its key and adds the locations as its value
#         if time not in dict:
#             dict[time] = x_pos_list
            
#         #if the time point is in the dictionary, appends the locations to its value
#         else:
#             dict[time].extend(x_pos_list)
#         return number_of_wells_that_pass_qc
            
#     else:
#         pass
        

 
# #putting time points in ascending order
# def putting_time_points_in_ascending_order(dict, control):

#     #list for storing the time points in ascending order
#     list = []

#     previous = 0
    
#     #looping over the time points to order them in ascending order
#     for key in dict.keys():
#         key2 = turn_to_number(key)
        
#         #if the time point is not control comparisons will be made (control will be added to the start)
#         if key != control:
        
#             #if the current time point is higher than the previous time point, the current time point will be added to the end of the list
#             if int(previous) < int(key2):
#                 list.append(key)
                
#             #if the current time point is lower than the previous time point, the correct position for the current time point will be found
#             else:
#                 #looping over the ordered time points list that is forming
#                 for i in range(len(list)):
                
#                     #removing the unit writing from the time point that is currently being looped
#                     num = turn_to_number(list[i])
                    
#                     #if the current time point (key2) is less than the time point in the list currently being looped (num), the current time point will be added there
#                     if int(key2) < int(num):
#                         list.insert(i, key)
#                         break

#         #if there are time points in the list, the previous will be set the last time point in the list
#         if len(list) != 0:
#             number = turn_to_number(list[(len(list)-1)])
#             previous = number

#     #the control (0 min) will be added to the beginning of the ordered time points list
#     new_list = [control]
#     new_list.extend(list)
    
#     #the list is converted into a tuple, since the tuple is accepted into the dabest visualisation with format (control 1, test 1, test 2, test 3, ...)
#     lili = tuple(new_list)
#     return lili
    
    
# #quality control check for timelapse assays
# def timelapse_qc_check_total_worms(batchresults_dataframe):

#     #dict for storing well nos as keys and the total worm counts of that well no as values
#     dict_1 = {}
    
#     #looping through the batch results data frame
#     for index, row in batchresults_dataframe.iterrows():
    
#         well_no = row['WellNo']
#         worm_count = row['Total Worms']
        
#         #adding worm counts to the dictionary
#         if well_no not in dict_1:
#             dict_1[well_no] = [worm_count]
#         else:
#             dict_1[well_no].append(worm_count)
    
#     print(dict_1)
   
#     #dict for storing whether the well passes quality control or not
#     dict_2 = {}
    

#     #looping through the dictionary of well no, worm totals pairs
#     for key in dict_1.keys():
    
#         all_worms_count = dict_1[key]
        
#         #mean of worm count for the well
#         mean_worm_count = sum(all_worms_count) / len(all_worms_count)
        
#         #if the mean worm counts of the well is 150 plus or minus 10%, it passes quality control
#         if mean_worm_count >= 135:
#             dict_2[key] = 'Y'
            
#         #if it doesn't, qc for that well fails
#         else:
#             dict_2[key] = 'N'
            
#     print(dict_2)
    
#     return dict_2
    
    
        
    
# #shared control estimation plot where time points are the independent variables
# def do_data_visualisation_timelapse(filename, location_filesfolder, control_name, colors_key, save_folder, save_name):

#     #creates the dictionary that will keep compound as key, and its value as all the location values of worms under that compound
#     dict = {}
    
#     #converts the batch results file from a csv to a pandas data frame
#     batch_res = pd.read_csv(filename)
    
#     #dictionary for storing quality control for timelapse
#     quality_control = timelapse_qc_check_total_worms(batch_res)
    
#     #keeping track of the number of wells that pass quality control
#     number_of_wells_that_pass_qc = 0
    
#     #the list for storing the well nos that don't pass qc
#     list_nopass_qc = []
    
#     #converts the folder that contains the location values from a string to a pathlib object
#     folder_of_loc_files = plb.Path(location_filesfolder)

#     #looping over the rows in the batch results file to fill the dictionary with time points as keys and the locations of worms under the time point as values
#     for index, row in batch_res.iterrows():
#         well_no = row['WellNo']
#         #if the well passes quality control
#         if quality_control[well_no] == 'Y':
        
#             #adding time points as keys and locations of the worms as values to the dictionary
#             number_of_wells_that_pass_qc = getting_location_collumns_timelapse(row, folder_of_loc_files, dict, number_of_wells_that_pass_qc)
    
#         #if well doesn't pass quality control, add to no pass qc
#         elif quality_control[well_no] == 'N':
#             if well_no not in list_nopass_qc:
#                 list_nopass_qc.append(well_no)
                


#     #converting the dictionary into a data frame where collumn titles are time points and converting the location units from pixel per inch to mm
#     data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

#     control = str(control_name)
    
#     #putting time points in ascending order
#     lili = putting_time_points_in_ascending_order(dict, control)
    
#     #prints the number of wells that pass quality control
#     print('number of wells that pass quality control that are used in data visualisation:', number_of_wells_that_pass_qc)
    
#     #prints that wellnos that didn't pass qc
#     print('wells that didnt pass quality control', list_nopass_qc)
    
#     sns.set_theme()
    
#     #creating a data frame where the time points and the location values are 2 collumns
#     df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    
#     #reseting the indexes, removing the unit writing (min) from the numbers, and converting the numbers to integers
#     df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    
#     #adding the plot titles, and arranging the ticks for 5 intervals
#     line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
#     line.xaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.xaxis.set_major_formatter(ticker.ScalarFormatter())
#     line.yaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    
#     #loading the data frame and the ordered list of time points into dabest
#     new_object = db.load(data_frame, idx= lili)
    
#     #if no colors key is attached
#     if colors_key == 'Select file':
        
#         #shared control visualisation
#         mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     else:
#         #checking if all the colors in the key are present in the data frame
#         dict_colors = colors_key_check(colors_key, lili)

#         #shared control visualisation with color
#         mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     if save_folder != 'Select file':
#         #saving the pdf of the plot
#         my_path = os.path.abspath(save_folder)
#         title = save_name + '.pdf'
#         plt.savefig(os.path.join(my_path, title))
        
#     #showing the plots
#     plt.show()
  

# #function for removing the unit writing from the time point
# def turn_to_number(string):
#     s2 = ''
    
#     #looping through the string
#     for char in string:
        
#         #adding to the string if character is a digit
#         if char.isdigit():
#             s2 += char
            
#         #if came across a nondigit character, finish the string
#         if not char.isdigit() and len(s2) != 0:
#             return s2
#     return s2
    
    



    
    


# #getting the locations of the worms from the location file data frame and converting the values into a list
# def getting_locations_of_worms_and_converting_into_a_list(locationfile):

#     #convert the locations file into a pandas data frame
#     locations = pd.read_csv(locationfile)
    
#     #the location values collumn in the data frame
#     location_values = locations['X']
    
#     #converting the location values of the given well into a list
#     location_x_list = location_values.tolist()
    
#     return location_x_list
    



# #looping over the dictionary keys to put the control to the start and the rest of the variables next to it as test conditions
# def creating_the_input_tuple(dict, control):

#     # list for storing the variables
#     list = []
    
#     #looping over the dictipnary keys
#     for key in dict.keys():
#         #if the current key is not control, add it to the list
#         if key.lower() != control.lower():
#             list.append(key)
            
#     #create a new list where the control is at the start and the rest of variables are next to it
#     new_list = [control]
#     new_list.extend(list)

#     #convert it into a tuple
#     lili = tuple(new_list)
#     return lili
    


# #multi 2 group plot and 2 shared control plot generation for compound as reference and strain as independent variable
# def multi2group_dataviz_1(filename, location_filesfolder, strain_control, compound_1, compound_2, colors_key):
    
#     #converts the batch results file from a csv to a pandas data frame
#     file = pd.read_csv(filename)
    
#     #converts the folder that contains the location values from a string to a pathlib object
#     folder = plb.Path(location_filesfolder)
    
#     #first dictionary for the first compound as reference
#     dict_1 = {}
    
#     #second dictionary for the second compound as reference
#     dict_2 = {}
    
#     #control strain under the first reference compound
#     control_variable_1 = compound_1 + '_' + strain_control
    
#     #control strain under the second reference compound
#     control_variable_2 = compound_2 + '_' + strain_control
    
#     #list of strains
#     strains_list = [strain_control]
    
#     #the list of tuple pairs of same strain under the 2 compounds for the multi 2 group plot
#     multi2_list = [(control_variable_1, control_variable_2)]
    
#     #the list for storing the well nos that don't pass qc
#     list_doesnt_pass_qc = []
    
#     #keeping track of the number of wells that pass quality control
#     number_of_wells_that_pass_qc = 0

#     #looping through the rows in the file (looping through each well)
#     for index, row in file.iterrows():
    
#         #filename of the given well
#         file_name = row['File Name']
        
#         #well no of the given well
#         well = row['WellNo']
        
#         #the name of the corresponding location file of the given well at the row
#         location_file_name = 'loc_' + file_name + '_' + well + '.csv'
        
#         #finding the location file in the given folder that contains it
#         locationfile = folder.joinpath(location_file_name)
        
#         #strain of the given well
#         strain = row['Strain']
        
#         #compound of the given well
#         compound = row['Compound']
        
#         #if the well is passing quality control
#         if row['Passes QC'] == 'Y':

#             #if the location file exists
#             if locationfile.is_file():
            
#                 #incrementing the number of wells that pass quality control since this well is being used in data visualisation
#                 number_of_wells_that_pass_qc += 1
            
            
#                 #name with the compound and strain
#                 name = compound + '_' + strain
            
#                 #if the compound of the given well is the first reference compound
#                 if compound == compound_1:
                
#                     #the list of the locations of the worms of the given well
#                     location_x_list = getting_locations_of_worms_and_converting_into_a_list(locationfile)

#                     #if the name is not in the list, add the name as the key and the locations list as it value to the first compound dict
#                     if name not in dict_1:
#                         dict_1[name] = location_x_list
                        
#                     #if the name is in the list, append the new locations list to it value to the first compound dict
#                     else:
#                         dict_1[name].extend(location_x_list)
                
#                 #if the compound of the given well is the second reference compound
#                 elif compound == compound_2:
                
#                     #the list of the locations of the worms of the given well
#                     location_x_list = getting_locations_of_worms_and_converting_into_a_list(locationfile)

#                     #if the name is not in the list, add the name as the key and the locations list as it value to the first compound dict
#                     if name not in dict_2:
#                         dict_2[name] = location_x_list
                        
#                     #if the name is in the list, append the new locations list to it value to the second compound dict
#                     else:
#                         dict_2[name].extend(location_x_list)
                 
#                 #if strain is not in the list, add to the strains list
#                 if strain not in strains_list:
#                     strains_list.append(strain)
#             else:
#                 pass
                
#         #if row doesn't pass quality control, add the well to the now pass qc list
#         elif row['Passes QC'] == 'N':
#             list_doesnt_pass_qc.append(well)
        
                
#     #converting the dictionaries into data frames where collumn titles are the names and converting the locations from pixel per inch to mm
#     data_frame_1 = converting_dict_to_dataframe_and_ppi_to_mm(dict_1)
#     data_frame_2 = converting_dict_to_dataframe_and_ppi_to_mm(dict_2)

#     #merging the two data frames together
#     total_df = pd.concat([data_frame_1, data_frame_2], axis = 1)

    

#     #creating the tuple for the first shared control plot under the first reference compound
#     lili_1 = creating_the_input_tuple(dict_1, control_variable_1)
    
#     #creating the tuple for the first shared control plot under the second reference compound
#     lili_2 = creating_the_input_tuple(dict_2, control_variable_2)

#     #load the first reference compound condition to dabest for shared control estimation plot
#     first = db.load(total_df, idx= lili_1)
    
#     #load the second reference compound condition to dabest for shared control estimation plot
#     second = db.load(total_df, idx= lili_2)

#     #list for the multi 2 group plot
#     list_for_dataviz = []
    
#     #looping through the strains list
#     for s in strains_list:
#         #strain under the first compound and under the second compound
#         n1 = compound_1 + '_' + s
#         n2 = compound_2 + '_' + s
        
#         #if the strain under first compound and under the second compound are existent
#         if n1 in dict_1.keys() and n2 in dict_2.keys():
#             #form the tuple pair as strain under the first reference compound and strain under the second reference compound
#             tuple_to_add = (n1, n2)
            
#             #add the tuple to mutli 2 group plot list
#             list_for_dataviz.append(tuple_to_add)
    
#     #convert the list into a tuple, it is assumed that at least 1 well of control variable passes qc!
#     tuple_for_dataviz = tuple(list_for_dataviz)

#     #load the tuple for multi 2 group plot to dabest
#     new_object = db.load(total_df, idx= tuple_for_dataviz)
    
#     #create the figure that will have the strain shared control plots under two reference compounds on two sides
#     figure, axes = plt.subplots(nrows =1, ncols=2, figsize=(48, 8))
    
#     #if color key is not selected
#     if colors_key == 'Select file':
    
#         #multi 2 group estimation plot
#         mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         first.mean_diff.plot(ax=axes[0], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         second.mean_diff.plot(ax=axes[1], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     #if color key is selected
#     else:
    
#         #multi 2 group estimation plot
#         mm_refs_plot = new_object.mean_diff.plot(custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         first.mean_diff.plot(ax=axes[0], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         second.mean_diff.plot(ax=axes[1], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#     #print the wells that didn't pass quality control
#     print('wells that didnt pass quality control', list_doesnt_pass_qc)
    
#     #prints the number of wells that pass quality control
#     print('number of wells that pass quality control that are used in data visualisation:', number_of_wells_that_pass_qc)
    
#     #showing the plots
#     plt.show()

    
# #multi 2 group plot and 2 shared control plot generation for strain as reference and compound as independent variable
# def multi2group_dataviz_2(filename, location_filesfolder, compound_control, strain_1, strain_2, colors_key):
    
#     #converts the batch results file from a csv to a pandas data frame
#     file = pd.read_csv(filename, encoding= 'unicode_escape')
    
#     #converts the folder that contains the location values from a string to a pathlib object
#     folder = plb.Path(location_filesfolder)
    
#     #first dictionary for the first strain as reference
#     dict_1 = {}
    
#     #second dictionary for the second strain as reference
#     dict_2 = {}
    
#     #control compound under the first reference strain
#     control_variable_1 = compound_control + '_' + strain_1
    
#     #control compound under the second reference strain
#     control_variable_2 = compound_control + '_' + strain_2
    
#     #compounds list
#     compounds_list = [compound_control]
    
#     #the list of tuple pairs of same compound under the 2 strains for the multi 2 group plot
#     multi2_list = [(control_variable_1, control_variable_2)]
    
#     #list of the wells that don't pass qc
#     list_doesnt_pass_qc = []
    
#     #keeping track of the number of wells that pass quality control
#     number_of_wells_that_pass_qc = 0
    
#     #looping through the rows in the file (looping through each well)
#     for index, row in file.iterrows():
        
#         #filename of the well
#         file_name = row['File Name']
        
#         #well no
#         well = row['WellNo']
        
#         #the corresponding location file for the well
#         location_file_name = 'loc_' + file_name + '_' + well + '.csv'
        
#         #finding the location file in the given folder that contains it
#         locationfile = folder.joinpath(location_file_name)
        
#         #strain of the well
#         strain = row['Strain']
        
#         #compound of the well
#         compound = row['Compound']

#         #if the well passes quality control
#         if row['Passes QC'] == 'Y':
        
#             #if the location file exists
#             if locationfile.is_file():
            
#                 #incrementing the number of wells that pass quality control since this well is being used in data visualisation
#                 number_of_wells_that_pass_qc += 1
                
#                 #name of variable
#                 name = compound + '_' + strain
            
#                 #if the strain of the given well is the first reference strain
#                 if strain == strain_1:

#                     #the list of the locations of the worms of the given well
#                     location_x_list = getting_locations_of_worms_and_converting_into_a_list(locationfile)

#                     #if the name is not in the list, add the name as the key and the locations list as it value to the first compound dict
#                     if name not in dict_1:
#                         dict_1[name] = location_x_list
                        
#                     #if the name is in the list, append the new locations list to it value to the first compound dict
#                     else:
#                         dict_1[name].extend(location_x_list)
                    
#                 #if the strain of the given well is the second reference strain
#                 elif strain == strain_2:
                
#                     #the list of the locations of the worms of the given well
#                     location_x_list = getting_locations_of_worms_and_converting_into_a_list(locationfile)

#                     #if the name is not in the list, add the name as the key and the locations list as it value to the second compound dict
#                     if name not in dict_2:
#                         dict_2[name] = location_x_list
                        
#                     #if the name is in the list, append the new locations list to it value to the second compound dict
#                     else:
#                         dict_2[name].extend(location_x_list)
                
#                 #if compound is not in the list, add to the compounds list
#                 if compound not in compounds_list:
#                     compounds_list.append(compound)
#             else:
#                 pass
                
#         #if row doesn't pass quality control, add the well to the now pass qc list
#         elif row['Passes QC'] == 'N':
#             list_doesnt_pass_qc.append(well)
            
                    
#     #converting the dictionaries into data frames where collumn titles are the names and converting the locations from pixel per inch to mm
#     data_frame_1 = converting_dict_to_dataframe_and_ppi_to_mm(dict_1)
#     data_frame_2 = converting_dict_to_dataframe_and_ppi_to_mm(dict_2)
    
#     #merging the two data frames together
#     total_df = pd.concat([data_frame_1, data_frame_2], axis = 1)


#     #creating the tuple for the first shared control plot under the first reference compound
#     lili_1 = creating_the_input_tuple(dict_1, control_variable_1)
    
#     #creating the tuple for the first shared control plot under the second reference compound
#     lili_2 = creating_the_input_tuple(dict_2, control_variable_2)

#     #load the first reference compound condition to dabest for shared control estimation plot
#     first = db.load(total_df, idx= lili_1)
    
#     #load the second reference compound condition to dabest for shared control estimation plot
#     second = db.load(total_df, idx= lili_2)

#     #list for the multi 2 group plot
#     list_for_dataviz = []
    
            
#     #looping through the compounds list
#     for c in compounds_list:
#         #compound under the first strain and under the second strain
#         n1 = c + '_' + strain_1
#         n2 = c + '_' + strain_2
#         #if the strain under first compound and under the second compound are existent
#         if n1 in dict_1.keys() and n2 in dict_2.keys():
#             #form the tuple pair as strain under the first reference compound and strain under the second reference compound
#             tuple_to_add = (n1, n2)
#             list_for_dataviz.append(tuple_to_add)
            
#     #convert the list into a tuple, it is assumed that at least 1 well of control variable passes qc!
#     tuple_for_dataviz = tuple(list_for_dataviz)
    
#     #load the tuple for multi 2 group plot to dabest
#     new_object = db.load(total_df, idx= tuple_for_dataviz)
    
#     #create the figure that will have the strain shared control plots under two reference compounds on two sides
#     figure, axes = plt.subplots(nrows =1, ncols=2, figsize=(48, 8))
    
#     #if color key is not selected
#     if colors_key == 'Select file':
    
#         #multi 2 group estimation plot
#         mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         first.mean_diff.plot(ax=axes[0], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         second.mean_diff.plot(ax=axes[1], raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     #if color key is selected
#     else:
    
#         #multi 2 group estimation plot
#         mm_refs_plot = new_object.mean_diff.plot(custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         first.mean_diff.plot(ax=axes[0], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#         #shared control plot under the first reference compound on the left of the second plot
#         second.mean_diff.plot(ax=axes[1], custom_palette=colors_key, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#     #print the wells that didn't pass quality control
#     print('wells that didnt pass quality control', list_doesnt_pass_qc)
    
#     #prints the number of wells that pass quality control
#     print('number of wells that pass quality control that are used in data visualisation:', number_of_wells_that_pass_qc)
    
#     #showing the plots
#     plt.show()

    



    
    
# #shared control estimation plot for time points as independent variable restriction under 1 compound condition
# def do_data_visualisation_timelapse_under_1compound(filename, location_filesfolder, control_name, compound_name, colors_key, save_folder, save_name):

#     #creates the dictionary that will keep time points as key, and its value as all the location values of worms under that compound
#     dict = {}
    
#     #converts the batch results file from a csv to a pandas data frame
#     batch_res = pd.read_csv(filename)
    
#     #converts the folder that contains the location values from a string to a pathlib object
#     folder_of_loc_files = plb.Path(location_filesfolder)
    
#     #keeping track of the number of wells that pass quality control
#     number_of_wells_that_pass_qc = 0
    
#     #the list for storing the well nos that don't pass qc
#     list_nopass_qc = []
    
#     #dictionary for storing quality control for timelapse
#     quality_control = timelapse_qc_check_total_worms(batch_res)

#     #loops through all the rows in the batch results data frame
#     for index, row in batch_res.iterrows():
        
#         well_no = row['WellNo']
    
#         #checking if the compound of the well is the selected compound
#         if (row['Compound']).lower() == compound_name.lower():
        
#             #if the well passes quality control
#             if quality_control[well_no] == 'Y':
            
#                 #adding time points as keys and locations of the worms as values to the dictionary
#                 number_of_wells_that_pass_qc = getting_location_collumns_timelapse(row, folder_of_loc_files, dict, number_of_wells_that_pass_qc)
                
#             #if well doesn't pass quality control, add to no pass qc
#             elif quality_control[well_no] == 'N':
#                 if well_no not in list_nopass_qc:
#                     list_nopass_qc.append(well_no)

#     #converting the dictionary into a data frame and changing the locations from pixel per inch to mm
#     data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

#     control = str(control_name)

#     #putting time points in ascending order
#     lili = putting_time_points_in_ascending_order(dict, control)
    
#     #prints the number of wells that pass quality control
#     print('number of wells that pass quality control that are used in data visualisation:', number_of_wells_that_pass_qc)
    
#     #prints that wellnos that didn't pass qc
#     print('wells that didnt pass quality control', list_nopass_qc)

#     sns.set_theme()
    
#     #creating a data frame where the time points and the location values are 2 collumns
#     df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    
#     #reseting the indexes, removing the unit writing (min) from the numbers, and converting the numbers to integers
#     df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    
#     #adding the plot titles, and arranging the ticks for 5 intervals
#     line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
#     line.xaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.xaxis.set_major_formatter(ticker.ScalarFormatter())
#     line.yaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    
#     #loading the data frame and the ordered list of time points into dabest
#     new_object = db.load(data_frame, idx= lili)
    
#     #if no colors key is attached
#     if colors_key == 'Select file':
        
#         #shared control visualisation
#         mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     else:
#         #checking if all the colors in the key are present in the data frame
#         dict_colors = colors_key_check(colors_key, lili)

#         #shared control visualisation with color
#         mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
#     if save_folder != 'Select file':
#         #saving the pdf of the plot
#         my_path = os.path.abspath(save_folder)
#         title = save_name + '.pdf'
#         plt.savefig(os.path.join(my_path, title))
    

#     #showing the plots
#     plt.show()
    
    
# #shared control estimation plot for time points as independent variable restriction under 1 compound condition
# def do_data_visualisation_timelapse_under_1strain(filename, location_filesfolder, control_name, strain_name, colors_key, save_folder, save_name):
#     #creates the dictionary that will keep time points as key, and its value as all the location values of worms under that compound
#     dict = {}
    
#     #converts the batch results file from a csv to a pandas data frame
#     batch_res = pd.read_csv(filename)
    
#     #converts the folder that contains the location values from a string to a pathlib object
#     folder_of_loc_files = plb.Path(location_filesfolder)
    
    
#     #dictionary for storing quality control for timelapse
#     quality_control = timelapse_qc_check_total_worms(batch_res)
    
#     #keeping track of the number of wells that pass quality control
#     number_of_wells_that_pass_qc = 0
    
#     #the list for storing the well nos that don't pass qc
#     list_nopass_qc = []

#     #loops through all the rows in the batch results data frame
#     for index, row in batch_res.iterrows():
    
#         well_no = row['WellNo']
    
#         #checking if the strain of the well is the selected strain
#         if (row['Strain']).lower() == strain_name.lower():
        
#             #if the well passes quality control
#             if quality_control[well_no] == 'Y':
            
#                 #adding time points as keys and locations of the worms as values to the dictionary
#                 number_of_wells_that_pass_qc = getting_location_collumns_timelapse(row, folder_of_loc_files, dict, number_of_wells_that_pass_qc)
                
#             #if well doesn't pass quality control, add to no pass qc
#             elif quality_control[well_no] == 'N':
#                 if well_no not in list_nopass_qc:
#                     list_nopass_qc.append(well_no)

#     #converting the dictionary into a data frame and changing the locations from pixel per inch to mm
#     data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

#     control = str(control_name)
    
#     #putting time points in ascending order
#     lili = putting_time_points_in_ascending_order(dict, control)

#     #prints the number of wells that pass quality control
#     print('number of wells that pass quality control that are used in data visualisation:', number_of_wells_that_pass_qc)
    
#     #prints that wellnos that didn't pass qc
#     print('wells under the restricted condition that didnt pass quality control', list_nopass_qc)
    
#     sns.set_theme()
    
#     #creating a data frame where the time points and the location values are 2 collumns
#     df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    
#     #reseting the indexes, removing the unit writing (min) from the numbers, and converting the numbers to integers
#     df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    
#     #adding the plot titles, and arranging the ticks for 5 intervals
#     line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
#     line.xaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.xaxis.set_major_formatter(ticker.ScalarFormatter())
#     line.yaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    
#     #loading the data frame and the ordered list of time points into dabest
#     new_object = db.load(data_frame, idx= lili)
    
#     #if no colors key is attached
#     if colors_key == 'Select file':
        
#         #shared control visualisation
#         mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     else:
#         #checking if all the colors in the key are present in the data frame
#         dict_colors = colors_key_check(colors_key, lili)

#         #shared control visualisation with color
#         mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
        
#     if save_folder != 'Select file':
#         #saving the pdf of the plot
#         my_path = os.path.abspath(save_folder)
#         title = save_name + '.pdf'
#         plt.savefig(os.path.join(my_path, title))
    

#     #showing the plots
#     plt.show()
    
  
# #shared control estimation plot for time points as independent variable restriction under 1 compound condition
# def do_data_visualisation_timelapse_under_1compound_and_1strain(filename, location_filesfolder, control_name, compound_name, strain_name, colors_key, save_folder, save_name):
#     #creates the dictionary that will keep time points as key, and its value as all the location values of worms under that compound
#     dict = {}
    
#     #converts the batch results file from a csv to a pandas data frame
#     batch_res = pd.read_csv(filename)
    
#     #converts the folder that contains the location values from a string to a pathlib object
#     folder_of_loc_files = plb.Path(location_filesfolder)
    
    
#     #dictionary for storing quality control for timelapse
#     quality_control = timelapse_qc_check_total_worms(batch_res)
    
#     #keeping track of the number of wells that pass quality control
#     number_of_wells_that_pass_qc = 0
    
#     #the list for storing the well nos that don't pass qc
#     list_nopass_qc = []

#     #loops through all the rows in the batch results data frame
#     for index, row in batch_res.iterrows():
    
#         well_no = row['WellNo']
    
#         #checking if the strain of the well is the selected strain and the compound of the well is the selected compound
#         if (row['Strain']).lower() == strain_name.lower() and (row['Compound']).lower() == compound_name.lower():
        
#             #if the well passes quality control
#             if quality_control[well_no] == 'Y':
            
#                 #adding time points as keys and locations of the worms as values to the dictionary
#                 number_of_wells_that_pass_qc = getting_location_collumns_timelapse(row, folder_of_loc_files, dict, number_of_wells_that_pass_qc)
                
#             #if well doesn't pass quality control, add to no pass qc
#             elif quality_control[well_no] == 'N':
#                 if well_no not in list_nopass_qc:
#                     list_nopass_qc.append(well_no)

#     #converting the dictionary into a data frame and changing the locations from pixel per inch to mm
#     data_frame = converting_dict_to_dataframe_and_ppi_to_mm(dict)

#     control = str(control_name)

#     #putting time points in ascending order
#     lili = putting_time_points_in_ascending_order(dict, control)
    
#     #prints the number of wells that pass quality control
#     print('number of wells that pass quality control that are used in data visualisation:', number_of_wells_that_pass_qc)
    
#     #prints that wellnos that didn't pass qc
#     print('wells under the restricted condition that didnt pass quality control', list_nopass_qc)

#     sns.set_theme()
    
#     #creating a data frame where the time points and the location values are 2 collumns
#     df_for_lineplot = data_frame.melt(var_name= 'time point (min)', value_name= 'mean of worm locations at a given time point')
    
#     #reseting the indexes, removing the unit writing (min) from the numbers, and converting the numbers to integers
#     df_for_lineplot_nan_removed = df_for_lineplot.dropna().reset_index(drop=True)
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].apply(lambda x: turn_to_number(x))
#     df_for_lineplot_nan_removed['time point (min)'] = df_for_lineplot_nan_removed['time point (min)'].astype('int')
    
#     #adding the plot titles, and arranging the ticks for 5 intervals
#     line = sns.lineplot(data= df_for_lineplot_nan_removed, x = 'time point (min)', y = 'mean of worm locations at a given time point', ci = 'sd')
#     line.xaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.xaxis.set_major_formatter(ticker.ScalarFormatter())
#     line.yaxis.set_major_locator(ticker.MultipleLocator(5))
#     line.yaxis.set_major_formatter(ticker.ScalarFormatter())
    
#     #loading the data frame and the ordered list of time points into dabest
#     new_object = db.load(data_frame, idx= lili)
    
#     #if no colors key is attached
#     if colors_key == 'Select file':
        
#         #shared control visualisation
#         mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
    
#     else:
#         #checking if all the colors in the key are present in the data frame
#         dict_colors = colors_key_check(colors_key, lili)

#         #shared control visualisation with color
#         mm_refs_plot = new_object.mean_diff.plot(custom_palette=dict_colors, raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
        
        
#     if save_folder != 'Select file':
#         #saving the pdf of the plot
#         my_path = os.path.abspath(save_folder)
#         title = save_name + '.pdf'
#         plt.savefig(os.path.join(my_path, title))
    

#     #showing the plots
#     plt.show()
    
    


            
            
        
        
            
    
            
    
            
            
    
    
                
                
                    

                
                    
        
        
        
        
        
        
    
    
    
    
    


    
        
    



