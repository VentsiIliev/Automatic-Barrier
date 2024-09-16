import os

from ultralytics import YOLO
import cv2

import util
from util import get_car, read_license_plate, write_csv

results = {}

# mot_tracker = Sort()

# load models
coco_model = YOLO('assets/yolov8n.pt')
license_plate_detector = YOLO('assets/license_plate_detector.pt')

# load video
cap = cv2.VideoCapture('assets/sample2.mp4')
# cap = cv2.VideoCapture(0)
vehicles = [2, 3, 5, 7]
new_size = (640, 480)

bbox_color = (0, 255, 0)  # green
licence_plate_bbox_color = (0, 0, 255)  # red
bbox_thickness = 2
# read frames
frame_nmr = -1
ret = True


def run(frame):
    # global frame
    # frame = cv2.resize(frame, new_size)
    results[frame_nmr] = {}
    # detect vehicles
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score])
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), bbox_color, bbox_thickness)
    # detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # assign license plate to car
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, detections_)
        # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), licence_plate_bbox_color, bbox_thickness)
        if car_id != -1:

            # crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
            # cv2.imshow('license_plate_crop', license_plate_crop)
            # cv2.waitKey(0)
            # cv2.imwrite('assets/results/license_plate_crop.jpg', license_plate_crop)
            bbox = util.find_largest_(license_plate_crop)
            xx1, yy1, xx2, yy2 = bbox
            license_plate_crop = license_plate_crop[yy1:yy2, xx1:xx2]
            # process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
            # cv2.imshow('license_plate_crop', license_plate_crop_thresh)
            # cv2.waitKey(0)
            # read license plate number
            # license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
            license_plate_text,license_plate_text_score = util.tesseract_read_license_plate(license_plate_crop_thresh)
            print("license_plate_text", license_plate_text)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255),
                          bbox_thickness)
            if license_plate_text is not None:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), licence_plate_bbox_color,
                              bbox_thickness)
                # put text on the license plate
                cv2.putText(frame, license_plate_text, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)
                results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                              'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                'text': license_plate_text,
                                                                'bbox_score': score,
                                                                'text_score': license_plate_text_score}}
                # print the registration number
                # print("license_plate_text",license_plate_text)


while ret:
    # frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, new_size)
        run(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
# write results
write_csv(results, 'test.csv')
# print(results)

# # Get a list of all files in the directory
# image_files = os.listdir('assets/images')
#
# # Process each image file
# for image_file in image_files:
#     # Construct the full path to the image file
#     image_path = os.path.join('assets/images', image_file)
#
#     # Read the image using OpenCV
#     image = cv2.imread(image_path)
#
#     # Resize the image
#     image = cv2.resize(image, new_size)
#
#     # Call the run function
#     run(image)
#
#     cv2.imshow("image",image)
#     cv2.waitKey(0)
