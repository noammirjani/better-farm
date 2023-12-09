# BetterFarm Bird Detection System

The BetterFarm Bird Detection System is a culmination of the learnings and skills acquired during the Bootcamp OS Scale-Up Velocity (August-July 2023). This project involved managing a structured system, working with Raspberry Pi 4 and Linux, utilizing Python, and integrating with the Telegram API.

## Table of Contents
- [Overview](#overview)
- [How it Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Detector](#running-the-detector)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Dependencies](#dependencies)
- [Bootcamp Experience](#bootcamp-experience)
- [License](#license)

## Overview

The system operates in three primary steps: motion detection, bird identification using YOLOv3, and Telegram alerts. It continuously monitors the field for movement, checks if the motion corresponds to a bird, and sends timely notifications to the farmer.

## How it Works

### Motion Detection

- Utilizes frame comparison to identify any motion in the field.
- Suggests potential bird activity if movement is detected.

### Bird Identification with YOLOv3

- Employs the YOLOv3 algorithm to confirm bird presence upon detecting motion.
- Validates the movement by analyzing the captured frames.

### Alerts via Telegram

- Sends a notification message to the farmer upon bird detection.
- Enables quick response to potential threats in the field.

## Prerequisites

Ensure the following components and resources are available:

- Raspberry Pi with Raspbian OS installed
- Camera module compatible with Raspberry Pi
- YOLOv3 weights for object detection (Download link required; update bird_detect.py)

## Setup

1. Clone this repository.
2. Install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Download the [YOLOv3 weights](https://github.com/patrick013/Object-Detection---Yolov3/blob/master/model/yolov3.weights) and place them in the designated `yolo_data` folder.
4. Follow the steps below to create a new Telegram bot and obtain a token.

### Creating a Telegram Bot and Obtaining Token

1. Open Telegram and search for the "BotFather" bot.
2. Start a conversation with BotFather and type `/newbot` to create a new bot.
3. Follow the prompts to choose a name and username for your bot.
4. Once created, BotFather will provide a token for your bot. Copy this token.
5. Replace the `TOKEN` placeholder in the Flask server script with the copied token.

### Setting Up Webhook URL for the Telegram Bot

1. Expose your local server to the internet using a service like ngrok.
2. Start ngrok and obtain the public URL.
3. In your Telegram bot conversation with BotFather, use the `/setWebhook` command followed by your ngrok URL and the endpoint `/detected`.
4. Update the `webhook_url` variable in the Flask server script with your ngrok URL.

## Running the Detector

### Option 1: Running Server and Controller Separately

- Start the Flask server:
    ```bash
    python TelegramBot/main.py
    ```
- Run the controller script to interact with the server.

### Option 2: Running Both Server and Client

- Execute the main detection script:
    ```bash
    python main.py
    ```
- This automatically starts the Flask server and initiates the detection process.

## Usage

Upon bird detection, the system saves an image locally and sends an alert via Telegram to notify the user.

## Features

- **Motion Detection:** Utilizes frame comparison to identify movement in the field.
- **Bird Identification with YOLOv3:** Employs YOLOv3 to confirm bird presence upon detecting motion.
- **Alerts via Telegram:** Sends immediate notifications to the farmer upon bird detection.

## Contributing

To contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/fooBar`).
3. Make your changes and commit them (`git commit -am 'Add some fooBar'`).
4. Push to the branch (`git push origin feature/fooBar`).
5. Create a new Pull Request.

## Dependencies

- **MacBook with Camera Permissions**
  
OR

- **Raspberry Pi Requirements:**
  - Raspberry Pi 4 with Raspbian OS installed and connected to the internet.
  - Camera module compatible with Raspberry Pi.
  
Additionally, ensure the availability of the following resources:

- YOLOv3 weights for object detection (Download link required; update bird_detect.py).


### Platform-Specific Instructions

- **For macOS (MacBook):** The code works seamlessly without any changes.
- **For Raspberry Pi 4 with Camera Module:** Camera Initialization: The code currently uses the default camera (`cv2.VideoCapture(0)`). For the Raspberry Pi camera module, you might need to use `cv2.VideoCapture(0)` or `cv2.VideoCapture(-1)`. Try both to see which one works.


## Bootcamp Experience

This project was developed as part of the Bootcamp OS Scale-Up Velocity in August-July 2023. During the bootcamp, the focus was on learning how to manage projects effectively, structure systems, work with Raspberry Pi 4 and Linux, and utilize Python programming for real-world applications. Additionally, integration with the Telegram API was explored for communication and alerts.

## License

This project is licensed under the [MIT License](LICENSE).