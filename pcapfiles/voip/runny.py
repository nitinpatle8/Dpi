
import os
from os import path
import sys

FOLDER = os.getcwd()

filenames = os.listdir(FOLDER)

for file in filenames:
	
	if "voipvideo" in file:
		x = file.replace("voipvideo", "voip")
	else:
		x = file.replace("voipaudio", "voip")
	
	os.rename(file,x)



