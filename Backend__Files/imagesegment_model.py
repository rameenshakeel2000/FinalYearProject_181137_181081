# -*- coding: utf-8 -*-
"""ImagesegUnet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q-vJRjuEzd1N8x5mItktAKsJuBSRZBgI
"""

from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
import matplotlib.pyplot as plt
import pathlib
import librosa
import librosa.display
from keras.layers.convolutional import Conv2D,MaxPooling2D

from google.colab import drive
drive.mount('/content/drive/')

cd 'drive/MyDrive'

data = 'Braintumor/images/'

X=[]
path = data
for x in os.listdir(path):
  img=cv2.imread(path+x)
  img = cv2.resize(img, (448,448))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  X.append(img)

!pip3 install -U segmentation-models

import segmentation_models as sm

model = sm.Unet('vgg16', input_shape=(448, 448, 1), encoder_weights=None,activation='sigmoid')

model.summary()

label = 'Braintumor/masks/'

Y=[]
path = label
for x in os.listdir(path):
  img=cv2.imread(path+x)
  img= cv2.resize(img,(448,448))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  Y.append(img)

X=np.array(X)
Y=np.array(Y)

from keras import backend as K
def jaccard_distance(y_true, y_pred, smooth=100):
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
    jac = (intersection + smooth) / (sum_ - intersection + smooth)
    return jac

def dice_loss(y_true, y_pred):
  y_true = tf.cast(y_true, tf.float32)
  y_pred = tf.math.sigmoid(y_pred)
  numerator = 2 * tf.reduce_sum(y_true * y_pred)
  denominator = tf.reduce_sum(y_true + y_pred)

  return  numerator / denominator

model.compile('adam',loss=[dice_loss],metrics=['accuracy'],)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25,random_state=80)

y_train=tf.cast(y_train, tf.float32)
x_train=tf.cast(x_train, tf.float32)
x_test=tf.cast(x_test, tf.float32)
y_test=tf.cast(y_test, tf.float32)

model.fit(x_train,y_train,batch_size=10,epochs=10,validation_data=(x_test,y_test),verbose=True)

pred=model.predict(X[:1])

from matplotlib import *
#pred=pred.reshape(448,448)
plt.imshow(pred.reshape(448,448))

import numpy as np
print(np.shape(model.predict(X)))

a=[[1,2,3],[4,5,6]]
print(np.shape(a))

print(a[0][0])

print(type(model.predict(X)))

y= model.predict(X)

print(np.shape(y[1]))

yy=y[8]>0.85
print(yy.reshape(448,448))
cvy=yy.reshape(448,448) 

plt.imshow(cvy.astype(np.uint8))