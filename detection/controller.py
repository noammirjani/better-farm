import cv2
import os
from datetime import datetime
import requests
from detection.bird_detect import detect_bird, update_image
from detection.detect_motion import detect_motion

SAVE_DIR = "images-archive"
webhook_url = 'https://----.ngrok.io/detected'
telegram_chat_id = '----'


if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


# Saves frames containing detected birds.
def save_bird_image(frame, counter):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    img_name = os.path.join(SAVE_DIR, f"detected_bird_{timestamp}_{counter}.jpg")
    cv2.imwrite(img_name, frame)
    print(f"Image saved as {img_name}")
    return img_name


# Notifies about the bird detection via Telegram.
def send_telegram_message():
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


# Runs the bird detection process.
def run_bird_detection(cap):
    ret, pre_frame = cap.read()
    img_counter = 0
    print("🔎🔎🔎")

    while True:
        ret, current_frame = cap.read()

        if detect_motion(current_frame, pre_frame) and detect_bird(current_frame):
            update_image(current_frame)
            print("Motion detected, and a bird has been spotted!")
            save_bird_image(current_frame, img_counter)
            img_counter += 1

            response = send_telegram_message()
            if response.status_code == 200:
                print("Message to farmer sent successfully")
            print("🔎🔎🔎 ")
            # time.sleep(1)

        pre_frame = current_frame.copy()


# Opens the camera for video capture.
def open_camera():
    cap = cv2.VideoCapture(0)  # 0 represents the default camera
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    return cap


# Closes the camera capture.
def close_camera(cap):
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()


# Main function to start the bird detection process.
def run():
    cap = None
    try:
        cap = open_camera()
        run_bird_detection(cap)
    except KeyboardInterrupt:
        print("Program stopped by user.")
    except Exception as e:
        print("An error occurred: ", e)
    finally:
        close_camera(cap)


if __name__ == "__main__":
    run()

