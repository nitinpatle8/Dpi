from keras.engine.sequential import Sequential
import numpy as np
from tensorflow.python.keras.utils.np_utils import normalize
import tensorflow as tf
import keras
import os
import csv
import math

# M = 300
# N = 300

class histogram:

    def __init__(self, M = 300, N = 300, normalise = 5):
        self.M = M
        self.N = N
        self.mat = np.zeros(shape=(M, N))
        self.normalisef = normalise
    
    # insert packet size and time 

    def insert_pkt(self, pkt_byte, time, value):
        
        self.mat[math.floor(pkt_byte//self.normalisef)][math.floor(time * self.N/15.0)] += value

def listcsv(folder):
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames if os.path.splitext(f)[1] == '.csv']

def csvfile2histogram(file):

    if(not os.path.exists(file)):
        return False

    cat = {'browsing':0, 'chat':1, 'filetransfer':2, 'videostreaming':3, 'musicstreaming': 4, 'voip':5}

    h = histogram(300, 300)
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
            if(time >= 15.0):
                break
            # if(row[1] == '0'):
            #     value = -1
            # if(row[1] == '1'):
            #     value = 2
            value = 1
            # print(pkt_size, time)
            h.insert_pkt(pkt_size, time, value)
            line_count += 1
    
    # h.mat = h.mat - h.mat.mean()
    # h.mat = h.mat / h
    label = cat[category]
    return (h.mat, label) 


def csv2histogram(folder):
    
    # dp is
    # 
    # if folder exists
    # 

    if(not os.path.exists(folder)):
        print("returning from here")
        return False
     
    filenames = listcsv(folder)
    
    print('size of filenames is ' + str(len(filenames)))
    cat = {'browsing':0, 'chat':1, 'filetransfer':2, 'videostreaming':3, 'musicstreaming':4, 'voip': 5}

    data = []
    label = []

    for file in filenames:
        
        # create a historgram out of this csv file 
        # append that histogram's matrix to data list

        (d, l) = csvfile2histogram(file)  
        data.append(d)
        label.append(l)

    return (np.array(data), np.array(label))            



def __main__():

    # print('this path exists ' + str(os.path.exists('/home/hackerone/Documents/intern/DPIProjects/Dpi/csvfile_train')))

    train_data, train_label = csv2histogram('/home/hackerone/Documents/intern/DPIProjects/Dpi/csvfile_train')
    if(len(train_data)==0):
        print('len th zero')
        return
    # [test_data, test_label] = csv2histogram('/home/hackerone/Documents/intern/DPIProjects/Dpi/pcapfile_test/pcapfile_test')
    
    # model = keras.Sequential([
      
    #         keras.layers.Flatten(input_shape=(300,300)), # 2d array to 1 d array
    #          # 2d array to 1 d array
    #         keras.layers.Dense(128, activation=tf.nn.relu),
    #         keras.layers.Dense(5, activation=tf.nn.softmax)
    #     ])
    train_data = train_data.reshape(len(train_data), 300, 300, 1)
    model = Sequential()

    model.add(keras.layers.Conv2D(filters=10, kernel_size=(10, 10),  activation='relu', input_shape=(300,300,1)))
    model.add(keras.layers.MaxPooling2D())

    model.add(keras.layers.Conv2D(filters=20, kernel_size=(10, 10),  activation='relu'))
    model.add(keras.layers.MaxPooling2D())

    model.add(keras.layers.Flatten())

    model.add(keras.layers.Dense(units=64, activation='relu'))
    # model.add(keras.layers.Dense(units=84, activation='relu'))

    model.add(keras.layers.Dense(units=6, activation = 'softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# feeding the training data -> with label 
    # print(len(train_data))
    # print(train_data)
    model.fit(train_data, train_label, epochs=50)

    test_data, test_label = csv2histogram('/home/hackerone/Documents/intern/DPIProjects/Dpi/csvfile_test')

    test_data = test_data.reshape(len(test_data), 300, 300, 1)

    test_loss, test_acc = model.evaluate(test_data, test_label)


    print('test accuracy', test_acc)
    
    
__main__()