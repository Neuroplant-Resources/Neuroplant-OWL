import PySimpleGUI as sg
import analyze_image as ai

sg.ChangeLookAndFeel('GreenTan') 


def make_win1():
	layout1 = [          
	[sg.Text('Welcome to the Worm Counter!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],    
	[sg.Text('Choose whether you would like to process a single image or all images from a batch')],     
	[sg.Frame(layout=[            
	[sg.Radio('Single Image', "RADIO1", default=True, size=(15,1), key='_SINGLE_', enable_events=True), sg.Radio('Batch', "RADIO1", key='_BATCH_', enable_events=True)]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],     
	[sg.Text('_'  * 120)]]

	window1 = sg.Window('Worm Counter', layout1, default_element_size=(40, 1))
	return window1

def make_batch_win():
	layout2 = [      
	[sg.Text('Choose a folder to store your results: ', size=(65, 1), auto_size_text=False, justification='right'),sg.InputText('Default Folder'), sg.FolderBrowse()],      
	[sg.Text('Choose the folder that contains the images to be analyzed: ', size=(65, 1), auto_size_text=False, justification='right'),sg.InputText('Default Folder'), sg.FolderBrowse()],
	[sg.Text('Choose the metadata file associated with this batch of images: ', size=(65, 1), auto_size_text=False, justification='right'), sg.Input(), sg.FileBrowse()],
	[sg.Submit(tooltip='Click to submit this window')],
	[sg.Exit()]]

	batch_window = sg.Window('Batch Image Counter', layout2, default_element_size=(80, 1))
	return batch_window

def make_single_win():
	layout3 = [
	[sg.Frame('Single Pic', key = '_test_', layout=[

	[sg.Frame('Worm Strains in Each Well', visible = True, layout=[
	[sg.Text('Strain in Well P', size=(15,1)), sg.InputText(key='-StrainP-')],
	[sg.Text('Strain in Well Q', size=(15,1)), sg.InputText()],
	[sg.Text('Strain in Well R', size=(15,1)), sg.InputText()],
	[sg.Text('Strain in Well S', size=(15,1)), sg.InputText()]])],

	[sg.Frame('Slot 1 Data', visible = True, layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText()],
	[sg.Text('Compound', size=(15,1)), sg.InputText()]]
	),
	sg.Frame('Slot 2 Data',visible = True,  layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText()],
	[sg.Text('Compound', size=(15,1)), sg.InputText()]
	])],

	[sg.Frame('Slot 3 Data',visible = True, layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText()],
	[sg.Text('Compound', size=(15,1)), sg.InputText()]]
	),
	sg.Frame('Slot 4 Data',visible = True,  layout=[
	[sg.Text('Plate ID', size=(15,1)), sg.InputText()],
	[sg.Text('Compound', size=(15,1)), sg.InputText()]
	])],

	[sg.Frame('Choose the image file to be analyzed', visible=True, layout=[  
	[sg.Text('Choose a folder to save your results in: ', size=(15, 1), auto_size_text=False, justification='right'),      
	    sg.InputText('Results folder', key='-results-'), sg.FolderBrowse()], 
	[sg.Text('Your File', size=(15, 1), auto_size_text=False, justification='right'),      
	    sg.InputText('Image file', key='-file-'), sg.FileBrowse(),sg.Button('Analyze'), sg.Exit(),]])]
	])]]

	single_im = sg.Window('Single Image Processing', layout3, size=(900,400))
	return single_im


def main():
	win1 = make_win1()
	while True:
		event, values = win1.read()     
		if event in (None, 'Exit'):
			break
		if values['_BATCH_']:
			win1.hide()
			batch_win = make_batch_win()
			while True:
				e2, v2 = batch_win.read()
				#print(e2, v2)
				if e2 in (None, 'Exit'):
					break
			batch_win.close()
			break
		if values['_SINGLE_']:
			win1.hide()
			single_win = make_single_win()
			while True:
				e3, v3 = single_win.read()
				if e3 == 'Analyze':
					fpath = (v3['-file-'])
					rpath = (v3['-results-'])
					ai.crop_image(fpath, rpath)
					break
				if e3 in (None, 'Exit'):
					break
			single_win.close()
			break

		

	win1.close()

if __name__ == '__main__':
    main()