"""
For regular use case, Jessie.py is sufficient. This code contains the developing tools that was used for the followings:
1. Testing Purposes: Test the trained A.I at a given parameter.
2. Model Training Purposes: Used to gather data for the Sci-Kit Learn Decision Tree
"""


# Import the required libraries
import cv2
import torch
import time
import csv
from sklearn import tree
import pandas as pd
import numpy as np

# This class contains all detection algorithms and some data accessing
class Detection:
	def __init__(self):
		# This dictionary stores emotions count detected by the A.I
		self.emotion_table = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}
	
	# Input the emotion and it returns how many times the A.I detected these emotions according to the emotion_table.
	# If no input is taken, it returns the whole dictionary
	def getEmotionData(self, key=None):
		if key:
			return [key, self.emotion_table[key]]
		
		else:
			return self.emotion_table

	# Get the most occuring emotion at a given interval
	def getMostOccuringEmotion(self):
		operator = self.emotion_table
		max_value = max(self.emotion_table, key=lambda x:operator[x])
		return max_value
	
	# Takes three inputs, the source of the video (0 for webcam), the model_path and the duration. Returns nothing at the moment
	def timedDetection(self, source, model_path, duration):
		self.clearEmotionData()
		vid = cv2.VideoCapture(source)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		fno = 0
		success, img = vid.read()
		initial = time.time()

		while success:
	
			if fno % 32 == 0:
				results = model(img)

			try:
				self.emotion_table[results.pandas().xyxy[0].name[0]] += 1
				current = time.time()
				if current - initial >= duration:
					print(current - initial)
					break

				print(self.emotion_table)

			except IndexError:
				print("Not Detected")
				pass

			# read next frame
			success, img = vid.read()

		return self.emotion_table

	# Untimed detection for debugging purposes. Same arguements as the timed ones
	def untimedDetection(self, source, model_path):
		self.clearEmotionData()
		vid = cv2.VideoCapture(source)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		fno = 0
		success, img = vid.read()

		while success:
	
			if fno % 32 == 0:
				results = model(img)

			try:
				self.emotion_table[results.pandas().xyxy[0].name[0]] += 1
				print(self.emotion_table)

			except IndexError:
				print("Not Detected")

			# read next frame
			success, img = vid.read()

	# This function is used to make the test data for the upcoming AI
	def collectData(self, source, model_path, csv_path, epochs): #
		self.clearEmotionData()
		header = list(self.emotion_table.keys())
		header.append("percieved_emotion")
		file = open(csv_path, "a", encoding = "UTF8", newline='')
		writer = csv.writer(file)
		# writer.writerow(header)
		
		for x in range(epochs):
			result = self.timedDetection(source, model_path, 5)
			operator = [result[header[0]], result[header[1]], result[header[2]], result[header[3]], result[header[4]], result[header[5]], np.nan]
			writer.writerow(operator)
			time.sleep(2) # To make the IP Camera not dying by closing and opening too many times.
		
		file.close()
		while True:
			choice_list = ["happy", "sad", "neutral", "angry", "disgust", "surprise"]
			print("Choice List: ", choice_list)
			choice = str(input("How are you feeling about this video?: "))
			
			
			if choice not in choice_list:
				print("Invalid Input")
			else:
				self.giveEmotionLabel(choice, choice_list, csv_path)
				break

	# Another function used to create video data. This is WIP (Working in Progress) only intended for development only.
	def collectVideoData(self, source, model_path, csv_path):
		self.clearEmotionData()
		vid = cv2.VideoCapture(source)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		fno = 0
		header = list(self.emotion_table.keys())
		header.append("percieved_emotion")
		success, img = vid.read()
		initial = time.time()

		while success:
			
			if fno % 32 == 0:
				results = model(img)

			try:
				current = time.time()
				self.emotion_table[results.pandas().xyxy[0].name[0]] += 1
				if current - initial >= 5:
					result = self.emotion_table
					file = open(csv_path, "a", encoding = "UTF8", newline='')
					writer = csv.writer(file)
					operator = [result[header[0]], result[header[1]], result[header[2]], result[header[3]], result[header[4]], result[header[5]], 3]
					if operator[3] <= 2:
						print("Skip!")
						self.clearEmotionData()
						initial = time.time()

					else:
						writer.writerow(operator)
						print(self.emotion_table)
						self.clearEmotionData()
						initial = time.time()

			except IndexError:
				# print("Not Detected")
				pass

			# read next frame
			success, img = vid.read()
		
		file.close()

	# Intermediate method, used with the collectData method to label the "perceived emotion" column.
	def giveEmotionLabel(self, choice, choice_list, csv_path):
		new_file = pd.read_csv(csv_path)
		index = int(choice_list.index(choice))
		new_file["percieved_emotion"] = new_file["percieved_emotion"].fillna(index)
		new_file.to_csv(csv_path, index=False)

	# Clears the emotion_table dictionary for another use
	def clearEmotionData(self):
		self.emotion_table = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}

# This class contains every processing algorithms for the emotions data
class Processing:
	def __init__(self):
		self.conversion_table = {0: 'happy', 1: 'sad', 2: 'neutral', 3: 'angry', 4: 'disgust', 5: 'surprise'}

	# Experimental, AI powered prediction from the custom gathered dataset. (Used Decision Tree). Result returns the absolute emotion value.
	def getPredictedEmotion(self, data):
		from joblib import load

		# Load the model from a file using joblib
		model = load('jacob_1.joblib')
		header = list(data.values())
		result = model.predict([header])
		result = self.conversion_table[result[0]]
		return result

	
	# Traditional method of logical prediction. Manually coded from common sense.
	def getDominantEmotion(self):
		pass

# Test run codes. Will be removed in the final iteration of this script.

test = Detection()

emote = test.timedDetection("http://10.100.9.1:4747/mjpegfeed", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\Jessie_1.pt", 5)

process = Processing()

processed_emotion = process.getPredictedEmotion(emote)

print(processed_emotion)
		