# Import the required libraries
import cv2
import torch
import time


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
				emotion = results.pandas().xyxy[0].name[0]
				self.emotion_table[emotion] += 1
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

			# This is a Google API key. This key will be filled later.
			operator = open("googlekeys.txt", "r")
			api_key = operator.read()
			video_id = video.split("v=")[1]
			youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
			# This part extract the duration of the video
			video_response = youtube.videos().list(id=video_id, part="contentDetails").execute()
			duration = video_response["items"][0]["contentDetails"]["duration"]
			video_duration = isodate.parse_duration(duration).total_seconds()
			print(video_duration)
			self.timedDetection(self, source, model_path, video_duration)

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
				pass

			# read next frame
			success, img = vid.read()

	def clearEmotionData(self):
		self.emotion_table = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}

# This class contains every processing algorithms for the emotions data
class Processing:
	# def __init__(self, duration, table):
	# 	self.duration = duration
	# 	self.table = table

	def __init__(self):
		self.result = ""
		self.conversion_table = {0: 'happy', 1: 'sad', 2: 'neutral', 3: 'angry', 4: 'disgust', 5: 'surprise'}

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
	def getPredictedEmotion(self, data):
		from joblib import load

		# Load the model from a file using joblib
		model = load('Libs\walter.joblib')
		header = list(data.values())
		result = model.predict([header])
		result = self.conversion_table[result[0]]
		

		if data[result] <= 2:
			result = self.getDominantEmotion(data)
			print("Finny")
		else:
			print("Most")
		return result

test = Detection()
result = test.timedDetection("http://192.168.1.127:4747/mjpegfeed", "Libs\\Jessie_1.pt", 5)

true_emotion = Processing()
absolute_emotion = true_emotion.getPredictedEmotion(result)
print(absolute_emotion)