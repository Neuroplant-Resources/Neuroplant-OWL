import PySimpleGUI as sg

layout2 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
    [sg.Combo(('Compound', 'Strain', 'Time lapse'), default_value='Compound', key='_IV_2_', enable_events=True)],
    [sg.Text('Select your Image Analysis Summary file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('What is your control condition?', size=(50, 1), auto_size_text=False, justification='left', font=(12)), sg.InputText('Control', key='-control_name-')],
    [sg.Text('Would you like to save your plot as a PDF ors SVG file?', font=(9)), sg.Combo(('PDF', 'SVG' , 'PNG'), default_value='PDF', key='_filetype_', enable_events=True)],
    [sg.Text('Where would you like to save your file?', justification='left', visible='False', size=(50, 1), font=(9)),  sg.InputText('Select file', key = 'pdf_key', visible='False'), sg.FolderBrowse()],
    [sg.Text('If yes, please input a name for the pdf file:', auto_size_text=False, justification='left', size=(50, 1), font=(9)),
    sg.InputText('Data visualisation', key='-pdf_name_plot-')],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    
    #dataviz_options_win = sg.Window('Data Visualization Options', layout1, size=(900,600), resizable=True, finalize=True)
    #return dataviz_options_win

layout1 = [
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

layout3 = [
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
layout = [[sg.Button('Shared Control'), sg.Button('Multi'), sg.Button('Two Groups')],
[sg.Column(layout1, key='-Shared Control-'), sg.Column(layout2, visible=False, key='-Multi-'), sg.Column(layout3, visible=False, key='-Two Groups-')]]

window = sg.Window('Swapping the contents of a window', layout)

layout = 'Shared Control'  # The currently visible layout
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event in ['Shared Control', 'Multi', 'Two Groups']:
        window[f'-{layout}-'].update(visible=False)
        layout = event
        print(layout)
        window[f'-{layout}-'].update(visible=True)
window.close()
