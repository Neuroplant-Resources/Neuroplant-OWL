import PySimpleGUI as sg
import analyze_image as ai
import pathlib as plb
import unblind_key as un
import tkinter as tk
import dataviz as dv
import timepoint_add as tl
import colors_key as ck
import webbrowser

sg.ChangeLookAndFeel('GreenTan')

text_style = {
    'size': (40, 1),
    'justification': 'right'
}
box_style = {
    'size': (25, 1)
}

link_style = {
    'text_color' : 'blue',
    'enable_events' : True
}

RM_URL = 'https://github.com/wormsenseLab/Neuroplant-OWL'
MD_URL = 'https://docs.google.com/spreadsheets/d/1u8PN5a5s7SFurxspXNJSq5FKKNKTdzFmCgwjjsEf4XE/edit?usp=sharing'
bkey_URL = ''
ttips = {
 'mdt' : 'Link to Metadata template',
 'bkt' : 'Link to Blinding Key Template'
}

### Generates the first window that the user encounters.
### Opens upon running the program
def make_win1():
    layout1 = [
    [sg.Text('Welcome to Our Worm Locator!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Combo(('Image analysis', 'Unblind data', 'Data visualization', 'Timelapse'), size=(20, 1), default_value= 'Image analysis'), sg.Button('Go')],
    [sg.Text('Would you like to perform data visualization?', font=(14))],
    [sg.Frame(layout=[[sg.Radio('Yes, two group estimation plot', 'RADIO1', default=False, size=(50,1), key='_DataVizTwoGroup_', enable_events=True, font=(14))], [sg.Radio('Yes,  shared control estimation plot', 'RADIO1', key='_DataVizSharedControl_', enable_events=True, font=(14))],
     [sg.Radio('Yes, multi 2 group estimation plot', 'RADIO1', key='_DataVizMultiTwo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
#    [sg.Text('If you have timelapse scans, would you like to add time points collumn to your batch results file?',size=(100,1), font='Lucida', justification='left')], [sg.Radio('Yes', 'RADIO1', default=False, key='_TimeLapseCollumn_', enable_events=True, font=(14))],
    [sg.Exit()]]



    window1 = sg.Window('Worm Counter', layout1, default_element_size=(60, 2), resizable=True, finalize=True)
    return window1

### Makes the window to process multiple images


def make_batch_win():

    ia_inupt_column = [
    [sg.Text('Folder containing images to analyze: ',  **text_style),sg.In(**box_style, enable_events=True, key='-image_folder-',), sg.FolderBrowse()],
    [sg.Text('Metadata file (Optional): ', **text_style), sg.In(**box_style, key = 'md_file'), sg.FileBrowse(),],
    [sg.Text('Select a folder to store your results: ', **text_style),sg.In(**box_style, key = '-results_folder-'), sg.FolderBrowse()],
    [sg.Text('Name your summary file: ', **text_style),
    sg.In( **box_style, key='-name-') ],
    [sg.Button('Analyze'), sg.Button('Back'), sg.Exit()]]

    ia_text_column = [
    [sg.Text('1. The OWL will process ALL images contained in a single folder.')],
    [sg.Text('2. Inputing a metadata sheet will allow you to connect experimental\nconditions to the corresponding wells of an image.')],
    [sg.Text('Link to download the accepted Metadata Template', key='_mdTemplate_', tooltip=ttips['mdt'], **link_style)],
    [sg.Text('3. The OWL will return the results as .csv files to the folder specified.')],
    [sg.Text('4. The returned results will include multiple files containing the location\ndata for each well and a summary file.')],
    [sg.Text('Link to Documentation', key='_README_', tooltip=RM_URL, **link_style),]
    ]



    img_analysis_layout = [
    [sg.Column(ia_text_column),
    sg.VSeperator(),
    sg.Column(ia_inupt_column),]
    ]

    batch_window = sg.Window('OWL', img_analysis_layout, default_element_size=(80, 1), resizable=True, finalize=True)
    return batch_window




def unblind_window():

    ub_inupt_column = [
    [sg.Text('Select the type of file you would like to unblind:',size=(100,1), font='Lucida')],
    [sg.Combo(('Metadata sheet', 'Image analysis summary'), key = '_data_2UB_', default_value='Metadata sheet', size=(20, 1))],
    [sg.Text('What test condition would you like to unblind?',size=(100,1), font='Lucida')],
    [sg.Combo(('Strain name', 'Test compound'), key='_conditions_', default_value = 'Strain name', size=(20, 1))],
    [sg.Text('Select the file you would like to unblind: ', size=(50, 1),font=(12) ,auto_size_text=False, visible='False')], [sg.InputText('Select file', key = '_to_unblind_', visible='False'), sg.FileBrowse()],
    [sg.Text('Select your blinding key: ', size=(50, 1),font=(12) ,auto_size_text=False, visible='False')], [sg.InputText('Select file', key = 'key_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select a folder to store your results: ', size=(50, 1),font=(12) ,auto_size_text=False)], [sg.InputText('Select folder', key = '-results_folder-'), sg.FolderBrowse()],
    [sg.Text('Name your unblinded data sheet:', size=(50, 1), auto_size_text=False, font=(12))], [sg.InputText('Unblinded Metadata', key='-metadata_name-')],
    [sg.Button('Unblind'), sg.Button('Back'), sg.Exit()]]

    ub_text_column = [
    [sg.Text('1. You can choose to unblind a metadata sheet or a summary file\nreturned from image analysis.')],
    [sg.Text('2. Unblinding will only work if you are using the metadata, the returned\nsummary file from image analysis or the blinding key templates')],
    [sg.Text('Metadata Template', key='_mdTemplate_', tooltip=ttips['mdt'], **link_style), sg.Text('Blinding Key Template', key='_bkey_temp_', tooltip=ttips['bkt'], **link_style)],
    [sg.Text('3. Check that your blinded data is consistent. Errors in data entry\nmay result in incomplete unmasking of blinded datasets')],
    [sg.Text('Link to blinding documentation for troubleshooting:', key='_README_', tooltip=RM_URL, **link_style),]
    ]
    
    unblinding_layout = [
    [sg.Column(ub_text_column, element_justification='left' ),
    sg.VSeperator(),
    sg.Column(ub_inupt_column, element_justification='left')]
    ]

    u_win = sg.Window('Unmasking data', unblinding_layout, size=(900,450), resizable=True, finalize=True)
    return u_win
    


def shared_control_window():
    layout5 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14)), sg.Radio('Time Lapse', 'RADIO2', key='_TimeLapse_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('_'  * 120)],
    [sg.Text('If you would like to restrict the variable you are not plotting, please make selections, otherwise click "None".')],
    [sg.Text('What type of variable would you like to restrict the independent variable under?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('None', 'RADIO3', default=False, key='_none_select_', enable_events=True, font=(14)), sg.Radio('Compound', 'RADIO3', key='_compound_select_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO3', key='_strain_select_', enable_events=True, font=(14)), sg.Radio('Both', 'RADIO3', default=False, key='_both_select_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select the compound you want to restrict under:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('restricting compound', key='-compound-select-name-')],
    [sg.Text('Select the strain you want to restrict under:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('restricting strain', key='-strain-select-name-')],
    [sg.Text('_'  * 120)],
    [sg.Text('Would you like to select your colors?'), sg.Radio('Yes',  'RADIO4', default=False, key='yes_for_col_key', enable_events=True), sg.Radio('No', 'RADIO4', default=False, key='no_for_col_key', enable_events=True), sg.Text('If yes, please attach a colors key:', justification='left'), sg.InputText('Select file', key = 'col_key', justification='left', visible='False'), sg.FileBrowse()],
    [sg.Text('_'  * 120)],
    [sg.Text('Would you like to save your plot as a pdf file?', font=(9)), sg.Radio('Yes',  'RADIO5', default=False, key='yes_for_saving_pdf', enable_events=True), sg.Radio('No', 'RADIO5', default=False, key='no_for_saving_pdf', enable_events=True)], [sg.Text('If yes, select the folder in which you want to save your plot as a pdf file:', justification='left', visible='False', size=(50, 1), font=(9)),  sg.InputText('Select file', key = 'pdf_key', visible='False'), sg.FolderBrowse()],
    [sg.Text('If yes, please input a name for the pdf file:', auto_size_text=False, justification='left', size=(50, 1), font=(9)),
    sg.InputText('Data visualisation', key='-pdf_name_plot-')],
    [sg.Text(' '  * 120)],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_options_win = sg.Window('Data Visualization Options', layout5, size=(900,600), resizable=True, finalize=True)
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

    
def dataviz_multitwo_window():
    layout7 = [
    [sg.Text('What is your reference condition?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('compound (I used 2 kinds of compounds)', 'RADIO2', default=False, key='_CompoundReference_', enable_events=True, font=(14)), sg.Radio('strains (I used 2 kinds of strains)', 'RADIO2', key='_StrainReference_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('What are the 2 reference condition types?', size=(30, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Reference 1', key='-ref1-'), sg.InputText('Reference 2', key='-ref2-')],
    [sg.Text('What factor do you want to compare?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('compound ', 'RADIO3', default=False, key='_CompoundComparison_', enable_events=True, font=(14)), sg.Radio('strain ', 'RADIO3', key='_StrainComparison_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('What is the name of your control variable in your comparison factor?', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('If you prefer to select your colors, attach a colors key, otherwise leave blank:', size=(50, 2),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'col_key', visible='False'), sg.FileBrowse()],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,400), resizable=True, finalize=True)
    return dataviz_multitwo_win
   
# def timelapse_window():
#     layout4 = [
#     [sg.Text('If you have time lapse analysis, you may add a time point collumn to your batch results file by using the time lapse key template that matches the file name to the time point',size=(120,1), font='Lucida', justification='left')],
#     [sg.Text('Select your batch results file that you would like the time points collumn to be added to: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'filefortimelapse_', visible='False'), sg.FileBrowse()],
#     [sg.Text('Select your time lapse key: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'timelapsekey_', visible='False'), sg.FileBrowse()],
#     [sg.Text('Select a folder to store the new file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-tl_folder-'), sg.FolderBrowse()],
#      [sg.Text('Name your file with the time points collumn:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
#     sg.InputText('File with Time Points', key='-filenamewithtimelapse-')],
#     [sg.Text('_'  * 140)],
#         [sg.Button('Add TimePoints'), sg.Button('Back')], [sg.Exit()]]
    
#     tl_win = sg.Window('Time Lapse Analysis Collumn', layout4, size=(900,250), resizable=True, finalize=True)
#     return tl_win

def dataviz_window():     
    sharedcontrol = [
        [sg.Text('Shared control plot', justification='center', key='_shared_control_')],
        [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Combo(('Compound', 'Strain', 'Time lapse'), default_value='Compound', key='_IV_sc_', enable_events=True)],
        [sg.Text('Select your Image Analysis Summary file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = '_sumfile_sc_', visible='False'), sg.FileBrowse()],
        [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '_locfile_sc_'), sg.FolderBrowse()],
        [sg.Text('What is your control condition?', size=(50, 1), auto_size_text=False, justification='left', font=(12)), sg.InputText('Control', key='_control_sc_')],
        [sg.Text('Would type of file would you like to save your plot as?', font=(9)), sg.Combo(('PDF', 'SVG' , 'PNG'), default_value='PDF', key='_filetype_sc_', enable_events=True)],
        [sg.Text('Where would you like to save your file?', justification='left', visible='False', size=(50, 1), font=(9)),  sg.InputText('Select folder', key = '_save_loc_sc_', visible='False'), sg.FolderBrowse()],
        [sg.Text('File name:', auto_size_text=False, justification='left', size=(50, 1), font=(9)),
        sg.InputText('Data visualisation', key='_fname_sc_')],
        [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
        
        #dataviz_options_win = sg.Window('Data Visualization Options', layout1, size=(900,600), resizable=True, finalize=True)
        #return dataviz_options_win

    multigroups = [
        [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Combo(('Compound','Strain'), default_value='Compound', key='_IV_comp_')],
        [sg.Text('Select your Image Analysis Summary file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
        [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
        [sg.Text('Control condition:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
        sg.InputText('Control', key='-control_name-')],
        [sg.Text('Test condition:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
        sg.InputText('Test', key='-test_name-')],
        [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
        #dataviz_twogroup_win = sg.Window('Data Visualization Options', layout6, size=(900,250), resizable=True, finalize=True)
        #return dataviz_twogroup_win

    twogroups = [
        [sg.Text('What is your reference condition?',size=(100,1), font='Lucida', justification='left')],
        [sg.Combo(('Compound','Strain'), default_value='Compound', key='_Reference_', enable_events=True)],
        [sg.Text('What are the 2 reference condition types?', size=(30, 1), auto_size_text=False, justification='left', font=(12)),
        sg.InputText('Reference 1', key='-ref1-'), sg.InputText('Reference 2', key='-ref2-')],
        [sg.Text('What factor do you want to compare?',size=(100,1), font='Lucida', justification='left')],
        [sg.Combo(('Compound ', 'Strain'), default_value='Compound', key='_Comparison_', enable_events=True)],
        [sg.Text('What is the name of your control variable in your comparison factor?', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
        sg.InputText('Control', key='-control_name-')],
        [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
        [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
        [sg.Text('If you prefer to select your colors, attach a colors key, otherwise leave blank:', size=(50, 2),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'col_key', visible='False'), sg.FileBrowse()],
        [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
        #dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,400), resizable=True, finalize=True)
        #return dataviz_multitwo_win
       

    # ----------- Create actual layout using Columns and a row of Buttons
    dv_layout = [[sg.Button('Shared Control'), sg.Button('Multi'), sg.Button('Two Groups')],
    [sg.Column(sharedcontrol, key='-Shared Control-'), sg.Column(multigroups, visible=False, key='-Multi-'), sg.Column(twogroups, visible=False, key='-Two Groups-')]]

    dv_window = sg.Window('Data visualization', dv_layout)
    dv_layout = 'Shared Control'  # The currently visible layout

    while True:
        event, values = dv_window.read()
        #print(event, values)
        if event in (None, 'Exit'):
            break
        if event == 'Back':
            break

        if event in ['Shared Control', 'Multi', 'Two Groups']:
            dv_window[f'-{dv_layout}-'].update(visible=False)
            dv_layout = event       
            dv_window[f'-{dv_layout}-'].update(visible=True)
        if event == 'Do Data Vis' and dv_layout == 'Shared Control':
            dv.do_data_visualisation_strain(values)
        #if event == 'Do Data Vis' and dv_layout == 'Multi':
        #if event == 'Do Data Vis' and dv_layout == 'Two Groups':
                

    return dv_window, event, values

def check_fpaths(ipath, rpath):
        return True


### This funtion initiates the GUI
def make_GUI():
    win1 = make_win1()
    while True:
        event, values = win1.read()
        #print(values)
        
        ### If exit button is clicked then the whole program is terminated
        if event in (None, 'Exit'):
            break
        ### Opens a window to analyze a batch of images
        ### User is returned to the main page upon completion of analysis
        if (event == 'Go') and (values[0]=='Image analysis') :
            win1.hide()
            batch_win = make_batch_win()
            while True:
                e2, v2 = batch_win.read()
                if e2 in (None, 'Exit'):
                    batch_win.close()
                    break
                if e2 == '_README_':
                    webbrowser.open(RM_URL)
                if e2 == '_mdTemplate_':
                    webbrowser.open(MD_URL)
                if e2 == 'Analyze':
                    mdpath = (v2['md_file'])
                    rpath = (v2['-results_folder-'])
                    fpath = (v2['-image_folder-'])
                    results_name = (v2['-name-'])

                    im_path = plb.Path(fpath)
                    res_path = plb.Path(rpath)
                    
                    if im_path.exists() and res_path.exists() and (len(rpath) != 0) and (len(fpath) !=0 ) and (len(results_name) != 0):

                        ai.batch_process(im_path, res_path, mdpath, v2, e2, results_name)
                        batch_win.close()
                        make_GUI()
                        break
                    else:
                        sg.popup('Please enter a valid file name or folder path')
                if e2 == 'Back':
                    batch_win.close()
                    make_GUI()
                    break
            batch_win.close()
            break
        
            

        if (event == 'Go') and (values[0] == 'Unblind data'):
            win1.hide()
            unblind = unblind_window()
            while True:
                e4, v4 = unblind.read()
                if e4 == '_README_':
                    webbrowser.open(RM_URL)
                if e4 == '_mdTemplate_':
                    webbrowser.open(MD_URL)
                if e4 == '_bkey_temp_':
                    webbrowser.open(bkey_URL)
                if e4 == 'Back':
                    unblind.close()
                    make_GUI()
                    break
                if e4 in (None, 'Exit'):
                    break
                if e4 == 'Unblind':
                    if plb.Path(v4['_to_unblind_']).exists() and plb.Path(v4['key_file']).exists() and plb.Path(v4['-results_folder-']).exists():
                        un.unblind(v4)
                        unblind.close()
                        make_GUI()
                        break
                    else: sg.popup('Please enter a valid file or folder path')
            unblind.close()
            break
            
        if (event == 'Go') and (values[0]=='Data visualization'):
            win1.hide()
            dv_win, e, v = dataviz_window()
            if e == sg.WIN_CLOSED or e == 'Exit':
                print(e)
                dv_win.close()
                break
            elif e == 'Back':
                dv_win.close()
                make_GUI()
                break
            #elif e == ''
            #dv_win.close()


        if values['_DataVizSharedControl_']:
            win1.hide()
            dataviz_options = shared_control_window()
            while True:
                e5, v5 = dataviz_options.read()
                if e5 == 'Back':
                    dataviz_options.close()
                    make_GUI()
                    break
                if e5 == sg.WIN_CLOSED or e5 == 'Exit':
                    dataviz_options.close()
                    break
                if e5 == 'Do Data Vis':
                    batch_res = v5['batch_results_file']
                    loc_files_folder = v5['-location_files_folder-']
                    control_name = v5['-control_name-']
                    if v5['yes_for_saving_pdf']:
                        pdf_store_folder = v5['pdf_key']
                    else:
                        pdf_store_folder = 'Select file'
                    pdf_file_name = v5['-pdf_name_plot-']
                    if v5['yes_for_col_key']:
                        colors_key = v5['col_key']
                    else:
                        colors_key = 'None'
                    if v5['_none_select_']:
                        if colors_key != 'None':
                            colors = ck.dict_color_key(colors_key)
                        else:
                            colors = 'Select file'
                        if v5['_CompoundInfo_']:
                            dv.do_data_visualisation_compound(batch_res, loc_files_folder, control_name, colors, pdf_store_folder, pdf_file_name)
                        elif v5['_StrainInfo_']:
                            dv.do_data_visualisation_strain(batch_res, loc_files_folder, control_name, colors, pdf_store_folder, pdf_file_name)
                        elif v5['_TimeLapse_']:
                            dv.do_data_visualisation_timelapse(batch_res, loc_files_folder, control_name, colors, pdf_store_folder, pdf_file_name)
                    if colors_key != 'None':
                        colors = ck.dict_color_key_mutli2(colors_key)
                    else:
                        colors = 'Select file'
                    if v5['_StrainInfo_'] and v5['_compound_select_']:
                        selected_compound = v5['-compound-select-name-']
                        dv.data_viz_for_strain_under_1_compound(batch_res, loc_files_folder, control_name, selected_compound, colors, pdf_store_folder, pdf_file_name)
                    if v5['_CompoundInfo_'] and v5['_strain_select_']:
                        selected_strain = v5['-strain-select-name-']
                        dv.data_viz_for_compound_under_1_strain(batch_res, loc_files_folder, control_name, selected_strain, colors, pdf_store_folder, pdf_file_name)
                    if v5['_TimeLapse_'] and v5['_compound_select_']:
                        selected_compound = v5['-compound-select-name-']
                        dv.do_data_visualisation_timelapse_under_1compound(batch_res, loc_files_folder, control_name, selected_compound, colors, pdf_store_folder, pdf_file_name)
                    if v5['_TimeLapse_'] and v5['_strain_select_']:
                        selected_strain = v5['-strain-select-name-']
                        dv.do_data_visualisation_timelapse_under_1strain(batch_res, loc_files_folder, control_name, selected_strain, colors, pdf_store_folder, pdf_file_name)
                    if v5['_TimeLapse_'] and v5['_both_select_']:
                        selected_compound = v5['-compound-select-name-']
                        selected_strain = v5['-strain-select-name-']
                        dv.do_data_visualisation_timelapse_under_1compound_and_1strain(batch_res, loc_files_folder, control_name, selected_compound, selected_strain, colors, pdf_store_folder, pdf_file_name)
            dataviz_options.close()
            break
                    
                        
                        
        
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
            dataviz_twogroup.close()
            break
                    
                        
        if values['_DataVizMultiTwo_']:
            win1.hide()
            dataviz_multitwo = dataviz_multitwo_window()
            while True:
                e7, v7 = dataviz_multitwo.read()
                if e7 == 'Back':
                    dataviz_multitwo.close()
                    make_GUI()
                    break
                if e7 == sg.WIN_CLOSED or e7 == 'Exit':
                    break
                if v7['_CompoundReference_'] or v7['_StrainComparison_']:
                    v7['_StrainComparison_'] = True
                    v7['_CompoundReference_'] = True
                    
                if v7['_StrainReference_'] or v7['_CompoundComparison_']:
                    v7['_CompoundComparison_'] = True
                    v7['_StrainReference_'] = True
                
                if e7 == 'Do Data Vis':
                    batch_res = v7['batch_results_file']
                    loc_files_folder = v7['-location_files_folder-']
                    reference_1 = v7['-ref1-']
                    reference_2 = v7['-ref2-']
                    colors_key = v7['col_key']
                    control_variable = v7['-control_name-']
                    if colors_key != 'Select file':
                        colors_key = ck.dict_color_key_mutli2(colors_key)
                    if v7['_CompoundReference_'] and v7['_StrainComparison_']:
                        dv.multi2group_dataviz_1(batch_res, loc_files_folder, control_variable, reference_1, reference_2, colors_key)
                    elif v7['_StrainReference_'] and v7['_CompoundComparison_']:
                        dv.multi2group_dataviz_2(batch_res, loc_files_folder, control_variable, reference_1, reference_2, colors_key)
            dataviz_multitwo.close()
            break
        
        # if values['_TimeLapseCollumn_']:
        #     win1.hide()
        #     tl_window = timelapse_window()
        #     while True:
        #         e8, v8 = tl_window.read()
        #         if e8 == 'Back':
        #             tl_window.hide()
        #             make_GUI()
        #         if e8 in ('Exit', None):
        #             break
        #         if e8 == 'Add TimePoints':
        #             file = v8['filefortimelapse_']
        #             key = v8['timelapsekey_']
        #             name = v8['-filenamewithtimelapse-']
        #             folder = v8['-tl_folder-']
        #             tl.timelapse_collumn_addition(file, key, folder, name)
        #             message_win()
        #             tl_window.close()

                    
                    
                    
    win1.close()
   

 

def message_win():
    layout = [[sg.Text('Done!', size=(60, 1), justification='center', font=(14))], [sg.OK()]]
    window = sg.Window('Message', layout, size=(400, 60))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            window.close()
            break
        break

def main():
    make_GUI()

if __name__ == '__main__':
    main()
