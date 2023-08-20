import cv2

motion_threshold = 8000


def detect_motion(current_frame, previous_frame):
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    delta_frame = cv2.absdiff(current_gray, previous_gray)
    threshold = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:
            return True

    return False


