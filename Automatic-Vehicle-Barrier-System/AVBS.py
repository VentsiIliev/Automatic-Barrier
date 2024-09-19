from datetime import datetime

import cv2

from API.BarrierControl import BarrierControl
from API.Database import Database
from API.LicensePlateRecognizer import LicensePlateRecognizer
from API.VehicleDetection import VehicleDetection
from model.Barrier import Barrier
from model.Camera import Camera
from model.LicencePlateDetector import LicencePlateDetector
from model.LicensePlateReader import LicensePlateReader
from model.VehicleDetector import VehicleDetector
from API.AccessControl import AccessControl
from model.access_events.AccessEvent import AccessEvent
from model.access_events.AccessEventType import AccessEventType


class AVBS:
    def __init__(self):
        # Initialize components
        self.vehicle_detector = VehicleDetector("assets/models/yolov8n.pt")
        self.vehicle_detection = VehicleDetection(self.vehicle_detector)
        self.lisense_plate_detector = LicencePlateDetector("assets/models/license_plate_detector.pt")
        self.licese_plate_reader = LicensePlateReader("^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$")
        self.license_plate_recognizer = LicensePlateRecognizer(self.lisense_plate_detector, self.licese_plate_reader)
        self.access_control = AccessControl()
        self.barrier = Barrier()
        self.barrier_control = BarrierControl(self.barrier)
        self.database = Database("logs/access_events_logs.csv")
        self.camera = Camera(1, 1280, 720)
        # self.camera = cv2.VideoCapture('assets/videos/sample2.mp4')
        self.enforce_access_control = True

    def run(self):
        while True:
            frame = self.camera.capture()
            # ret, frame = self.camera.read()
            if frame is None:
                print("failed to grab frame")
                break
            # Detect vehicle
            # resize frame
            # frame = cv2.resize(frame, (1280, 720))

            vehicle_detected_region = self.vehicle_detection.detect_vehicle(frame)

            if vehicle_detected_region is not None:

                if self.barrier_control.get_status():
                    continue

                # Recognize license plate
                license_plate = self.license_plate_recognizer.recognize(vehicle_detected_region)
                if license_plate is not None:
                    # Check access
                    if self.enforce_access_control:
                        access_granted = self.access_control.check_access(license_plate)
                    else:
                        access_granted = True
                    if access_granted:
                        # Lift barrier
                        self.barrier_control.open()

                        # Log access event
                        event = AccessEvent(AccessEventType.GRANTED, datetime.now(), license_plate)

                    else:
                        # Deny access
                        self.barrier_control.deny_access()
                        # Log access event
                        event = AccessEvent(AccessEventType.DENIED, datetime.now(), license_plate)

                    self.database.log_event(event)

                    self.draw_info(event, frame)

            else:
                if self.barrier_control.get_status():
                    self.barrier_control.close()

            cv2.imshow('frame', frame)
            cv2.waitKey(1)

    def draw_info(self, event, frame):
        # draw info on frame
        if event.type == AccessEventType.GRANTED:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        cv2.putText(frame, event.type.name, (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, event.time.strftime('%Y-%m-%d %H:%M:%S'), (400, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, event.registration_number, (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
