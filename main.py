import cv2
import numpy as np
import socket
import struct
from PIL import Image
import io

# Load YOLO
net = cv2.dnn.readNet("yolo_data/yolov3.weights", "yolo_data/yolov3.cfg")
layer_names = net.getLayerNames()
output_layer_indexes = net.getUnconnectedOutLayers().flatten() - 1
output_layers = [layer_names[i] for i in output_layer_indexes]
classes = [line.strip() for line in open("yolo_data/coco.names")]

# Consider these classes as animals (based on COCO dataset)
animal_classes = ["bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe"]

# Parameters
HOST, PORT = "localhost", 8000

def detect_motion(frame):
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # For each detection from each output layer, get the confidence, class id
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Get the class name
                class_name = classes[class_id]

                # If the class is in our list of animals, then consider it as valid detection
                if class_name in animal_classes:
                    print(f"Detected: {class_name}")
                    return True

    return False

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
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting...")
            break

        if detect_motion(frame):
            send_image_to_pc(frame)
            user_input = input("Do you want to continue detecting more birds? (yes/no): ").strip().lower()
            if user_input != 'yes':
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
