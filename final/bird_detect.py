import cv2
import argparse
import numpy as np


def detect_bird(frame):
    # Load YOLO
    net = cv2.dnn.readNet("yolo_data/yolov3.weights", "yolo_data/yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layer_indexes = net.getUnconnectedOutLayers().flatten() - 1
    output_layers = [layer_names[i] for i in output_layer_indexes]
    classes = [line.strip() for line in open("yolo_data/coco.names")]

    # Consider bird class
    bird_classes = ["bird"]

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                class_name = classes[class_id]
                if class_name in bird_classes:
                    print(f"Detected: {class_name}")
                    return True
    return False
