# This code is already obsolete and its mostly for archival purposes

# Import the required libraries (Some libraries will not be import here)
import cv2
import torch
import time
import csv
from sklearn import tree
import pandas as pd
import numpy as np
import os

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

	# This special method is used on videos it takes the same arguements as the two methods.
	# It also takes two additional methods "mode" and "video", the "mode" specifies the format of the video and the "video" specifies the path/link.
	# If the mode is 0, the video is a normal video file (mp4, mjpeg, mpeg, mov). If it is 1, it is a youtube link.
	# This method will call the "timedDetection" method according to the video duration.
	# Note: From testing the video link duration will be slightly greater since there is also the duration of ADs.

	def timedDetectionVideo(self, source, model_path, video, mode):
		if mode == 0:
			capture_video = cv2.VideoCapture(video)
			video_duration = capture_video.get(cv2.CAP_PROP_POS_MSEC)
			print(video_duration)
			self.timedDetection(self, source, model_path, video_duration)

		# This piece of this code can only be ran around 5000 times per day. Please don't over use this method
		elif mode == 1:
			import googleapiclient.discovery
			import isodate

			# This is a Google API key. This key belongs to my account
			api_key = "AIzaSyC96RuGTW8FpllPXsIXa7uxmQmwk9M1T3I"
			video_id = video.split("v=")[1]
			youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
			# This part extract the duration of the video
			video_response = youtube.videos().list(id=video_id, part="contentDetails").execute()
			duration = video_response["items"][0]["contentDetails"]["duration"]
			video_duration = isodate.parse_duration(duration).total_seconds()
			print(video_duration)
			self.timedDetection(self, source, model_path, video_duration)

	# This method is used to make the test data for the decision tree AI. Only intended for development purposes.
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

	# Another method used to create video data. Only intended for development only.
	def collectVideoData(self, source, model_path, csv_path):
		self.clearEmotionData()
		vid = cv2.VideoCapture(source)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		fno = 0
		header = list(self.emotion_table.keys())
		header.append("percieved_emotion")
		success, img = vid.read()
		initial = time.time()
		file = open(csv_path, "a", encoding = "UTF8", newline='')
		writer = csv.writer(file)

		while success:
			# if fno % 32 == 0:
			results = model(img)

			try:
				current = time.time()
				self.emotion_table[results.pandas().xyxy[0].name[0]] += 1
				if current - initial >= 5:
					emotion = self.emotion_table
					operator = [emotion[header[0]], emotion[header[1]], emotion[header[2]], emotion[header[3]], emotion[header[4]], emotion[header[5]], 4]
					if operator[4] <= 1:
						print("Skip!: ", self.emotion_table)
						self.clearEmotionData()
						initial = time.time()

					else:
						file = open(csv_path, "a", encoding = "UTF8", newline='')
						writer.writerow(operator)
						print(self.emotion_table)
						self.clearEmotionData()
						initial = time.time()
						file.close()

			except IndexError:
				# print("Not Detected")
				pass

			# read next frame
			success, img = vid.read()

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
		self.result = ""
		self.conversion_table = {0: 'happy', 1: 'sad', 2: 'neutral', 3: 'angry', 4: 'disgust', 5: 'surprise'}

	# Experimental, AI powered prediction from the custom gathered dataset. (Used Decision Tree). Result returns the absolute emotion value.
	def getPredictedEmotion(self, data):
		from joblib import load

		# Load the model from a file using joblib
		model = load('jacob_2.joblib')
		header = list(data.values())
		result = model.predict([header])
		result = self.conversion_table[result[0]]
		return result
	
	# Traditional method of logical prediction. Manually coded from common sense.
	def getDominantEmotion(self):
		pass

# Test run codes. Will be removed in the final iteration of this script.

test = Detection()

emote = test.timedDetection(0, "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\Jessie_1.pt", 5)

process = Processing()

processed_emotion = process.getPredictedEmotion(emote)

print(processed_emotion)

# chosen_folder_dir = 'C:\\Users\\Firesoft\\Downloads\\Data_Collection_Video'
# validation = 0

# new_file_array = []

# files = os.listdir(chosen_folder_dir)

# for file in files:
# 	new_file_array.append(chosen_folder_dir + "\\" + file)

# print(new_file_array)

# for videos in new_file_array:
# 	test.collectVideoData(videos, "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\Jessie_1.pt", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\data_collection.csv")

# test.collectData("http://10.100.9.1:4747/mjpegfeed", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\Jessie_1.pt", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\datasets\\experiment_data.csv", 150)
# test.collectVideoData("C:\\Users\\Firesoft\\Downloads\\Data_Collection_Video\\Disgust_3_AdobeExpress.mp4", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\Jessie_1.pt", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\datasets\\experiment_data.csv")
# test.untimedDetection("C:\\Users\\Firesoft\\Downloads\\Disgust2.mp4", "C:\Users\Firesoft\Documents\Computing\Testing_Grounds\trained_models\Jessie_1.pt")