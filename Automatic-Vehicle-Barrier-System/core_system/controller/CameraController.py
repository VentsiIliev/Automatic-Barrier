class CameraController:
    def __init__(self, camera):
        self.camera = camera

    def restart_camera(self,settings):
        self.camera.restart(settings)
