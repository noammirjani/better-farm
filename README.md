# BetterFarm Bird Detection System

## Overview

The BetterFarm Bird Detection System utilizes a Raspberry Pi, a camera, and sophisticated computer vision techniques to automatically detect birds in real-time. If a bird is detected, a message is sent to a farmer through Telegram, alerting them of the bird's presence.

## How it Works

Motion Detection: By comparing consecutive frames, we can identify any movement on the field, potentially indicating bird activity.
Bird Identification with YOLOv3: Once motion is detected, the system uses the YOLOv3 algorithm to confirm if the movement was caused by a bird.
Alerts via Telegram: When a bird is detected, a Telegram bot sends a notification message to the farmer.

## Prerequisites

Raspberry Pi (with Raspbian OS installed)
Camera module for Raspberry Pi
YOLOv3 weights (download link needed in bird_detect.py)

## Setup

1. Clone this repository.
2. Install necessary Python packages:
```
pip install -r requirements.txt
```
3. Ensure you have the YOLOv3 weights in the yolo_data folder.
4. Set up the Telegram bot and get the TOKEN.
5. Replace the TOKEN in the Flask server script.

## Running the Detector

### Start the Flask server:
``` 
python TelegramBot/main.py
```
### Run the main detection script:
```commandline
python main.py
```

## Usage

When the system detects a bird, it will save the image to a local directory, and you will receive an alert on Telegram.