import PySimpleGUI as sg
import analyze_image as ai
import pathlib as plb
import unblind_key as un
import tkinter as tk
import dataviz as dv
import timepoint_add as tl
import webbrowser
import pandas as pd

sg.ChangeLookAndFeel('GreenTan')

text_style = {
    'size': (40, 1),
    'justification': 'right'
}

dv_text = {
    'size':(50, 1),
    'auto_size_text':False,
    'justification':'left'
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
ck_URL = 'https://docs.google.com/spreadsheets/d/1xdAJYOK26fsM8uFkZXIBNLxrziE9vB7q0AoK1pYCyWI/edit?usp=sharing'
tg_URL = 'https://acclab.github.io/DABEST-python-docs/_images/tutorial_27_0.png'
sc_URL = 'https://acclab.github.io/DABEST-python-docs/_images/tutorial_42_0.png'
mg_URL = 'https://acclab.github.io/DABEST-python-docs/_images/tutorial_47_0.png'
bkey_URL = ''
ttips = {
 'mdt' : 'Link to Metadata template',
 'bkt' : 'Link to Blinding Key Template'
}

### Generates the first window that the user encounters.
### Opens upon running the program
def make_win1():
    gui_input_column = [
    [sg.Combo(('Image analysis', 'Unblind data', 'Data visualization'), key = '_ddown_' ,size=(20, 1), default_value= 'Image analysis'), sg.Button('Go')],
    [sg.Exit()]]
    
    gui_text_column = [
    [sg.Text('The OWL can perform a multiple tasks that inlcude:')],
    [sg.Text('1. Analyze images from chemotaxis assays using C. elegans.')],
    [sg.Text('2. Unblind data associated with chemotaxis assays')],
    [sg.Text('3. Generate plots of bootstrapped confidence intervals.')]
    ]

    layout1 = [
    [sg.Text('Welcome to Our Worm Locator!', size=(40, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Column(gui_text_column),
    sg.VSeperator(),
    sg.Column(gui_input_column),]
    ]

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

    dv_layout = [
        [sg.Text('The OWL offers 2 different visualization options:')],
        [sg.Text('1. Two groups: Compare only two groups (Control and Test)')],
        [sg.Text('Two group example', key = 'tg_link',**link_style), sg.Button('Two groups')],
        [sg.Text('2. Shared control: Compare multiple test conditions to a single control group')],
        [sg.Text('Shared control example', key = 'sc_link',**link_style), sg.Button('Shared Control')],
        # [sg.Text('3. Multiple groups: Compare multiple controls to their respective test conditions')],
        # [sg.Text('Multiple groups example', key = 'mg_link',**link_style), sg.Button('Multiple Groups')],
        [sg.Button('Back'), sg.Button('Exit')]
        ]


    dv_hold = sg.Window('Data Viz Options', dv_layout, size=(500,300), resizable=True, finalize=True)
    return dv_hold

def dv_sharedcontrol():
    rgt = [

        
        [sg.Text('What is your independent variable?', size=(50,1), justification='left'), sg.Combo(('Compound', 'Strain'), default_value='Compound', key='_IV_sc_', enable_events=True, pad=(0,20),size=(15,1))],
        [sg.Text('Select your Image Analysis Summary file: ', size=(50,1) , justification='left', visible='False'), sg.InputText('Select file', key = '_sumfile_sc_', visible='False'), sg.FileBrowse()],
        [sg.Text('Select the folder that contains your location files: ',  size=(50,1), justification='left'), sg.InputText('Default Folder', key = '_locfile_sc_'), sg.FolderBrowse()],
        [sg.Text('What is your control condition?', justification='left',  size=(50,1)), sg.InputText('Control', key='_control_sc_')],
        [sg.Text('What type of file would you like to save your plot as?',  size=(50,1), justification='left'), sg.Combo(('PDF', 'SVG' , 'PNG'), default_value='PDF', key='_filetype_sc_', size=(8,1), enable_events=True)],
        [sg.Text('Where would you like to save your file?', justification='left', visible='False',  size=(50,1)), sg.InputText('Select folder', key = '_save_loc_sc_', visible='False'), sg.FolderBrowse()],
        [sg.Text('Give a filename to your plot:',  justification='left',  size=(50,1)), sg.InputText('Data visualisation', key='_fname_sc_')],
        [sg.Text('Select the colors you would like to use in your plot (Optional):', justification='left', size=(50,1)), sg.Button('Select Data and Colors')],
        [sg.Checkbox('Check this box if you would like to exclude data that does not pass quality control (<150 worms)',key = '_qc_', default=False)]
        ]

    sc_layout = [
        [
         sg.Column(rgt, pad=(0, None))],
        [sg.Button('Do Data Vis'), sg.Button('Home'), sg.Exit()]
    ]

    sc = sg.Window('Shared control', sc_layout, size=(900,400), resizable=True, finalize=True)
    return sc

def dv_tg():
    tg_layout = [
        [sg.Text('What is your independent variable?', **dv_text)],
        [sg.Combo(('Compound','Strain'), default_value='Compound', key='_IV_cond_', size=(15,1))],
        [sg.Text('Select your Image Analysis Summary file: ', **dv_text), sg.InputText('Select file', key = '_tg_sum_', visible='False'), sg.FileBrowse()],
        [sg.Text('Select the folder that contains your location files: ', **dv_text),sg.InputText('Default Folder', key = '_tg_loc_'), sg.FolderBrowse()],
        [sg.Text('Control condition:',**dv_text),
        sg.InputText('Control', key='_control_name_')],
        [sg.Text('Test condition:', **dv_text),
        sg.InputText('Test', key='-test_name-')],
        [sg.Button('Do Data Vis'), sg.Button('Home')], [sg.Exit()]]
    tg = sg.Window('Two group comparison', tg_layout, size=(900,250), resizable=True, finalize=True)
    return tg

# def dv_mg():
#     multigroups = [
#         [sg.Text('To plot multiple groups on one axis, fill in the fields below.', font='Lucida', justification='left')],
#         [sg.Text('* Input the list of conditions with your control as the fist item and seperate each condition by a comma', font='Lucida', justification='left')],
#         [sg.Text('Example: DMSO, isoamyl alcohol, 2-nonanone', font='Lucida', justification='left')],
#         [sg.Text('Example: N2, PR678, CX10', font='Lucida', justification='left')],
#         [sg.Text('Group 1:'), sg.InputText(key='-g1-')],
#         [sg.Text('Group 2:'), sg.InputText(key='-g2-')],
#         [sg.Text('Group 3:'), sg.InputText(key='-g3-')],
#         [sg.Text('Group 4:'), sg.InputText(key='-g4-')],
#         [sg.Text('Group 5:'), sg.InputText(key='-g5-')],
#         [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'brf_2g', visible='False'), sg.FileBrowse()],
#         [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = 'locf_2g'), sg.FolderBrowse()],
#         [sg.Text('If you prefer to select your colors, attach a colors key, otherwise leave blank:', size=(50, 2),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'col_key', visible='False'), sg.FileBrowse()],
#         [sg.Button('Do Data Vis'), sg.Button('Home')], [sg.Exit()]]
#     mg = sg.Window('Paired analysis?', multigroups, size=(900,400), resizable=True, finalize=True)
#     return mg
       
def generate_df(vs):
    df = pd.DataFrame(columns=['Condition', 'Color'])
    
    for row in range(15):
        current_row = []
        for col in range(2):
            current_row.append(vs[row, col])
        #print(current_row)
        df.loc[len(df)] = current_row
    return df

def clear_all(w):
    for row in range(15):
        for col in range(2):
            w[(row,col)].update('')


def make_ckey():

    header = [

    sg.Text('Condition', pad=(0,0), size=(15,1), justification='c'), 
    sg.Text('Color (Hex code)',  pad=(0,0), size=(15,1), justification='c')]

    layout = [header]

    for row in range(0, 15):
        current_row = [
            sg.Input(size=(15,1), pad = (0,0), key=(row,0)),
            sg.Input(size=(15,1), pad = (0,0), key=(row,1))
        ]

        layout.append(current_row)

    button_row = [sg.Button('Submit'), sg.Button('Clear')]
    layout.append(button_row)

    ck_window = sg.Window('Spreadsheet', layout)
    return ck_window

def check_control(fpath, con, val):
    cf = plb.Path(fpath)
    cfile = pd.read_csv(cf)
    cfile[con] = cfile[con].apply(str.lower) 
    tf = val in cfile[con].to_list()
    return tf

def check_colorkey(k, vals):
    colors = k.apply(lambda x: x.astype(str).str.lower())
    cols = colors.columns
    cdict = colors.set_index(cols[0])[cols[1]].to_dict()


    dfp = plb.Path(vals['_sumfile_sc_'])
    dat = pd.read_csv(dfp)
    conditions = dat[vals['_IV_sc_']].to_list()
    conditions = [str(x).lower() for x in conditions]
    tf = all(y in cdict for y in conditions)
    return tf

def check_resultfile(fpath):
    cf = plb.Path(fpath)
    cfile = pd.read_csv(cf)
    heds = cfile.columns.to_list()
    expected = ['WellNo', 'Total Worms', 'Compound', 'Strain',
       'File Name', 'Well width', 'Plate ID', 'Passes QC']
    tf = all(x in heds for x in expected)
    return tf

### This funtion initiates the GUI
def make_GUI():
    win1 = make_win1()
    while True:
        event, values = win1.read()

        
        ### If exit button is clicked then the whole program is terminated
        if event in (None, 'Exit'):
            break
        ### Opens a window to analyze a batch of images
        ### User is returned to the main page upon completion of analysis
        if (event == 'Go') and (values['_ddown_']=='Image analysis') :
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
        
            

        if (event == 'Go') and (values['_ddown_'] == 'Unblind data'):
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
            
        if (event == 'Go') and (values['_ddown_']=='Data visualization'):
            win1.hide()
            dv_win = dataviz_window()

            while True:
                e, v = dv_win.read()

                if e == sg.WIN_CLOSED or e == 'Exit':
                    dv_win.close()
                    break
                elif e == 'Back':
                    dv_win.close()
                    make_GUI()
                    break
                if e == 'tg_link':
                    webbrowser.open(tg_URL)
                if e == 'sc_link':
                    webbrowser.open(sc_URL)
                if e == 'mg_link':
                    webbrowser.open(mg_URL)
                elif e == 'Shared Control':
                    dv_win.hide()
                    shared = dv_sharedcontrol()
                    while True:
                        sc_e, sc_v = shared.read()
                        if sc_e == 'Select Data and Colors':
                            ckey_win = make_ckey()
                            while True:
                                ck_e, ck_v = ckey_win.read()
                                if ck_e in (sg.WIN_CLOSED, 'Exit'):
                                    ckey_win.close()
                                    break
                                elif ck_e == 'Submit':
                                    colorkey = generate_df(ck_v)
                                    ckey_win.close()
                                    break
                                elif ck_e == 'Clear':
                                    clear_all(ckey_win)
                                    continue
                        if sc_e == sg.WIN_CLOSED or sc_e == 'Exit':
                            shared.close()
                            dv_win.close()
                            break
                        elif sc_e == 'Home':
                            shared.close()
                            dv_win.close()
                            make_GUI()
                            break

                        elif (sc_e == 'Do Data Vis') and (plb.Path(sc_v['_sumfile_sc_']).exists()) and (plb.Path(sc_v['_locfile_sc_']).exists()) and (plb.Path(sc_v['_save_loc_sc_']).exists()):

                            control_val = sc_v['_control_sc_'].lower()
                            control_con = sc_v['_IV_sc_']
                            fp = sc_v['_sumfile_sc_']

                            if check_resultfile(fp):
                                if check_control(fp, control_con, control_val) == True:
                                    try:
                                        colorkey
                                    except NameError:
                                        var_exists = False
                                        hold = pd.DataFrame()
                                        dv.do_data_visualisation(sc_v, hold)
                                        shared.close()
                                        dv_win.close()
                                        make_GUI()
                                        break
                                    else:
                                        var_exists = True
                                        b = check_colorkey(colorkey, sc_v)

                                        if b:
                                            dv.do_data_visualisation(sc_v, colorkey)
                                            shared.close()
                                            dv_win.close()
                                            make_GUI()
                                            break
                                        else:
                                            sg.popup('There are either missing values in the color key,\nor data entry errors in the summary file')
                                else:
                                    sg.popup('Control not found in the data, please recheck column values')
                            else:
                                sg.popup('Column headers do not match expected values.\nCheck that you have input the correct files or\nSee documentation for expected headers')
                elif e == 'Two groups':
                    dv_win.hide()
                    two_groups = dv_tg()
                    while True:
                        tg_e, tg_v = two_groups.read()
                        if tg_e == sg.WIN_CLOSED or tg_e == 'Exit':
                            two_groups.close()
                            dv_win.close()
                            break
                        elif tg_e == 'Home':
                            two_groups.close()
                            dv_win.close()
                            make_GUI()
                            break
                        elif (tg_e == 'Do Data Vis') and (plb.Path(tg_v['_tg_sum_']).exists()) and (plb.Path(tg_v['_tg_loc_']).exists()):
                            control_val = tg_v['_control_name_'].lower()
                            control_con = tg_v['_IV_cond_']
                            fp = tg_v['_tg_sum_']

                            if check_resultfile(fp):
                                if (check_control(fp, control_con, control_val) == True) & (check_control(fp, control_con ,tg_v['-test_name-']) == True):
                                    dv.do_dv_tg(tg_v)
                                    two_groups.close()
                                    dv_win.close()
                                    make_GUI()
                                    break
                                        
                                else:
                                    sg.popup('Values not found in the data, please recheck column values')
                            else:
                                sg.popup('Column headers do not match expected values.\nCheck that you have input the correct files or\nSee documentation for expected headers')

                # elif e == 'Multiple Groups':
                #     dv_win.hide()
                #     multi_groups = dv_mg()
                #     while True:
                #         mg_e, mg_v = multi_groups.read()
                #         print(mg_v)
                #         if mg_e == sg.WIN_CLOSED or mg_e == 'Exit':
                #             multi_groups.close()
                #             dv_win.close()
                #             break
                #         elif mg_e == 'Home':
                #             multi_groups.close()
                #             dv_win.close()
                #             make_GUI()
                #             break
                #         elif (mg_e == 'Do Data Vis') and (plb.Path(mg_v['_mg_sum_']).exists()) and (plb.Path(mg_v['_mg_loc_']).exists()):
                #             dv.do_dv_mg(mg_v)
                #             multi_groups.close()
                #             dv_win.close()
                #             make_GUI()
                #             break
            dv_win.close()
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
