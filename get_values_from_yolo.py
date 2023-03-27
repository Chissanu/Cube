import cv2
import torch
vid = cv2.VideoCapture(r"C:\Users\fin_t\OneDrive\เอกสาร\homework folder\cognitive\proj stuff\IMG_8286.MOV")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r"C:\Users\fin_t\OneDrive\เอกสาร\homework folder\cognitive\proj stuff\model_106.pt")
fps = vid.get(cv2.CAP_PROP_FPS)
print('frames per second =',fps)
success, img = vid.read()
fno = 0
count = 0
sad = 0
happy = 0
while success:
	if fno % 32 == 0:
		results = model(img)
		count +=1
		if results.pandas().xyxy[0].name[0] == "sad":
			sad +=1
		if results.pandas().xyxy[0].name[0] == "happy":
			happy +=1
		
	#print(count,results.pandas().xyxy[0])
	# read next frame
	success, img = vid.read()

print("total frames",count)
print("sad frames", sad)
print("happy frames", happy)
print("undetected frames", count-sad-happy)