from PySide6.QtQuick import QQuickImageProvider
import numpy as np
import cv2

from Backend.utils import toQImage

class FrameProvider(QQuickImageProvider):

    def __init__(self):
        QQuickImageProvider.__init__(self,  QQuickImageProvider.ImageType.Image)
        self._cameras = {}
    
    def open_camera(self, camera_id):
        if camera_id not in self._cameras:
             self._cameras[camera_id] = cv2.VideoCapture(camera_id)

    def requestImage(self, id, size, requestedSize):
        camera_id = int(id)

        if camera_id in self._cameras:
            ret, frame = self._cameras[camera_id].read()
            
            if not ret:
                frame = np.zeros((640, 480, 3))

        else:
            frame = np.zeros((640, 480, 3))
        
        return toQImage(frame)