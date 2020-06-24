# -*- coding: utf-8 -*-

import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')      


# ------ Column Definition ------ #      


layout = [          
    [sg.Text('Welcome to the Worm Counter!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],    
    [sg.Text('Choose whether you would like to process a single image or all images from a batch')],     
    [sg.Frame(layout=[            
    [sg.Radio('Single Image', "RADIO1", default=True, size=(15,1)), sg.Radio('Batch', "RADIO1")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],     
    [sg.Text('_'  * 120)],
    
    [sg.Frame('Worm Strains in Each Well', layout=[
    [sg.Text('Strain in Well P'), sg.InputText()],
    [sg.Text('Strain in Well Q'), sg.InputText()],
    [sg.Text('Strain in Well R'), sg.InputText()],
    [sg.Text('Strain in Well S'), sg.InputText()]])],
    
    [sg.Frame('Slot 1 Data',layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]]
    ),
    sg.Frame('Slot 2 Data', layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]
    ])],

    [sg.Frame('Slot 3 Data',layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]]
    ),
    sg.Frame('Slot 4 Data', layout=[
    [sg.Text('Plate ID'), sg.InputText()],
    [sg.Text('Compound'), sg.InputText()]
    ])],
    

    [sg.Text('Choose A Folder', size=(35, 1))],      
    [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),      
        sg.InputText('Default Folder'), sg.FolderBrowse()],      
    [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()]   ] 
     


window1 = sg.Window('Worm Counter', layout, default_element_size=(40, 1), grab_anywhere=False, keep_on_top=True)      

event, values = window1.read()      

window1.close()    

sg.popup('Title',      
            'The results of the window.',      
            'The button clicked was "{}"'.format(event),      
            'The values are', values)      
