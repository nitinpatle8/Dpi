import os
import pcap2csv as p2c
from os import path
import sys

def delete_csv(dir):
    # delete csv
    [os.remove(os.path.join(dir, file)) for file in os.listdir(dir) if file.endswith('.csv')]

def delete_csv_list(filenames):
    for file in filenames:
        os.remove(file)

def delete_file(file):
    os.remove(file)

# takes folder as system argument and deletes all csv files in that folder 
