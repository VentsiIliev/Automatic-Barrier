from core_system.config.settings.BaseSettings import Settings


class CameraSettings(Settings):
    def __init__(self):
        super().__init__()
        # Initialize default camera settings
        self.set_value("index", 1)
        self.set_value("width", 1280)
        self.set_value("height", 720)

    def set_camera_index(self, index):
        """Set the camera index."""
        self.set_value("index", index)

    def get_camera_index(self):
        """Get the camera index."""
        return self.get_value("index")

    def get_camera_width(self):
        """Get the camera width."""
        return self.get_value("width")

    def get_camera_height(self):
        """Get the camera height."""
        return self.get_value("height")

    def set_resolution(self, width, height):
        """Set the camera resolution."""
        self.set_value("width", width)
        self.set_value("height", height)

    def set_width(self, width):
        """Set the camera width."""
        self.set_value("width", width)

    def set_height(self, height):
        """Set the camera height."""
        self.set_value("height", height)

    def get_resolution(self):
        """Get the camera resolution."""
        return (self.get_value("width"), self.get_value("height"))

    def display_settings(self):
        """Utility method to display the camera settings."""
        index = self.get_camera_index()
        width, height = self.get_resolution()
        print(f"Camera Index: {index}")
        print(f"Resolution: {width}x{height}")
