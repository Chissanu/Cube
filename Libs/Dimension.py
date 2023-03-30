import cv2
import torch
# Capture the camera frame
vid = cv2.VideoCapture("http://10.100.9.1:4747/mjpegfeedjjjj")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r"C:\Users\Firesoft\Documents\Computing\Testing_Grounds\trained_models\model_201.pt")
fps = vid.get(cv2.CAP_PROP_FPS)
print('frames per second =',fps)
success, img = vid.read()

# Emotion Count Dictionary
emotion_count = {"happy": 0, "sad": 0, "neutral": 0, "angry": 0, "disgust": 0, "surprise": 0}
fno = 0
count = 0

while success:
	if fno % 32 == 0:
		results = model(img)
		count +=1
	try:
		emotion_count[results.pandas().xyxy[0].name[0]] += 1
		print(emotion_count)
			    
	except IndexError:
		print("Not Detected")
			
	# print(count,results.pandas().xyxy[0])
	# read next frame
	success, img = vid.read()

print("total frames",count)