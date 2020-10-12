import PySimpleGUI as sg


sg.ChangeLookAndFeel('GreenTan') 

def make_win1():
	window1 = sg.Window('Worm Counter', layout, default_element_size=(40, 1), grab_anywhere=False, keep_on_top=False)      

	layout = [          
    [sg.Text('Welcome to the Worm Counter!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],    
    [sg.Text('Choose whether you would like to process a single image or all images from a batch')],     
    [sg.Frame(layout=[            
    [sg.Radio('Single Image', "RADIO1", default=True, size=(15,1), key='_SINGLE_', enable_events=True), sg.Radio('Batch', "RADIO1", key='_BATCH_', enable_events=True)]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],     
    [sg.Text('_'  * 120)]]


def get_batch_imgs():

    

def main():

	win1 = make_win1()
	while True:  # Event Loop            
    	event, values = window1.read()
    	print(event, values)      
	    if event in (None, 'Exit'):
	        break
	    if values['_SINGLE_']:
	        window1.Element('_test_').Update(visible = True)
	        window1.Element('_Folder_').Update(visible = False)
	    if values['_BATCH_']:
	        #window1.Element('_test_').Update(visible = False)
	        window1.Element('_Folder_').Update(visible=True)
	        #for event in range(14):
	        #    window1.FindElement(event).Update('')