from vision.camera import Camera
from vision.pose_estimation import PoseEstimator
from fuzzy.fuzzy_system import FuzzySystem
from collections import deque
import time
import cv2
import math
from playsound import playsound
import threading
import requests

# ---------- TELEGRAM CONFIG ----------
BOT_TOKEN = "8515010900:AAGcf13k4ZcTmFiMMj55g20Lg6qdVac4cvQ"
CHAT_ID = "5072631321"

# ---------- GLOBAL UNTUK MOUSE ----------
dragging = False
start_x, start_y = -1, -1

danger_zone = {
    "x1": 100,
    "y1": 100,
    "x2": 400,
    "y2": 350
}

# ---------- GLOBAL UNTUK ALARM ----------
alarm_active = False
alarm_thread = None
telegram_sent = False


def play_alarm():
    global alarm_active
    while alarm_active:
        playsound("assets/beep4.wav")
        time.sleep(0.2)


# ===== TELEGRAM ASYNC (ANTI FRAME DROP) =====
def send_telegram_async(distance, speed):
    message = (
        "🚨 *PERINGATAN AREA BERBAHAYA!* 🚨\n\n"
        "Segera lakukan pengawasan!"
    )
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, data=data, timeout=3)
    except Exception as e:
        print("Telegram error:", e)
# =========================================


def distance_to_fence(cx, cy, x1, y1, x2, y2):
    dx = max(x1 - cx, 0, cx - x2)
    dy = max(y1 - cy, 0, cy - y2)
    return math.sqrt(dx * dx + dy * dy)


def mouse_callback(event, x, y, flags, param):
    global dragging, start_x, start_y, danger_zone

    if event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        danger_zone["x1"] = min(start_x, x)
        danger_zone["y1"] = min(start_y, y)
        danger_zone["x2"] = max(start_x, x)
        danger_zone["y2"] = max(start_y, y)

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False


def main():
    global alarm_active, alarm_thread, telegram_sent

    camera = Camera()
    pose_estimator = PoseEstimator()
    fuzzy = FuzzySystem()

    status_buffer = deque(maxlen=15)

    cv2.namedWindow("Pose Check")
    cv2.setMouseCallback("Pose Check", mouse_callback)

    prev_point = None

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        pose_point = pose_estimator.process(frame)

        # Gambar danger zone
        cv2.rectangle(
            frame,
            (danger_zone["x1"], danger_zone["y1"]),
            (danger_zone["x2"], danger_zone["y2"]),
            (0, 0, 255),
            2
        )

        speed = 0
        distance = 0
        status = "AMAN"
        color = (0, 255, 0)
        risk_value = 0

        if pose_point:
            cx, cy = pose_point

            # HITUNG KECEPATAN
            if prev_point is not None:
                px, py = prev_point
                speed = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
            prev_point = (cx, cy)

            # HITUNG JARAK
            distance = distance_to_fence(
                cx, cy,
                danger_zone["x1"],
                danger_zone["y1"],
                danger_zone["x2"],
                danger_zone["y2"]
            )

            # FUZZY EVALUATION
            risk_value = fuzzy.evaluate(distance, speed)

            # BUFFER STATUS
            if risk_value >= 65:
                status_buffer.append(1)
            else:
                status_buffer.append(0)

            # ---------- LOGIKA ALARM STABIL ----------
            if sum(status_buffer) >= 10:
                if not alarm_active:
                    alarm_active = True
                    telegram_sent = False
            else:
                alarm_active = False
                telegram_sent = False

            # ---------- TELEGRAM THREAD (ANTI DROP FRAME) ----------
            if alarm_active and not telegram_sent:
                threading.Thread(
                    target=send_telegram_async,
                    args=(distance, speed),
                    daemon=True
                ).start()
                telegram_sent = True

            # ---------- ALARM THREAD ----------
            if alarm_active:
                if alarm_thread is None or not alarm_thread.is_alive():
                    alarm_thread = threading.Thread(
                        target=play_alarm,
                        daemon=True
                    )
                    alarm_thread.start()

            # STATUS VISUAL
            if risk_value < 40:
                status = "AMAN"
                color = (0, 255, 0)
            elif risk_value < 70:
                status = "WASPADA"
                color = (0, 255, 255)
            else:
                status = "BAHAYA"
                color = (0, 0, 255)

            cv2.putText(
                frame,
                f"{status} ({risk_value:.1f})",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            # ===== INI YANG TADI HILANG (SUDAH DIKEMBALIKAN) =====
            cv2.putText(
                frame,
                f"Jarak: {int(distance)} px",
                (30, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Kecepatan: {int(speed)} px/frame",
                (30, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 200, 0),
                2
            )
            # ===================================================

            if alarm_active:
                cv2.putText(
                    frame,
                    "ALARM AKTIF!",
                    (30, 145),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

            cv2.circle(frame, (cx, cy), 6, (255, 255, 255), -1)

        cv2.putText(
            frame,
            "Drag mouse to set danger zone",
            (30, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            2
        )

        cv2.imshow("Pose Check", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    alarm_active = False
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
