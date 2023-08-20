import cv2
from bird_detect import detect_bird
from detect_motion import detect_motion
import socket
import struct
from PIL import Image
import io

HOST, PORT = "localhost", 8000
previous_frame = None


def send_image_to_pc(frame):
    image_stream = io.BytesIO()
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img.save(image_stream, format='JPEG')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        image_data = image_stream.getvalue()
        s.sendall(struct.pack('<L', len(image_data)))
        s.sendall(image_data)


def main():
    cap = cv2.VideoCapture(0)
    global previous_frame
    ret, previous_frame = cap.read()

    while True:
        ret, current_frame = cap.read()

        if detect_motion(current_frame, previous_frame) and detect_bird(current_frame):
            print("Motion detected, and a bird has been spotted!")
            send_image_to_pc(current_frame)
            user_input = input("Do you want to continue? (yes/no): ").strip().lower()
            if user_input != 'yes':
                break

        previous_frame = current_frame.copy()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
