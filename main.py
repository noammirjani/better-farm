import cv2
from bird_detect import detect_bird
from detect_motion import detect_motion
import os
import time
from datetime import datetime
import requests


previous_frame = None
img_counter = 0  # Counter to name saved images uniquely
SAVE_DIR = "bird-detected"
webhook_url = 'https://b25d-82-80-173-170.ngrok-free.app/detected'
telegram_chat_id = '5669380497'

# Create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def save_image_locally(frame):
    global img_counter
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Modify the save path to include the bird-detected directory and the timestamp
    img_name = os.path.join(SAVE_DIR, f"detected_bird_{timestamp}_{img_counter}.jpg")
    cv2.imwrite(img_name, frame)
    print(f"Image saved as {img_name}")
    img_counter += 1


def open_camera():
    ap = cv2.VideoCapture(0)
    if not ap.isOpened():
        raise IOError("Cannot open webcam")
    return ap


def close_camera(cap):
    cap.release()
    cv2.destroyAllWindows()


def send_message_to_telegram_bot():
    now = datetime.now()
    formatted_time = now.strftime("%H:%M")
    formatted_date = now.strftime("%d.%m.%Y")

    message = f"A bird was detected at {formatted_time} on {formatted_date}"

    payload = {
        'url': webhook_url,
        'chat_id': telegram_chat_id,
        'text': message,
    }

    response = requests.post(webhook_url, json=payload)
    return response


def run(cap):
    ret, pre_frame = cap.read()

    while True:
        ret, current_frame = cap.read()

        if detect_motion(current_frame, pre_frame) and detect_bird(current_frame):
            print("Motion detected, and a bird has been spotted!")
            save_image_locally(current_frame)

            # msg to telegram
            response = send_message_to_telegram_bot()
            if response.status_code == 200:
                print("message to farmer sent successfully")

            time.sleep(3)  # Pause the program for 3 seconds

        pre_frame = current_frame.copy()


def main():
    cap = None
    try:
        cap = open_camera()
        run(cap)
    except KeyboardInterrupt:
        print("Program stopped by user.")
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        close_camera(cap)


if __name__ == "__main__":
    main()
