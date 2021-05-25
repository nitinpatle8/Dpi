
import os
from os import path
import sys

FOLDER = os.getcwd()

filenames = os.listdir(FOLDER)

for file in filenames:
	
	if "musicstreaming" in file:
		x = file.replace("musicstreaming", "streaming")
	else:
		x = file.replace("videostreaming", "streaming")
	
	os.rename(file,x)



