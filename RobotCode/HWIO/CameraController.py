import cv2

class CameraController():
  def __init__(self, iCameraId) -> None:
    self._cameraId = iCameraId
    self._camera = cv2.VideoCapture(self._cameraId)
  
  def __del__(self):
    self._camera.release()
  
  def getFrameFromCamera(self):
    # Capture a frame from the camera
    success, frame = self._camera.read()
    return success, frame
  
  def convertFrameToJpeg(self, iFrame):
    return cv2.imencode('.jpg', iFrame)[1].tobytes()


