import mediapipe as mp
import cv2

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if results.pose_landmarks:
            # =========================
            # GAMBAR SKELETON POSE
            # =========================
            self.mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

            # =========================
            # HITUNG TITIK TENGAH PINGGUL
            # =========================
            landmarks = results.pose_landmarks.landmark

            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]

            h, w, _ = frame.shape
            cx = int((left_hip.x + right_hip.x) / 2 * w)
            cy = int((left_hip.y + right_hip.y) / 2 * h)

            # =========================
            # GAMBAR TITIK PUSAT
            # =========================
            cv2.circle(frame, (cx, cy), 6, (255, 0, 0), -1)

            return cx, cy

        return None
