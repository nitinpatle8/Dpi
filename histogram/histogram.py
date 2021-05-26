import numpy as np
from tensorflow.python.keras.utils.np_utils import normalize
import tensorflow as tf
import keras
import os
import csv
import math

class histogram:

    def __init__(self, M = 300, N = 300, normalise = 5):
        self.M = M
        self.N = N
        self.mat = np.zeros(shape=(M, N))
        self.normalisef = normalise
    
    # insert packet size and time 

    def insert_pkt(self, pkt_byte, time, value):
        
        self.mat[pkt_byte//self.normalisef][math.floor(time * self.N/60.0)] += value

    
def csv2histogram(folder):
    
    # dp is
    # 
    # if folder exists
    # 

    if(not os.path.exists(folder)):
        return False
     
    filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == '.csv']

    cat = {'browsing':0, 'chat':1, 'filetransfer':2, 'streaming':3, 'voip':4}

    data = []
    label = []

    for file in filenames:
        
        # create a historgram out of this csv file 
        # append that histogram's matrix to data list

        h = histogram()
        category = ''
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                # row[3] packet size
                # row[2] time
                category = row[10]
                pkt_size = int(row[3])
                time = float(row[2])
                # print(pkt_size, time)
                h.insert_pkt(pkt_size, time, 1)
                line_count += 1
            
        data.append(h.mat)
    
        label.append(cat[category])    

    return (np.array(data), np.array(label))            


def __main__():

    train_data, train_label = csv2histogram('/home/hackerone/Documents/intern/DPIProjects/Dpi/pcapfile_train')

    # [test_data, test_label] = csv2histogram('/home/hackerone/Documents/intern/DPIProjects/Dpi/pcapfile_test/pcapfile_test')
    
    model = keras.Sequential([
            keras.layers.Flatten(input_shape=(300,300)), # 2d array to 1 d array
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(5, activation=tf.nn.softmax)
        ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# feeding the training data -> with label 
    model.fit(train_data, train_label, epochs=10)

    test_data, test_label = csv2histogram('/home/hackerone/Documents/intern/DPIProjects/Dpi/pcapfile_test')

    test_loss, test_acc = model.evaluate(test_data, test_label)


    print('test accuracy', test_acc)
    
    
__main__()