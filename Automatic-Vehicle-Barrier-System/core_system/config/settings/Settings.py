class Settings:
    def __init__(self, system_settings, camera_settings):
        self.system_settings = system_settings
        self.camera_settings = camera_settings

    def get_system_settings(self):
        return self.system_settings

    def get_camera_settings(self):
        return self.camera_settings

    def set_camera_settings(self, camera_settings):
        self.camera_settings = camera_settings

    def set_system_settings(self, system_settings):
        self.system_settings = system_settings
