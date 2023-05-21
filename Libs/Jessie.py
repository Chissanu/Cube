# Import the required libraries
import cv2
import torch
import time
import statistics

# This class contains all detection algorithms and some data accessing
class Detection:
	def __init__(self):
		# This dictionary stores emotions count detected by the A.I
		self.emotion_table = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}
		self.emotion_table_cache = []
		self.calibration_operator = []
		self.user_calibration_constant = 0
		self.detection_control = 0
		self.real_time_emotion = ""
	
	# Takes three inputs, the source of the video (0 for webcam), the model_path and the duration. Returns nothing at the moment
	def timedDetection(self, source, model_path, duration):
		self.clearEmotionData()
		vid = cv2.VideoCapture(source)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		fno = 0
		success, img = vid.read()
		initial = time.time()
		count = 0

		while success:
			count += 1
			if fno % 32 == 0:
				results = model(img)

			current = time.time()
			if current - initial >= duration:
				# print(current - initial)
				break

			else:
				try:
					emotion = results.pandas().xyxy[0].name[0]
					self.emotion_table[emotion] += 1
					# print(self.emotion_table)

				except IndexError:
					#print("Not Detected")
					pass
			
				# read next frame
				success, img = vid.read()
		
		if len(self.calibration_operator) <= 5:
			self.calibration_operator.append(count)

		return self.emotion_table
			
	def clearEmotionData(self):
		self.emotion_table = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}

	def calibration(self, source, model_path):
		epochs = 5
		for x in range(epochs):
			self.timedDetection(source, model_path, 5)
			initial = time.time()

		while True:
			current = time.time()
			if current - initial >= 1:
				break
 
		print("========================================")
		print("           Calibration Finish           ")
		print("========================================")
		return statistics.mean(self.calibration_operator)
	
	def initialize(self, source, model_path):
		self.timedDetection(source, model_path, 1)
		self.calibration_operator = []
		print("========================================")
		print("              Initialized               ")
		print("========================================")
		return
	
	def realTimeDetection(self, source, model_path, calibration_constant):
		self.clearEmotionData()
		vid = cv2.VideoCapture(source)
		model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
		fno = 0
		success, img = vid.read()
		initial = time.time()
		time_elasped = 0
		detection_threshold = 5
		duration = 1
		self.detection_control = 0

		while success and self.detection_control == 0:
			if fno % 32 == 0:
				results = model(img)

			if time_elasped >= detection_threshold:
				# print(time_elasped)
				duration = 0.5
				total_emotion = []
				for items in self.emotion_table_cache:
					if total_emotion == []:
						total_emotion = list(items.values())
						# print(total_emotion)
					
					else:
						temp = list(items.values())
						total_emotion = [total_emotion[0] + temp[0], total_emotion[1] + temp[1], total_emotion[2] + temp[2], 
		       							total_emotion[3] + temp[3], total_emotion[4] + temp[4], total_emotion[5] + temp[5]]
						# print(total_emotion)

				prediction_data = {"happy": total_emotion[0], "sad": total_emotion[1], "neutral": total_emotion[2],
		       					  "angry": total_emotion[3], "disgust": total_emotion[4], "surprise": total_emotion[5]}
				
				get_emotion = Processing()
				self.real_time_emotion = get_emotion.getPredictedEmotion(prediction_data, calibration_constant)
				print(self.real_time_emotion)
				total_emotion = []
				self.emotion_table_cache.pop(0)
				time_elasped -= 1
				# self.stop_detection()
				# print("New Iteration")

			else:
				try:
					emotion = results.pandas().xyxy[0].name[0]
					self.emotion_table[emotion] += 1

				except IndexError:
					#print("Not Detected")
					pass
			
			current = time.time()
			if current - initial >= duration:
				time_elasped += 1
				self.emotion_table_cache.append(self.emotion_table)
				self.emotion_table = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}
				# print(self.emotion_table_cache)
				initial = time.time()
				# read next frame
				success, img = vid.read()
	
	def stop_detection(self):
		self.detection_control = 1
		return

# This class contains every processing algorithms for the emotions data
class Processing:

	def __init__(self):
		self.result = ""
		self.conversion_table = {0: 'happy', 1: 'sad', 2: 'neutral', 3: 'angry', 4: 'disgust', 5: 'surprise'}
		# Model Data Calibration Constant Multiplier
		self.model_calibration_constant = 170

	def getDominantEmotion(self, table):
		hmultiplier = 40
		smultiplier = 2
		nmultiplier = 1
		amultiplier = 3
		dmultiplier = 10
		sumultiplier = 8 
		mullist = [hmultiplier,smultiplier,nmultiplier,amultiplier,dmultiplier,sumultiplier]
		emolist = ["happy","sad","neutral","angry","disgust","surprise"]

		for i in range(6):
			table[emolist[i]]*=mullist[i]

		# print(table)
		return max(table, key=table.get)
	
	# AI powered prediction from the custom gathered dataset. Result returns the absolute emotion value as a string
	def getPredictedEmotion(self, data, calibration_constant):
		from joblib import load

		# Load the model from a file using joblib
		model = load('Libs\walter.joblib')
		header = list(data.values())
		calibrated_header = []
		calibration_ratio = 0

		if calibration_constant <= self.model_calibration_constant:
			calibration_ratio = self.model_calibration_constant // calibration_constant

		for x in header:
			calibrated_header.append(x + (x * calibration_ratio))

		# print(calibrated_header)
		result = model.predict([calibrated_header])
		result = self.conversion_table[result[0]]
		

		if data[result] <= 0:
			result = self.getDominantEmotion(data)
			#print("Finny")
		else:
			pass
			#print("Most")
		return result
	
# test = Detection()
# test.initialize(0, "Libs\Jessie_1.pt")
# calibrate = test.calibration(0, "Libs\Jessie_1.pt")
# test.realTimeDetection(0, "Libs\Jessie_1.pt", calibrate)