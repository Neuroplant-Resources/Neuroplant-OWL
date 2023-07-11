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
            rawswarm_axes = mm_refs_plot.axes[0]
            contrast_axes = mm_refs_plot.axes[1]

            rawswarm_axes.yaxis.set_tick_params(tickdir='in')
            rawswarm_axes.xaxis.set_tick_params(tickdir='in')


            contrast_axes.yaxis.set_tick_params(tickdir='in')
            contrast_axes.xaxis.set_tick_params(tickdir='in')
        else:

            colors = ck.apply(lambda x: x.astype(str).str.lower())
            cols = colors.columns
            cdict = colors.set_index(cols[0])[cols[1]].to_dict()
            print(cdict)       
        
            try:
                mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', custom_palette=cdict, contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
                rawswarm_axes = mm_refs_plot.axes[0]
                contrast_axes = mm_refs_plot.axes[1]

                rawswarm_axes.yaxis.set_tick_params(tickdir='in')
                rawswarm_axes.xaxis.set_tick_params(tickdir='in')


                contrast_axes.yaxis.set_tick_params(tickdir='in')
                contrast_axes.xaxis.set_tick_params(tickdir='in')
            except ValueError:
                
                d = {k: v or 'red' for (k, v) in cdict.items()}
                #c = {k: v for k, v in cdict.items() if v}
                mm_refs_plot = new_object.mean_diff.plot(raw_marker_size=1, swarm_label = 'Worm Locations \nwithin the arena (mm)', custom_palette=d, contrast_label= 'Difference of the Mean Locations (mm)', contrast_ylim = (-20,20), swarm_ylim=(-35,35))
                rawswarm_axes = mm_refs_plot.axes[0]
                contrast_axes = mm_refs_plot.axes[1]

                rawswarm_axes.yaxis.set_tick_params(tickdir='in')
                rawswarm_axes.xaxis.set_tick_params(tickdir='in')


                contrast_axes.yaxis.set_tick_params(tickdir='in')
                contrast_axes.xaxis.set_tick_params(tickdir='in')
        #saving the pdf of the plot
        res = new_object.mean_diff.results
        save_path = plb.Path(vals['_save_loc_sc_'])
        title = vals['_fname_sc_'] + '.' + vals['_filetype_sc_'].lower()
        plt.savefig(save_path.joinpath(title))
        res.to_csv(save_path.joinpath(vals['_fname_sc_'] + '.csv'))


    

    
            
            
    
    
                
                
                    

                
                    
        
        
        
        
        
        
    
    
    
    
    


    
        
    



