
# -*- coding: utf-8 -*-

import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')      


# ------ Column Definition ------ #      


layout = [          
    [sg.Text('Welcome to the Worm Counter!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],    
    [sg.Text('Choose whether you would like to process a single image or all images from a batch')],     
    [sg.Frame(layout=[            
    [sg.Radio('Single Image', "RADIO1", default=True, size=(15,1), key='_SINGLE_', enable_events=True), sg.Radio('Batch', "RADIO1", key='_BATCH_', enable_events=True)]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],     
    [sg.Text('_'  * 120)],
    
    [sg.Frame('Single Pic', key = '_test_', visible = False, layout=[
    
    [sg.Frame('Worm Strains in Each Well', visible = True, layout=[
    [sg.Text('Strain in Well P'), sg.InputText()],
    [sg.Text('Strain in Well Q'), sg.InputText()],
    [sg.Text('Strain in Well R'), sg.InputText()],
    [sg.Text('Strain in Well S'), sg.InputText()]])],
    
    [sg.Frame('Slot 1 Data', visible = True, layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]]
    ),
    sg.Frame('Slot 2 Data',visible = True,  layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]
    ])],

    [sg.Frame('Slot 3 Data',visible = True, layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]]
    ),
    sg.Frame('Slot 4 Data',visible = True,  layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]
    ])],

    [sg.Frame('Choose the image file to be analyzed', visible=True, layout=[     
    [sg.Text('Your File', size=(15, 1), auto_size_text=False, justification='right'),      
        sg.InputText('Default Folder'), sg.FileBrowse()],      
            ])]])],
    
    [sg.Frame('Connecting file paths to the code', key='_Folder_', visible=False, layout = [ 
    [sg.Text('Choose A Folder', size=(35, 1))],      
    [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),      
        sg.InputText('Default Folder'), sg.FolderBrowse()],      
    [sg.Submit(tooltip='Click to submit this window')] ])  ],
    [sg.Exit()]]


window1 = sg.Window('Worm Counter', layout, default_element_size=(40, 1), grab_anywhere=False, keep_on_top=False)      



while True:  # Event Loop            
    event, values = window1.read()
    print(event, values)      
    if event in (None, 'Exit'):
        break
    if values['_SINGLE_']:
        window1.Element('_test_').Update(visible = True)
        window1.Element('_Folder_').Update(visible = False)
    if values['_BATCH_']:
        window1.Element('_test_').Update(visible = False)
        window1.Element('_Folder_').Update(visible=True)
        for event in range(14):
            window1.FindElement(event).Update('')
        
        


window1.close()    