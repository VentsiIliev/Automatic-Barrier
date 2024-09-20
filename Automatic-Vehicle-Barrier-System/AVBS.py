import sys
import threading
import traceback
from datetime import datetime

import cv2
from PyQt5.QtWidgets import QApplication

from API.BarrierControl import BarrierControl
from API.Database import Database
from API.LicensePlateRecognizer import LicensePlateRecognizer
from API.SingletonDatabase import SingletonDatabase
from API.VehicleDetection import VehicleDetection
from AVBSWindow.AVBSWindow import AVBSWindow
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

        # Access control setup
        # self.database = Database("database/access_events_logs.csv")
        if self.enforce_access_control:
            working_hours = f"{self.system_settings[SystemSetting.WORKDAY_START_TIME.value]}-{self.system_settings[SystemSetting.WORKDAY_END_TIME.value]}"
            self.access_control = AccessControl( working_hours)

        self.barrier = Barrier()
        self.barrier_control = BarrierControl(self.barrier)

        self.camera = Camera(self.camera_settings)
        self.vehicles_on_premises = []

        # Initialize the UI with barrier control
        # Create a thread for running the main processing loop
        self.ui = None
        self.app = None
        processing_thread = threading.Thread(target=self.run, daemon=True)
        processing_thread.start()

        self.initUI(self.barrier_control)

    def run(self):
        while self.ui is None:
            pass
        try:
            while True:
                frame = self.camera.capture()
                if frame is None:
                    print("Failed to grab frame")
                    continue  # Skip to the next iteration instead of breaking the loop

                print("Frame grabbed successfully")
                self.ui.update_camera_feed(frame)
                vehicle_detected_region = self.vehicle_detection.detect_vehicle(frame)

                if vehicle_detected_region is not None:
                    if self.barrier_control.get_status():
                        continue

                    license_plate = self.license_plate_recognizer.recognize(vehicle_detected_region)

                    if license_plate:
                        direction = self.get_vehicle_direction(license_plate)
                        access_granted = self.check_access_control(license_plate, direction)

                        if access_granted:
                            self.update_vehicle_on_premises(license_plate, direction)
                            self.barrier_control.open()
                            event = AccessEvent(AccessEventType.GRANTED, datetime.now(), license_plate, direction)
                        else:
                            self.barrier_control.deny_access()
                            event = AccessEvent(AccessEventType.DENIED, datetime.now(), license_plate, direction)

                        SingletonDatabase().getInstance().log_event(event)
                        self.ui.update_info_panel(event, vehicle_detected_region, len(self.vehicles_on_premises))
                else:
                    if self.barrier_control.get_status():
                        self.barrier_control.close()

                # Handle key press (ESC to quit)
                # if cv2.waitKey(1) & 0xFF == 27:
                #     self.settings_manager.save_settings()
                #     break
        except Exception as e:
            traceback.print_exc()


    def check_access_control(self, license_plate, direction):
        """ Check if access should be granted based on the current settings. """
        if not self.enforce_access_control:
            return True
        if direction == "IN":
            return self.access_control.check_access(license_plate)
        elif direction == "OUT":
            return license_plate in self.vehicles_on_premises

    def update_vehicle_on_premises(self, license_plate, direction):
        """ Update the list of vehicles currently on premises. """
        if direction == "IN":
            self.vehicles_on_premises.append(license_plate)
        elif direction == "OUT" and license_plate in self.vehicles_on_premises:
            self.vehicles_on_premises.remove(license_plate)

    def get_vehicle_direction(self, license_plate):
        """ Determine whether the vehicle is entering or exiting. """
        return "OUT" if license_plate in self.vehicles_on_premises else "IN"

    def initUI(self, barrier_control):
        """ Initialize the GUI and connect it with the barrier control """
        self.app = QApplication(sys.argv)
        window = AVBSWindow(barrier_control)
        self.ui = window
        window.show()
        # Do not exit the app here



