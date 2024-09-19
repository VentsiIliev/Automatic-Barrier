from datetime import datetime

import cv2
import numpy as np

from API.BarrierControl import BarrierControl
from API.Database import Database
from API.LicensePlateRecognizer import LicensePlateRecognizer
from API.VehicleDetection import VehicleDetection
from config.SystemSetting import SystemSetting
from config.SettingsManager import SettingsManger
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
        self.settings_manager = SettingsManger()
        self.settings = self.settings_manager.load_all_settings()
        self.system_settings = self.settings.get_system_settings()
        self.camera_settings = self.settings.get_camera_settings()
        self.enforce_access_control = self.system_settings[SystemSetting.ENFORCE_ACCESS_CONTROL.value]
        self.vehicle_detector = VehicleDetector("assets/models/yolov8n.pt")
        self.vehicle_detection = VehicleDetection(self.vehicle_detector)
        self.license_plate_detector = LicencePlateDetector("assets/models/license_plate_detector.pt")
        self.license_plate_reader = LicensePlateReader("^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$")
        self.license_plate_recognizer = LicensePlateRecognizer(self.license_plate_detector, self.license_plate_reader)
        if self.enforce_access_control:
            working_hours = f"{self.system_settings[SystemSetting.WORKDAY_START_TIME.value]}-{self.system_settings[SystemSetting.WORKDAY_END_TIME.value]}"
            self.access_control = AccessControl("database/whitelisted_vehicles.csv", working_hours)
        self.barrier = Barrier()
        self.barrier_control = BarrierControl(self.barrier)
        self.database = Database("database/access_events_logs.csv")
        self.camera = Camera(self.camera_settings)
        self.vehicles_on_premises = []
        # self.camera = cv2.VideoCapture('assets/videos/sample2.mp4')

    def run(self):
        info_image = np.zeros((800, 800, 3), dtype="uint8")
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
                        direction = self.get_vehicle_direction(license_plate)
                        if direction == "IN":
                            self.vehicles_on_premises.append(license_plate)
                            access_granted = self.access_control.check_access(license_plate)
                        elif direction == "OUT":
                            if license_plate in self.vehicles_on_premises:
                                self.vehicles_on_premises.remove(license_plate)
                                access_granted = True
                            else:
                                access_granted = False
                    else:
                        access_granted = True
                    if access_granted:
                        # Lift barrier
                        self.barrier_control.open()

                        # Log access event
                        event = AccessEvent(AccessEventType.GRANTED, datetime.now(), license_plate, direction)
                    else:
                        # Deny access
                        self.barrier_control.deny_access()
                        # Log access event
                        event = AccessEvent(AccessEventType.DENIED, datetime.now(), license_plate, direction)

                    self.database.log_event(event)

                    info_image = self.draw_info(info_image, event, vehicle_detected_region)
                    # Display the info_image in a separate window

            else:
                if self.barrier_control.get_status():
                    self.barrier_control.close()
                    info_image = np.zeros((800, 800, 3), dtype="uint8")

            cv2.imshow('Info', info_image)
            cv2.imshow('frame', frame)

            # on escape key press save settings and quit
            if cv2.waitKey(1) & 0xFF == 27:
                self.settings_manager.save_settings()
                break

    def draw_info(self, info_image, event, image):
        # Resize the passed image to fit into the info_image
        resized_image = cv2.resize(image, (300, 300))
        # Place the resized image onto the info_image
        info_image[0:300, 0:300] = resized_image
        # draw info on info_image
        if event.type == AccessEventType.GRANTED:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        cv2.putText(info_image, event.type.name, (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(info_image, event.time.strftime('%Y-%m-%d %H:%M:%S'), (350, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, 2)
        cv2.putText(info_image, event.registration_number, (350, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(info_image, event.direction, (350, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        # at bottom left corner display the number of vehicles on premises
        cv2.putText(info_image, f"Vehicles on premises: {len(self.vehicles_on_premises)}", (350, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return info_image

    def get_vehicle_direction(self, registration_number):
        if registration_number in self.vehicles_on_premises:
            return "OUT"
        else:
            return "IN"
