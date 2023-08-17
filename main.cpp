#include <opencv2/dnn.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <fstream>

int main() {
    // Load YOLO
    cv::dnn::Net net = cv::dnn::readNet("yolov3.weights", "yolov3.cfg");
    net.setPreferableBackend(cv::dnn:: DNN_BACKEND_OPENCV);
    net.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);

    // Load names of classes (birds in this case)
    std::vector<std::string> classes;
    std::ifstream ifs("coco.names");
    std::string line;
    while (std::getline(ifs, line)) classes.push_back(line);

    // Read image
    cv::Mat img = cv::imread("bird.jpg");
    cv::Mat blob;

    // Set up input
    cv::dnn::blobFromImage(img, blob, 1 / 255.0, cv::Size(416, 416), cv::Scalar(0,0,0), true, false);
    net.setInput(blob);

    // Run forward pass
    std::vector<cv::Mat> outs;
    net.forward(outs, net.getUnconnectedOutLayersNames());

    // Information for showing boxes (Class id, confidence, bounding box coordinates)
    std::vector<int> classIds;
    std::vector<float> confidences;
    std::vector<cv::Rect> boxes;

    for (size_t i = 0; i < outs.size(); ++i) {
        // data for first detection (4 bounding box + 1 confidence + 80 class probabilities)
        float* data = (float*)outs[i].data;

        for (int j = 0; j < outs[i].rows; ++j, data += outs[i].cols) {
            cv::Mat scores = outs[i].row(j).colRange(5, outs[i].cols);
            cv::Point classIdPoint;
            double confidence;

            // Get the value and location of the maximum score
            cv::minMaxLoc(scores, 0, &confidence, 0, &classIdPoint);
            if (confidence > 0.5 && classes[classIdPoint.x] == "bird") {
                // Scale bounding box coordinates to the size of the image
                int centerX = (int)(data[0] * img.cols);
                int centerY = (int)(data[1] * img.rows);
                int width = (int)(data[2] * img.cols);
                int height = (int)(data[3] * img.rows);
                int left = centerX - width / 2;
                int top = centerY - height / 2;

                classIds.push_back(classIdPoint.x);
                confidences.push_back((float)confidence);
                boxes.push_back(cv::Rect(left, top, width, height));
            }
        }
    }

    // Apply non-max suppression
    std::vector<int> indices;
    cv::dnn::NMSBoxes(boxes, confidences, 0.5, 0.4, indices);

    // Draw bounding boxes
    for (int idx : indices) {
        cv::Rect box = boxes[idx];
        int classId = classIds[idx];
        cv::rectangle(img, box, cv::Scalar(0, 255, 0), 2);
        std::string label = classes[classId];
        cv::putText(img, label, box.tl(), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0,255,0), 2);
    }

    // Show the image with detections
    cv::imshow("Bird Detection", img);
    cv::waitKey();

    return 0;
}
