import tensorflow as tf


from tensorflow import keras 

import numpy as np
import matplotlib.pyplot as plt

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_name = ['T-shirt/top', 'Truoser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']


print(train_images.shape)
print(train_labels.shape)
print(train_labels[0])
# train_labels()

# plt.figure()
# plt.imshow(train_images[0])
# plt.colorbar()
# plt.grid(False)
# plt.show()

# scaling 0-255 to 0-1

train_images = test_images/255.0
test_images = test_images/255.0

plt.figure(figsize=(10,10))

for i in range(9):
    plt.subplot(3,3, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_name[train_labels[i]])

plt.show()

# configuring the layers of model

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)), # 2d array to 1 d array
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# feeding the training data -> with label 
model.fit(train_images, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_images, test_labels)


print('test accuracy', test_acc)

prediction = model.predict(test_images)

print(prediction[0])

print(test_labels[0])
