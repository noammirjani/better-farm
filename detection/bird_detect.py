import cv2
import argparse
import numpy as np


config_path = "yolo_data/yolov3.cfg"
weights_path = "yolo_data/yolov3.weights"
classes_path = "yolo_data/coco.names"


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help='path to input image')
    ap.add_argument('-c', '--config', required=True, help='path to yolo config file')
    ap.add_argument('-w', '--weights', required=True, help='path to yolo pre-trained weights')
    ap.add_argument('-cl', '--classes', required=True, help='path to text file containing class names')
    return ap.parse_args()


# Reads the image and sets up YOLO for object detection.
def read_and_preprocess(image_path, config_path, weights_path, classes_path):
    image = cv2.imread(image_path)
    Width, Height = image.shape[1], image.shape[0]
    scale = 0.00392

    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    net = cv2.dnn.readNet(weights_path, config_path)
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    return image, Width, Height, classes, COLORS, net


# Retrieves YOLO output layers.
def get_output_layers(net):
    layer_names = net.getLayerNames()
    return [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]


# Draws bounding boxes for detected objects.
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, COLORS):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


# Processes YOLO detections.
def process_detections(net, image, Width, Height, classes, COLORS):
    outs = net.forward(get_output_layers(net))
    class_ids, confidences, boxes = [], [], []
    conf_threshold, nms_threshold = 0.5, 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x, center_y, w, h = int(detection[0] * Width), int(detection[1] * Height), int(
                    detection[2] * Width), int(detection[3] * Height)
                x, y = center_x - w / 2, center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        x, y, w, h = boxes[i]
        draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h), classes,
                          COLORS)

    return image


# Updates image with detected objects.
def update_image(image):
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    Width, Height = image.shape[1], image.shape[0]
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    net = cv2.dnn.readNet(weights_path, config_path)
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    return process_detections(net, image, Width, Height, classes, COLORS)


# Detects birds in an image using YOLO.
def detect_birds_in_image(image_path, config_path, weights_path, classes_path):
    image, Width, Height, classes, COLORS, net = read_and_preprocess(image_path, config_path, weights_path,
                                                                     classes_path)
    processed_image = process_detections(net, image, Width, Height, classes, COLORS)
    cv2.imshow("object detection", processed_image)
    cv2.waitKey()
    cv2.imwrite("object-detection.jpg", processed_image)
    cv2.destroyAllWindows()
    return processed_image


# Detects birds in a video frame.
def detect_bird(frame):
    net = cv2.dnn.readNet(weights_path, config_path)
    layer_names = net.getLayerNames()
    output_layer_indexes = net.getUnconnectedOutLayers().flatten() - 1
    output_layers = [layer_names[i] for i in output_layer_indexes]
    classes = [line.strip() for line in open(classes_path)]

    bird_classes = ["bird"]

    height, width, channels = frame.shape

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


def main():
    args = parse_arguments()
    detect_birds_in_image(args.image, args.config, args.weights, args.classes)


if __name__ == "__main__":
    main()
