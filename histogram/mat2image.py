import histogram as h
import numpy as np
from PIL import Image as im
import os 
# mat is a numpy array
def mat2png(mat):

    rows, columns = (300, 300)
    for i in range(rows):
        for j in range(columns):
            if(mat[i][j] > 0):
                mat[i][j] = 0
            else:
                mat[i][j] = 255
    
    data = im.fromarray(mat)
    data = data.convert("L")

    return data


def csvfile2img(file, folder):
        (data, label) = h.csvfile2histogram(file)
        data = mat2png(data)

        file = os.path.basename(file)
        file = file.removesuffix('.csv')
        file = file + '.png'
        filepath = os.path.join(folder, file)
        print(filepath)
        data.save(filepath)
            

def csv2img(folder, savefolder):
    filenames = h.listcsv(folder)
    
    for file in filenames:
        csvfile2img(file, savefolder)

def __main__():
    
    csv2img('/home/hackerone/Documents/intern/DPIProjects/Dpi/pcapfile_train/', '/home/hackerone/Documents/intern/DPIProjects/Dpi/imagef/train')
    csv2img('/home/hackerone/Documents/intern/DPIProjects/Dpi/pcapfile_test/', '/home/hackerone/Documents/intern/DPIProjects/Dpi/imagef/test')

__main__()




 
