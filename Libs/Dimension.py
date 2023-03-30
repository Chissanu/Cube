# Import the required libraries
import cv2
import torch
import time

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


# Test run codes. Will be removed in the final iteration of this script.

test = Detection()
test.timedDetection("http://10.100.9.1:4747/mjpegfeed", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\model_201.pt", 5)

while True:
	query = str(input("Choices: [None, data]?:" ))
	if query == 'data':
		print(test.getEmotionData())

	else:
		print(test.getMostOccuringEmotion())
		