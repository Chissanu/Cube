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


	def untimedDetection(self, source, model_path):
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

	def getDominantEmotion(self,table):
		hmultiplier = 4
		smultiplier = 2
		nmultiplier = 1
		amultiplier = 3
		dmultiplier = 8
		sumultiplier = 8
		mullist = [hmultiplier,smultiplier,nmultiplier,amultiplier,dmultiplier,sumultiplier]
		emolist = ["happy","sad","neutral","angry","disgust","surprise"]

		for i in range(6):
			table[emolist[i]]*=mullist[i]

		print(table)
		return table
	
	def getMostOccuringEmotion(self,table):
		operator = table
		max_value = max(table, key=lambda x:operator[x])
		print(max_value)
		return max_value



		

print("hello world")
print("hello world")
print("hello world")
print("hello world")
print("hello world")
# Test run codes. Will be removed in the final iteration of this script.

#random text for now, will get from backend later
wordcount = 0
text = "SDKGHK JHSHOIHGPI SHGO IDS HOIHG OIHdkgsh ghsigh slkghs lgh"
for i in text:
	if i == " ":
		wordcount +=1
#human reading rate is 4 words/sec, detection time is average read time + 25%
d = (wordcount/4) + (wordcount/8)
test = Detection()
t = test.timedDetection(0, "C:/Users/ACER/Documents/KMITL/cognitive/proj/model_201.pt", 5)

trueemotion = Processing()
t = trueemotion.getDominantEmotion(t)
trueemotion.getMostOccuringEmotion(t)