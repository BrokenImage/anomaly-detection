# -*- coding: utf-8 -*-
"""arvin_solar_module_clf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A7uVb9WPyy23ckzR8tgh0KyOHrP-c4eo
"""



# mounting google drive to access photos and dara
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# dir = "/content/drive/My Drive/InfraredSolarModules/"

import numpy as np
import keras as k
import json
import PIL

from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16 
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image

# imports photo data from JSON file
def imagegen():
    f = open('/content/drive/My Drive/InfraredSolarModules/module_metadata.json',) 
    meta = json.load(f) 
    f.close() 
    img = []
    label = []
    for i in range(9000,20000):
        print("doing image"+str(i))
        img.append(np.array(k.preprocessing.image.load_img('/content/drive/My Drive/InfraredSolarModules/' + meta[str(i)]['image_filepath'], target_size=(224, 224))))
        if meta[str(i)]['anomaly_class'] == 'No-Anomaly':
          label.append('No-Anomaly')
        else:
          label.append('Anomaly')  
    return np.array(img), np.array(label)
# generate images and labels 
imgs, labels = imagegen()
print(imgs.shape)
print(len(imgs))
print(len(imgs.shape))

#generator function to load images in batches
def imageLoader(imgs, batch_size):

    L = len(imgs)

    # this line is just to make the generator infinite, keras needs that    
    while True:

        batch_start = 0
        batch_end = batch_size

        while batch_start < L:
            print(batch_start)
            limit = min(batch_end, L)
            X = imgs[batch_start:limit]
            
            # Y = labels[batch_start:limit]
        # break
            yield X 
            
            batch_start += batch_size   
            batch_end += batch_size

#preprocess images for feature extraction
def preprocess_image(imgs):
  preprocessed_images = []
  counter = 1
  for image_item in imgs:
    print("doing image {}".format(counter))
    # image_item = image.img_to_array(image_item)
    image_item = np.expand_dims(image_item, axis=0)
    image_item = preprocess_input(image_item) 
    counter+=1

preprocess_image(imgs)

model = VGG16(weights="imagenet", include_top=False, classes=2)

# extract features
features = model.predict(imageLoader(imgs,100),steps=110)

print(features.shape)

type(imgs)

imgs.shape

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier

#reshape for training
features = features.reshape(11000,7*7*512)
#instantiate classifier model(Stochastic Gradient Decent)
svm_classifier = SGDClassifier()
#split data
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.35)

print(X_train.shape)

print(X_train.shape)
print(y_train)

#train
svm_classifier.fit(X_train, y_train)
#predict
y_pred = svm_classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score, accuracy_score, precision_score
#metrics
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))
print(precision_score(y_test, y_pred, pos_label='Anomaly'))
print(f1_score(y_test, y_pred, pos_label='Anomaly'))