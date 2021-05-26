import os
import pcap2csv as p2c
from os import path
import sys

def delete_csv_list(filenames):
    for file in filenames:
        os.remove(file)

def delete_csv(dir):
    # delete csv
    filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir) for f in filenames if os.path.splitext(f)[1] == '.csv']
    delete_csv_list(filenames)


def delete_file(file):
    os.remove(file)

# takes folder as system argument and deletes all csv files in that folder 
