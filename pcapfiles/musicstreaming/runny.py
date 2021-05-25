
import os
from os import path
import sys

FOLDER = os.getcwd()

filenames = os.listdir(FOLDER)

for file in filenames:
	x = file.replace("videostreaming", "musicstreaming")

	os.rename(file,x)



