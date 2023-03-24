### Note: These models are for testing purposes only and more advanced and tailored versions will be updated later.

# Download the models here:
## OneDrive - https://kmitlthailand-my.sharepoint.com/:f:/g/personal/64011532_kmitl_ac_th/Eu1vFiHfwXFGqmF67tWw_ogBKCKi1wPFEpRUrqMYaoFldw?e=QEIieH

# Testing the model via command line

## Step 1: Install the Pytorch libraries (For Nvidia GPU).

```shell
pip3 install torch --index-url https://download.pytorch.org/whl/cu118
pip3 install torchvision --index-url https://download.pytorch.org/whl/cu118
pip3 install torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Step 2: Clone the YOLOv5 repository.

```shell
git clone https://github.com/ultralytics/yolov5
```

## Step 4: Change the working directory to your cloned library

```shell
cd <your_yolov5_folder_cloned_from_github>
```

## Step 4: Install the required dependencies

```shell
pip3 install -qr requirements.txt
```

# Model detection using different inputs

## Picture:

```shell
python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.5 --source <your_picture_directory>
```

## Video:

```shell
python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.5 --source <your_video_directory>
```

## Webcam (Live Video Feed):

```shell
python detect.py --weights runs/train/exp/weights/best.pt --img 416 --conf 0.5 --source 0
```

### Note: Other than the webcam detection, the video and picture detection can provide an output with drawn landmarks. The directory of that file will be shown in the command line output.

# Model information

* Model 101 - Simplest model and the first working prototype. (Not recommend)
* Model 102 - The most stable model and resonably accurate prototype.
* Model 106 (Newest) - The tailored version of the Model 102. It is the most accurate one so far.
