import PySimpleGUI as sg
import pandas as pd




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

	window = sg.Window('Spreadsheet', layout)

	while True:

		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'Exit'):
			window.close()
			break
		elif event == 'Submit':
			colorkey = generate_df(values)
			return colorkey
			window.close()
			break
		elif event == 'Clear':
			clear_all(window)
			continue


# def main():
#     make_ckey()

# if __name__ == '__main__':
#     main()

