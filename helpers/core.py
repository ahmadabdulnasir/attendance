#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
import cv2
import os
from datetime import  datetime as dtime
from threading import Thread
import pickle
import face_recognition
import numpy as np
'''constants declaration '''
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Base directory were the current file is
# Setting haarcascade file to use
faceCascade_file = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
''' ./constants declaration'''

# 'haarcascade_frontalface_default'
# 'haarcascade_profileface'
# 'haarcascade_frontalcatface_extended'
# 'haarcascade_frontalface_default'
# 'haarcascade_upperbody'
# Create the haar cascade
faceCascade = cv2.CascadeClassifier(faceCascade_file)

# load the known faces and embeddings
print("[INFO] loading faces encodings model...")
data = pickle.loads(open("faces.model", "rb").read())
print("[INFO] loading faces encodings model Done")

def locaPredict(img):
    spam = face_recognition.load_image_file(img)
    boxes = face_recognition.face_locations(spam, model='hog')
    encodings = face_recognition.face_encodings(spam, boxes)
    name = "Unknown"
    for encoding in encodings:
		# attempt to match each face in the input image to our known  encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        # name = "Unknown"
        # check to see if we have found a match
        if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
			# loop over the matched indexes and maintain a count for
			# each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

		# update the list of names
		# names.append(name)
    result = name
    if result:
        rows = []
        tstp = str(dtime.now().strftime('%d-%b-%H-%Y-%M-%S%p'))
        username = result #['userid']
        present = 'Yes'
        date_ = str(dtime.now().strftime('%d_%b_%Y'))
        row = [tstp, username, present, date_]
        print('adding ', row)
        rows.append(row)
        saveRecord(rows)
    print(result)

def draw_box(frame):
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    today_dir = 'output/'+'{}/'.format(str(dtime.now().strftime('%d_%b_%Y')))
    frames_dir = today_dir+ 'frames/'
    output = 'output'
    if not os.path.isdir(output):
        os.mkdir(output)
    if not os.path.isdir(today_dir):
        os.mkdir(today_dir)
    if not os.path.isdir(frames_dir):
        os.mkdir(frames_dir)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
    	gray,
    	scaleFactor=1.1,
    	minNeighbors=5,
    	minSize=(30, 30),
    	#flags = cv2.CV_HAAR_SCALE_IMAGE
        )
    # Draw a rectangle around the faces
    exT = 30
    for (x, y, w, h) in faces:
        x = x - exT
        h = h + exT
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2) # BGR
        out_file = today_dir+ str(dtime.now().strftime('%d-%b-%H-%M-%s')) +'.png'
        frame_file = frames_dir +str(dtime.now().strftime('%d-%b-%H-%M-%s')) +'.jpg'
        cv2.imwrite(frame_file, frame)
        locaPredict(frame_file)

    return gray

header = ['Time Stamp', 'Username', 'Present', 'Date']
def saveRecord(rows):
    import csv
    if not os.path.isfile('Attendance.csv'):
        exit = False
    else:
        exit = True
    with open('Attendance.csv', 'a+', newline="") as f:
        c = csv.writer(f)
        if exit:
            pass
        else:
            c.writerow(header)
        for r in rows:
            c.writerow(r)
    print('*'*20 + ' Done ' + '*'*20)

def boot():
    '''
    This is a kick start function for testing the core module
    without the gui
    '''
    cap = cv2.VideoCapture(0)
    while(True):
    	# Capture frame-by-frame
    	ret, frame = cap.read()
    	img = draw_box(frame)
    	# Display the resulting frame
    	cv2.imshow('frame', img)
    	if cv2.waitKey(1) & 0xFF == ord('q'):
    		break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    boot()
