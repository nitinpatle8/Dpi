import os
import pcap2csv as p2c
from os import path
import sys

# this pcap_operation file is to get files from folder 
# and pass that list to pcap2csv generator

ip_address = ['192.168.43.153', '2001:4860:4864:6::1d']

last_rel_time = 60.0

def listDir(dir):

    filenames = [os.path.join(dir, file) for file in os.listdir(dir)]

    return filenames


def files2csv(filenames):
    
    for filename in filenames:
        filecsv = filename.removesuffix('.pcap')
        filecsv = filecsv + '.csv'
        try:
            if(p2c.check_files(filename, filecsv)):
                if not p2c.pcap2csv(filename, filecsv, ip_address, last_rel_time):
                    print(f"{filecsv} deleting this file")
                    os.remove(filecsv)
        except:
            print(f"{filename} not converted to csv")
            os.remove(filecsv)
            
def __main__():
   
    try:
        if path.isfile(sys.argv[1]): 
            files2csv([str(sys.argv[1])])

        elif path.isdir(sys.argv[1]):
            # print(sys.argv[1])
            filenames = listDir(str(sys.argv[1]))
            files2csv(filenames)
        
        print("successful converstion to csv")
    except:
        print("some error occured")
        exit(0)

__main__()