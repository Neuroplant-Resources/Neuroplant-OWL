import PySimpleGUI as sg
import analyze_image as ai
import pathlib as plb
sg.ChangeLookAndFeel('GreenTan') 

### Generates the first window that the user encounters.
### Opens upon running the program
def make_win1():
	layout1 = [          
	[sg.Text('Welcome to the Worm Counter!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],    
	[sg.Text('Choose whether you would like to process a single image or a batch of images')],     
	[sg.Frame(layout=[            
	[sg.Radio('Single Image', "RADIO1", default=True, size=(15,1), key='_SINGLE_', enable_events=True), sg.Radio('Batch', "RADIO1", key='_BATCH_', enable_events=True)]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],     
	[sg.Text('_'  * 120)], [sg.Exit()]]

	window1 = sg.Window('Worm Counter', layout1, default_element_size=(40, 1))
	return window1

### Makes the window to process multiple images
def make_batch_win():
	layout2 = [      
	[sg.Text('Select a folder to store your results: ', size=(65, 1), auto_size_text=False, justification='right'),sg.InputText('Default Folder', key = '-results_folder-'), sg.FolderBrowse()],      
	[sg.Text('Select the folder that contains the images to be analyzed: ',  size=(65, 1), auto_size_text=False, justification='right'),sg.InputText('Default Folder', key='-image_folder-',), sg.FolderBrowse()],
	#[sg.Text('Choose the metadata file associated with this batch of images: ', size=(65, 1), auto_size_text=False, justification='right'), sg.Input(), sg.FileBrowse()],
	[sg.Button('Analyze')],
	[sg.Button('Back')],
	[sg.Exit()]]

	batch_window = sg.Window('Batch Image Counter', layout2, default_element_size=(80, 1))
	return batch_window


### Creates the GUI window to process one image at a time
def make_single_win():
	layout3 = [
	[sg.Frame('Single Pic', key = '_test_', layout=[

	[sg.Frame('Worm Strains in Each Well', visible = False, key='-4Strains-', layout=[
	[sg.Text('Strain in Well P', size=(15,1)), sg.InputText(key='-StrainP-')],
	[sg.Text('Strain in Well Q', size=(15,1)), sg.InputText(key='-StrainQ-')],
	[sg.Text('Strain in Well R', size=(15,1)), sg.InputText(key='-StrainR-')],
	[sg.Text('Strain in Well S', size=(15,1)), sg.InputText(key='-StrainS-')]])],

	[sg.Frame('Slot 1 Data', visible = True,layout=[
	#[sg.Checkbox('Check this box if you there are multiple strains on this plate', enable_events=True ,key='-show_strains-', size=(10,1))],
	[sg.Text('Plate ID', size=(15,1)), sg.InputText(key='-PID1-')],
	[sg.Text('Strain on Plate 1', size=(15,1)), sg.InputText(key='-Strain1-')],
	[sg.Text('Compound', size=(15,1)), sg.InputText(key='-Compound1-')]]
	),
	sg.Frame('Slot 2 Data',visible = True,  layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText(key='-PID2-')],
	[sg.Text('Strain on Plate 2', size=(15,1)), sg.InputText(key='-Strain2-')],
	[sg.Text('Compound', size=(15,1)), sg.InputText(key='-Compound2-')]
	])],

	[sg.Frame('Slot 3 Data',visible = True, layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText(key='-PID3-')],
	[sg.Text('Strain on Plate 3', size=(15,1)), sg.InputText(key='-Strain3-')],
	[sg.Text('Compound', size=(15,1)), sg.InputText(key='-Compound3-')]]
	),
	sg.Frame('Slot 4 Data',visible = True,  layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText(key='-PID4-')],
	[sg.Text('Strain on Plate 4', size=(15,1)), sg.InputText(key='-Strain4-')],
	[sg.Text('Compound', size=(15,1)), sg.InputText(key='-Compound4-')]
	])],

	[sg.Frame('Choose the image file to be analyzed', visible=True, layout=[  
	[sg.Text('Choose a folder to save your results in: ', size=(40, 1), auto_size_text=False, justification='right'),      
	    sg.InputText('Results folder', key='-results-'), sg.FolderBrowse()], 
	[sg.Text('Select the image to be analyzed', size=(40, 1), auto_size_text=False, justification='right'),      
	    sg.InputText('Image file', key='-file-'), sg.FileBrowse(),sg.Button('Analyze'), sg.Button('Back'), sg.Exit(),]])]
	])]]

	single_im = sg.Window('Single Image Processing', layout3, size=(900,400))
	return single_im

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
					rpath = (v2['-results_folder-'])
					fpath = (v2['-image_folder-'])
					im_path = plb.Path(fpath)
					res_path = plb.Path(rpath)
					if im_path.exists() and res_path.exists():
						ai.batch_process(fpath, rpath, v2, e2)
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
	win1.close()

def main():
	make_GUI()

if __name__ == '__main__':
    main()