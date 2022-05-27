from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

with open("C:/Users/Emily/Desktop/current_analysis/auto_results/DS2_R1.csv","r") as file:
	file_drive = drive.CreateFile({'title':os.path.basename(file.name) })  
	file_drive.SetContentString(file.read()) 
	file_drive.Upload()