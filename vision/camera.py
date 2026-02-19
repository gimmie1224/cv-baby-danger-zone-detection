import cv2

class Camera:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def display(self, frame, text=None):
        if text:
            cv2.putText(
                frame,
                f"Status: {text}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        cv2.imshow("Monitoring Area Bayi", frame)

    def is_exit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
