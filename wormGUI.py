import PySimpleGUI as sg
import analyze_image as ai
import pathlib as plb
import unblind_key as un
import tkinter as tk
import dataviz as dv
import timepoint_add as tl
import colors_key as ck

#import connect_metadata as cm
sg.ChangeLookAndFeel('GreenTan')

### Generates the first window that the user encounters.
### Opens upon running the program
def make_win1():
    layout1 = [
    [sg.Text('Welcome to the Worm Counter!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Text('Choose whether you would like to process a single image or a batch of images', font=(14))],
    [sg.Frame(layout=[[sg.Radio('Single Image', 'RADIO1', default=False, size=(40,1), key='_SINGLE_', enable_events=True, font=(14)), sg.Radio('Batch', 'RADIO1', key='_BATCH_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('_'  * 120)],
    [sg.Text('Would you like to perform data visualization?', font=(14))],
    [sg.Frame(layout=[[sg.Radio('Yes, two group estimation plot', 'RADIO1', default=False, size=(50,1), key='_DataVizTwoGroup_', enable_events=True, font=(14))], [sg.Radio('Yes,  shared control estimation plot', 'RADIO1', key='_DataVizSharedControl_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    #[sg.Radio('Yes, multi 2 group estimation plot (multiple controls)', 'RADIO1', key='_DataVizMultiTwo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('_'  * 120)],
     [sg.Text('Would you like to unblind your metadata sheet or your batch results file?',size=(80,1), font='Lucida', justification='left')], [sg.Radio('Yes', 'RADIO1', default=False, key='_Yes_', enable_events=True, font=(14))],
    [sg.Text('_'  * 120)],
    [sg.Text('If you have timelapse scans, would you like to add time points collumn to your batch results file?',size=(100,1), font='Lucida', justification='left')], [sg.Radio('Yes', 'RADIO1', default=False, key='_TimeLapseCollumn_', enable_events=True, font=(14))]
    , [sg.Exit()]]

    window1 = sg.Window('Worm Counter', layout1, default_element_size=(60, 2), resizable=True, finalize=True)
    return window1

### Makes the window to process multiple images
def make_batch_win():
    layout2 = [
    [sg.Text('Select your metadata file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='right', visible='False'), sg.InputText('Select file', key = 'md_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select a folder to store your results: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='right'),sg.InputText('Default Folder', key = '-results_folder-'), sg.FolderBrowse()],
    [sg.Text('Select the folder that contains the images to be analyzed: ',  size=(50, 1), font=(12),auto_size_text=False, justification='right'),sg.InputText('Default Folder', key='-image_folder-',), sg.FolderBrowse()],
    [sg.Text('Name your results file ', size=(50, 1), auto_size_text=False, justification='right', font=(12)),
    sg.InputText('Batch_results', key='-name-') ],
    [sg.Button('Analyze'),sg.Button('Back')], [sg.Exit()]]

    batch_window = sg.Window('Batch Image Counter', layout2, default_element_size=(80, 1), resizable=True, finalize=True)
    return batch_window


### Creates the GUI window to process one image at a time
def make_single_win():
    layout3 = [
    [sg.Frame('Single Pic', key = '_test_', font=(14), layout=[

    [sg.Frame('Worm Strains in Each Well', visible = False, key='-4Strains-', font=(14),layout=[
    [sg.Text('Strain in Well P', size=(15,1), font=(12)), sg.InputText(key='-StrainP-')],
    [sg.Text('Strain in Well Q', size=(15,1), font=(12)), sg.InputText(key='-StrainQ-')],
    [sg.Text('Strain in Well R', size=(15,1), font=(12)), sg.InputText(key='-StrainR-')],
    [sg.Text('Strain in Well S', size=(15,1), font=(12)), sg.InputText(key='-StrainS-')]])],

    [sg.Frame('Slot 1 Data', visible = True, font=(14), layout=[
    #[sg.Checkbox('Check this box if you there are multiple strains on this plate', enable_events=True ,key='-show_strains-', size=(10,1))],
    [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID1-')],
    [sg.Text('Strain on Plate 1', size=(15,1), font=(12)), sg.InputText(key='-Strain1-')],
    [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound1-')]]
    ),
    sg.Frame('Slot 2 Data',visible = True, font=(12), layout=[
    [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID2-')],
    [sg.Text('Strain on Plate 2', size=(15,1), font=(12)), sg.InputText(key='-Strain2-')],
    [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound2-')]
    ])],

    [sg.Frame('Slot 3 Data',visible = True, font=(14), layout=[
    [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID3-')],
    [sg.Text('Strain on Plate 3', size=(15,1), font=(12)), sg.InputText(key='-Strain3-')],
    [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound3-')]]
    ),
    sg.Frame('Slot 4 Data',visible = True,  font=(14), layout=[
    [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID4-')],
    [sg.Text('Strain on Plate 4', size=(15,1), font=(12)), sg.InputText(key='-Strain4-')],
    [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound4-')]
    ])],

    [sg.Frame('Choose the image file to be analyzed', visible=True, font=(12),layout=[
    [sg.Text('Choose a folder to save your results in: ', size=(40, 1), auto_size_text=False, font=(12), justification='right'),
        sg.InputText('Results folder', key='-results-'), sg.FolderBrowse()],
    [sg.Text('Select the image to be analyzed', size=(40, 1), auto_size_text=False, font=(12), justification='right'), sg.InputText('Image file', key='-file-'), sg.FileBrowse()],
        [sg.Button('Analyze'), sg.Button('Back'), sg.Exit()]])]
    ])]]

    single_im = sg.Window('Single Image Processing', layout3, default_element_size=(80, 1), resizable=True, finalize=True)
    return single_im
 

def unblind_window():
    layout4 = [
    [sg.Text('Would you like to unblind your batch results file or your metadata sheet?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Batch Results File', 'RADIO2', default=False, key='_BatchFile_', enable_events=True, font=(14)), sg.Radio('Metadata Sheet', 'RADIO2', key='_Metadata_Sheet_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select the file you would like to unblind: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'metadata_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select your blinding key: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'key_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select a folder to store your results: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-results_folder-'), sg.FolderBrowse()],
     [sg.Text('Name your unblinded metadata sheet:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Unblinded Metadata', key='-metadata_name-')],
    [sg.Text('_'  * 140)],
    [sg.Text('Would you like to unblind only the compound names, only the strain names, or both?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO3', default=False, key='_Com_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO3', key='_Strain_', enable_events=True, font=(14)), sg.Radio('Both', 'RADIO3', key='_Both_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
        [sg.Button('Unblind'), sg.Button('Back')], [sg.Exit()]]
    
    u_win = sg.Window('Unblinding Metadata', layout4, size=(900,350), resizable=True, finalize=True)
    return u_win
    
def timelapse_window():
    layout4 = [
    [sg.Text('If you have time lapse analysis, you may add a time point collumn to your batch results file by using the time lapse key template that matches the file name to the time point',size=(120,1), font='Lucida', justification='left')],
    [sg.Text('Select your batch results file that you would like the time points collumn to be added to: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'filefortimelapse_', visible='False'), sg.FileBrowse()],
    [sg.Text('Select your time lapse key: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'timelapsekey_', visible='False'), sg.FileBrowse()],
    [sg.Text('Select a folder to store the new file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-tl_folder-'), sg.FolderBrowse()],
     [sg.Text('Name your file with the time points collumn:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('File with Time Points', key='-filenamewithtimelapse-')],
    [sg.Text('_'  * 140)],
        [sg.Button('Add TimePoints'), sg.Button('Back')], [sg.Exit()]]
    
    tl_win = sg.Window('Time Lapse Analysis Collumn', layout4, size=(900,250), resizable=True, finalize=True)
    return tl_win
    

def dataviz_options_window():
    layout5 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14)), sg.Radio('Time Lapse', 'RADIO2', key='_TimeLapse_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('If you prefer to select your colors, attach a colors key, otherwise leave blank:', size=(50, 2),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'col_key', visible='False'), sg.FileBrowse()],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_options_win = sg.Window('Data Visualization Options', layout5, size=(900,300), resizable=True, finalize=True)
    return dataviz_options_win
    
    
def dataviz_twogroup_window():
    layout6 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('What is the name of your test variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Test', key='-test_name-')],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_twogroup_win = sg.Window('Data Visualization Options', layout6, size=(900,250), resizable=True, finalize=True)
    return dataviz_twogroup_win


#def dataviz_multitwo_window():
#    layout7 = [
#    [sg.Text('Are you doing a pairwise comparison between compounds or strains?',size=(100,1), font='Lucida', justification='left')],
#        [sg.Frame(layout=[
#            [sg.Radio('2 kinds of compounds', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('2 kinds of strains', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
#    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
#    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
#    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
#    sg.InputText('Control', key='-control_name-')],
#    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
#    dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,250), resizable=True, finalize=True)
#    return dataviz_multitwo_win
    
def dataviz_multitwo_window():
    layout7 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('Please input the control - test pairs below. If you have less pairs than the number of questions, please leave the extra questions as it is.', size=(100, 1), auto_size_text=False, justification='left', font=(12))],
    [sg.InputText('Control1', key='-control1_name-'), sg.InputText('Test1', key='-test1_name-')],
    [sg.InputText('Control2', key='-control2_name-'), sg.InputText('Test2', key='-test2_name-')],
    [sg.InputText('Control3', key='-control3_name-'), sg.InputText('Test3', key='-test3_name-')],
    [sg.InputText('Control4', key='-control4_name-'), sg.InputText('Test4', key='-test4_name-')],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,250), resizable=True, finalize=True)
    return dataviz_multitwo_win
    

    
    
def check_fpaths(ipath, rpath):
        return True


### This funtion initiates the GUI
def make_GUI():
    win1 = make_win1()
    while True:
        event, values = win1.read()
        
        ### If exit button is clicked then the whole program is terminated
        if event in (None, 'Exit'):
            break
              
        

        ### Opens a window to analyze a batch of images
        ### Does not currently incorporate metadata for a batch of images but creates the fields to do so
        ### User is returned to the main page upon completion of analysis
        if values['_BATCH_']:
            win1.hide()
            batch_win = make_batch_win()
            while True:
                e2, v2 = batch_win.read()
                if e2 in (None, 'Exit'):
                    break
                if e2 == 'Analyze':
                    mdpath = (v2['md_file'])
                    rpath = (v2['-results_folder-'])
                    fpath = (v2['-image_folder-'])
                    results_name = (v2['-name-'])

                    im_path = plb.Path(fpath)
                    res_path = plb.Path(rpath)
                    
                    if im_path.exists() and res_path.exists():
                        ai.batch_process(fpath, rpath, mdpath, v2, e2, results_name)
                        batch_win.close()
                        make_GUI()
                        break
                    else:
                        sg.popup('Please enter a valid file or folder path')
                if e2 == 'Back':
                    batch_win.close()
                    make_GUI()
                    break
            batch_win.close()
            break
        
        ### Opens up a new window to analyze one image at a time.
        ### User can currently only add one strain and one compound to a plate
        ### User is not required to fill in a values for each plate
        if values['_SINGLE_']:
            win1.hide()
            single_win = make_single_win()
            while True:
                e3, v3 = single_win.read()
                if e3 == 'Analyze':
                    fpath = (v3['-file-'])
                    rpath = (v3['-results-'])
                    im_path = plb.Path(fpath)
                    res_path = plb.Path(rpath)
                    if im_path.exists() and res_path.exists():
                        ai.single_process(fpath, rpath, v3, e3)
                        single_win.close()
                        make_GUI()
                        break
                    else:
                        sg.popup('Please enter a valid file or folder path')
                if e3 == 'Back':
                    single_win.close()
                    make_GUI()
                    break
                if e3 in (None, 'Exit'):
                    break
            single_win.close()
            break
            

        if values['_Yes_']:
            win1.hide()
            unblind = unblind_window()
            while True:
                e4, v4 = unblind.read()
                if e4 == 'Back':
                    unblind.close()
                    make_GUI()
                    break
                if e4 in (None, 'Exit'):
                    break
                if e4 == 'Unblind':
                    unblind_process(v4, unblind)
                    exit()
            
                
        if values['_DataVizSharedControl_']:
            win1.hide()
            dataviz_options = dataviz_options_window()
            while True:
                e5, v5 = dataviz_options.read()
                if e5 == 'Back':
                    dataviz_options.close()
                    make_GUI()
                    break
                if e5 == sg.WIN_CLOSED or e5 == 'Exit':
                    break
                if e5 == 'Do Data Vis':
                    batch_res = v5['batch_results_file']
                    loc_files_folder = v5['-location_files_folder-']
                    control_name = v5['-control_name-']
                    colors_key = v5['col_key']
                    if colors_key == 'Select file':
                        if v5['_CompoundInfo_']:
                            dv.do_data_visualisation_compound(batch_res, loc_files_folder, control_name)
                        elif v5['_StrainInfo_']:
                            dv.do_data_visualisation_strain(batch_res, loc_files_folder, control_name)
                        elif v5['_TimeLapse_']:
                            dv.do_data_visualisation_timelapse(batch_res, loc_files_folder, control_name)
                    else:
                        colors_dict = ck.dict_color_key(colors_key)
                        if v5['_CompoundInfo_']:
                            dv.do_data_visualisation_compound_color(batch_res, loc_files_folder, control_name, colors_dict)
                        elif v5['_StrainInfo_']:
                            dv.do_data_visualisation_strain_color(batch_res, loc_files_folder, control_name, colors_dict)
                        elif v5['_TimeLapse_']:
                            dv.do_data_visualisation_timelapse_color(batch_res, loc_files_folder, control_name, colors_dict)
                        
                        
        
        if values['_DataVizTwoGroup_']:
            win1.hide()
            dataviz_twogroup = dataviz_twogroup_window()
            while True:
                e6, v6 = dataviz_twogroup.read()
                if e6 == 'Back':
                    dataviz_twogroup.close()
                    make_GUI()
                    break
                if e6 == sg.WIN_CLOSED or e6 == 'Exit':
                    break
                if e6 == 'Do Data Vis':
                    batch_res = v6['batch_results_file']
                    loc_files_folder = v6['-location_files_folder-']
                    control_name = v6['-control_name-']
                    test_name = v6['-test_name-']
                    if v6['_CompoundInfo_']:
                        dv.do_data_visualisation_compound_2_group(batch_res, loc_files_folder, control_name, test_name)
                    elif v6['_StrainInfo_']:
                        dv.do_data_visualisation_strain_2_group(batch_res, loc_files_folder, control_name, test_name)
                    
                        
#        if values['_DataVizMultiTwo_']:
#            win1.hide()
#            dataviz_multitwo = dataviz_multitwo_window()
#            while True:
#                e7, v7 = dataviz_multitwo.read()
#                if e7 == 'Back':
#                    dataviz_multitwo.close()
#                    make_GUI()
#                    break
#                if e7 == sg.WIN_CLOSED or e7 == 'Exit':
#                    break
#                if e7 == 'Do Data Vis':
#                    batch_res = v7['batch_results_file']
#                    loc_files_folder = v7['-location_files_folder-']
#                    c1 = v7['-control1_name-']
#                    t1 = v7['-test1_name-']
#                    c2 = v7['-control2_name-']
#                    t2 = v7['-test2_name-']
#                    c3 = v7['-control3_name-']
#                    t3 = v7['-test3_name-']
#                    c4 = v7['-control4_name-']
#                    t4 = v7['-test4_name-']
#                    if v7['_CompoundInfo_']:
#                        dv.do_data_visualisation_compound_multi2_group(batch_res, loc_files_folder, c1, t1, c2, t2, c3, t3, c4, t4)
#                    elif v7['_StrainInfo_']:
#                        dv.do_data_visualisation_strain_multi2_group(batch_res, loc_files_folder, c1, t1, c2, t2, c3, t3, c4, t4)
        
        
        if values['_TimeLapseCollumn_']:
            win1.hide()
            tl_window = timelapse_window()
            while True:
                e8, v8 = tl_window.read()
                if e8 == 'Back':
                    tl_window.hide()
                    make_GUI()
                if e8 in ('Exit', None):
                    break
                if e8 == 'Add TimePoints':
                    file = v8['filefortimelapse_']
                    key = v8['timelapsekey_']
                    name = v8['-filenamewithtimelapse-']
                    folder = v8['-tl_folder-']
                    tl.timelapse_collumn_addition(file, key, folder, name)
                    message_win()
                    tl_window.close()
                    exit()
                    
                    
                    
    win1.close()
    
    
    
def unblind_process(v4, unblind):
    metapath = (v4['metadata_file'])
    keypath = (v4['key_file'])
    rpath = (v4['-results_folder-'])
    name = v4['-metadata_name-']
    m_path = plb.Path(metapath)
    r_path = plb.Path(keypath)
    f_path = plb.Path(rpath)
    if m_path.exists() and r_path.exists():
        if v4['_Metadata_Sheet_']:
            if v4['_Com_']:
                un.solve_compound_names(metapath, keypath, rpath, name)
            elif v4['_Strain_']:
                un.solve_strain_names(metapath, keypath, rpath, name)
            elif v4['_Both_']:
                un.solve_both_strain_and_compound_names(metapath, keypath, rpath, name)
        if v4['_BatchFile_']:
            if v4['_Com_']:
                un.solve_compound_names_batchres(metapath, keypath, rpath, name)
            elif v4['_Strain_']:
                un.solve_strain_names_batchres(metapath, keypath, rpath, name)
            elif v4['_Both_']:
                un.solve_both_strain_and_compound_names_batchres(metapath, keypath, rpath, name)
    else:
        sg.popup('Please enter valid files')
    message_win()
    unblind.close()



def message_win():
    layout = [[sg.Text('Done!', size=(60, 1), justification='center', font=(14))], [sg.OK()]]
    window = sg.Window('Message', layout, size=(400, 60))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            break


def main():
    make_GUI()

if __name__ == '__main__':
    main()
