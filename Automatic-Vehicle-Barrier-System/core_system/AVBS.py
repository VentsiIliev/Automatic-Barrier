import sys
import threading
import traceback
from datetime import datetime

import cv2
from PyQt5.QtWidgets import QApplication

from core_system.API.BarrierControl import BarrierControl
from core_system.API.LicensePlateRecognizer import LicensePlateRecognizer
from core_system.controller.CameraController import CameraController
from shared.SingletonDatabase import SingletonDatabase
from core_system.API.VehicleDetection import VehicleDetection
from core_system.view.AVBSWindow.AVBSWindow import AVBSWindow
from core_system.config.settings.SystemSetting import SystemSetting
from core_system.config.settings.SettingsManager import SettingsManager
from core_system.model.Barrier import Barrier
from core_system.model.Camera import Camera
from core_system.model.LicencePlateDetector import LicencePlateDetector
from core_system.model.LicensePlateReader import LicensePlateReader
from core_system.model.VehicleDetector import VehicleDetector
from core_system.API.AccessControl import AccessControl
from shared.AccessEvent import AccessEvent
from shared.AccessEventType import AccessEventType


class AVBS:
    ERROR_MESSAGE_CAMERA_FAILED = "Could not capture frame from camera.\n Possibe reasons: \n 1. Camera is not connected \n 2. Camera is being used by another application \n 3. Camera is not working properly"
    YOLOVN8_MODEL_PATH = "core_system/assets/models/yolov8n.pt"
    LICENSE_PLATE_DETECTOR_MODEL_PATH = "core_system/assets/models/license_plate_detector.pt"
    LICENSE_PLATE_READER_PATTHERN = "^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$"
    def __init__(self):
        # Initialize components

        self.settings_manager = SettingsManager()
        # self.settings = self.settings_manager.load_all_settings()
        # self.system_settings = self.settings.get_system_settings()
        self.camera_settings = self.settings_manager.camera_settings
        # self.access_control_settings = self.settings_manager.access_control_settings
        # self.date_time_settings = self.settings_manager.date_time_settings

        self.vehicle_detector = VehicleDetector(self.YOLOVN8_MODEL_PATH)
        self.vehicle_detection = VehicleDetection(self.vehicle_detector)
        self.license_plate_detector = LicencePlateDetector(self.LICENSE_PLATE_DETECTOR_MODEL_PATH)
        self.license_plate_reader = LicensePlateReader(self.LICENSE_PLATE_READER_PATTHERN)
        self.license_plate_recognizer = LicensePlateRecognizer(self.license_plate_detector, self.license_plate_reader)

        # Access control setup
        # self.database = Database("database/access_events_logs.csv")
        if self.settings_manager.get_enforce_access_control():
            working_hours = f"{self.settings_manager.get_workday_start_time()}-{self.settings_manager.get_workday_end_time()}"
            self.access_control = AccessControl(working_hours)

        self.barrier = Barrier()
        self.barrier_control = BarrierControl(self.barrier)
        self.camera = Camera(self.camera_settings)
        self.camera_controller = CameraController(self.camera)
        self.vehicles_on_premises = []

        # Initialize the UI with barrier control
        # Create a thread for running the main processing loop
        self.ui = None
        self.app = None
        processing_thread = threading.Thread(target=self.run, daemon=True)
        processing_thread.start()

        try:
            self.initUI(self.barrier_control,self.camera_controller)
        except Exception as e:
            traceback.print_exc()
            # exit
            sys.exit(1)

    def run(self):
        while self.ui is None:
            pass
        try:
            while True:
                print(self.settings_manager.get_enforce_access_control())
                frame = self.camera.capture()
                if frame is None:
                    # self.ui.show_error_message(self.ERROR_MESSAGE_CAMERA_FAILED)
                    continue  # Skip to the next iteration instead of breaking the loop

                self.ui.update_camera_feed(frame)
                # vehicle_detected_region = self.vehicle_detection.detect_vehicle(frame)

                # if vehicle_detected_region is not None:
                #     if self.barrier_control.get_status():
                #         continue
                #resize the frame
                frame = cv2.resize(frame, (640, 480))
                license_plate = self.license_plate_recognizer.recognize(frame)

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
                    self.ui.update_info_panel(event, frame, len(self.vehicles_on_premises))
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
        if not self.settings_manager.get_enforce_access_control():
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

    def initUI(self, barrier_control,camera_controller):
        """ Initialize the GUI and connect it with the barrier control """
        self.app = QApplication(sys.argv)
        window = AVBSWindow(barrier_control, self.settings_manager,camera_controller)
        self.ui = window
        window.show()
        # Do not exit the app here

    def camera_settings_changed(self):
        """ Update the camera settings and restart the camera feed. """
        self.camera.restart()
