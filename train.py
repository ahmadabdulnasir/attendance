#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
import face_recognition
import cv2
import numpy as np
import os
import pickle


names = list()
enc = list()
d = os.listdir()
people = {}
for name in d:
    if os.path.isdir(name):
        print(os.listdir(name))
        print('[INFO] Found directory: {}'.format(name))
        fs = os.listdir(name)
        people[name] = fs
    else:
        print('[INFO] Not a directory: {}'.format(name))



def encodeUser(name):
    print('[INFO] Working on {}'.format(name))
    for img in people.get(name):
        img_file = name+'/'+img
        try:
            spam = face_recognition.load_image_file(img_file)
            egg = face_recognition.face_encodings(spam)[0]
            names.append(name)
            enc.append(egg)
        except Exception as e:
            print('[ERROR] : {}'.format(str(e) ))


 #
def boot():
    for name in people.keys():
        encodeUser(name)
    print('[INFO] Work Done ' + '*'*10+'\n Writing Data to Disk ....')
    data = {"encodings": enc, "names": names}
    f = open("faces.model", "wb")
    f.write(pickle.dumps(data))
    f.close()
    print('[INFO] All Done')
if __name__ == "__main__":
    boot()
