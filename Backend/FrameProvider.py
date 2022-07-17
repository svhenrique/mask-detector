from Backend.utils import detect_and_predict_mask
from PySide6.QtQuick import QQuickImageProvider
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import cv2
import os

from Backend.utils import toQImage

class FrameProvider(QQuickImageProvider):

    def __init__(self):
        QQuickImageProvider.__init__(self,  QQuickImageProvider.ImageType.Image)
        self._cameras = {}
        self.face_detector = cv2.dnn.readNet(
            os.path.join("Models", "FaceDetector", "res10_300x300_ssd_iter_140000.caffemodel"),
            os.path.join("Models", "FaceDetector", "deploy.prototxt")
        )
        self.mask_detector = load_model(os.path.join("Models", "MaskDetector", "mask_detector.model"))

    def _transform_frame(self, frame):
        frame = frame.copy()

        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = imutils.resize(frame, width=400)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, self.face_detector, self.mask_detector)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Com Mascara" if mask > withoutMask else "Sem Mascara"
            color = (0, 255, 0) if label == "Com Mascara" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        return frame

    def open_camera(self, camera_id):
        if camera_id not in self._cameras:
             self._cameras[camera_id] = cv2.VideoCapture(camera_id)

    def requestImage(self, id, size, requestedSize):
        camera_id = int(id)


        if camera_id in self._cameras:
            ret, frame = self._cameras[camera_id].read()

            if not ret:
                frame = np.zeros((640, 480, 3))

            frame = self._transform_frame(frame)

        else:
            frame = np.zeros((640, 480, 3))
        
        return toQImage(frame)