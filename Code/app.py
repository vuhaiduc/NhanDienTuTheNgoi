import os
import tempfile
import time
import math as m
import cv2
import mediapipe as mp
import subprocess
from flask import Flask, Response, render_template, jsonify
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
import threading

app = Flask(__name__)

def findDistance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def findAngle(x1, y1, x2, y2):
    try:
        theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
        return int(180 / m.pi * theta)
    except:
        return 90

def sendWarning(message):
    try:
        tts = gTTS(text=message, lang='vi')
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "warning.mp3")
        tts.save(file_path)

        if not os.path.exists(file_path):
            print("Không thể tạo file âm thanh!")
            return

        print(f"Đường dẫn file: {file_path}")
        print("Đang phát âm thanh...")

        # Phát âm thanh bằng trình phát mặc định
        player = subprocess.Popen(["start", file_path], shell=True)

        # Chờ file phát xong trước khi xóa
        time.sleep(5)

        print("Xóa file âm thanh...")
        os.remove(file_path)

    except Exception as e:
        print(f"Lỗi: {e}")

good_frames = 0
bad_frames = 0
good_posture_time = 0  # Thời gian ngồi đúng tư thế (giây)
bad_posture_time = 0   # Thời gian ngồi sai tư thế (giây)

font = cv2.FONT_HERSHEY_SIMPLEX
green = (127, 255, 0)
red = (50, 50, 255)

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

error_message = ""

def draw_text(image, text, position, font_path, font_size, color):
    # Chuyển đổi hình ảnh OpenCV sang định dạng Pillow
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    
    # Tải font chữ hỗ trợ tiếng Việt
    font = ImageFont.truetype(font_path, font_size)
    
    # Vẽ văn bản lên hình ảnh
    draw.text(position, text, font=font, fill=color)
    
    # Chuyển đổi hình ảnh Pillow trở lại định dạng OpenCV
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

def generate_frames():
    global good_frames, bad_frames, error_message, good_posture_time, bad_posture_time
    cap = cv2.VideoCapture('http://192.168.1.4:4747/video')
    
    # Đường dẫn đến font chữ hỗ trợ tiếng Việt (ví dụ: Arial Unicode MS)
    font_path = "arial.ttf"  # Thay đổi đường dẫn này nếu cần
    font_size = 30

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        h, w = image.shape[:2]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        error_message = ""

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            keypoints = {landmark.name: (int(lm[landmark].x * w), int(lm[landmark].y * h)) for landmark in mp_pose.PoseLandmark}

            # Kiểm tra xem các điểm keypoint cần thiết có tồn tại không
            if 'LEFT_SHOULDER' in keypoints and 'NOSE' in keypoints and 'LEFT_HIP' in keypoints:
                neck_inclination = findAngle(keypoints['LEFT_SHOULDER'][0], keypoints['LEFT_SHOULDER'][1], keypoints['NOSE'][0], keypoints['NOSE'][1])
                torso_inclination = findAngle(keypoints['LEFT_HIP'][0], keypoints['LEFT_HIP'][1], keypoints['LEFT_SHOULDER'][0], keypoints['LEFT_SHOULDER'][1])

                # Đảm bảo giá trị góc hợp lệ
                neck_inclination = min(max(neck_inclination, 0), 90)
                torso_inclination = min(max(torso_inclination, 0), 90)

                color = green if (neck_inclination < 40 and torso_inclination < 10) else red

                if color == green:
                    bad_frames = 0
                    good_frames += 1
                    # Cập nhật thời gian ngồi đúng tư thế
                    good_posture_time = good_frames // 30  # Giả sử 30 FPS, chuyển đổi khung hình thành giây
                    posture_time = good_posture_time
                    posture_status = "Đúng tư thế"
                else:
                    good_frames = 0
                    bad_frames += 1
                    # Cập nhật thời gian ngồi sai tư thế
                    bad_posture_time = bad_frames // 30  # Giả sử 30 FPS, chuyển đổi khung hình thành giây
                    posture_time = bad_posture_time
                    posture_status = "Sai tư thế"

                # Hiển thị góc nghiêng cổ và lưng bằng tiếng Việt
                neck_text = f"Cổ: {neck_inclination}°"
                torso_text = f"Lưng: {torso_inclination}°"
                image = draw_text(image, neck_text, (10, 30), font_path, font_size, color)
                image = draw_text(image, torso_text, (10, 70), font_path, font_size, color)

                # Hiển thị thời gian và trạng thái ở góc dưới bên trái
                text = f"{posture_status}: {posture_time}s"
                text_position = (10, h - 50)  # Góc dưới bên trái
                image = draw_text(image, text, text_position, font_path, font_size, color)

                # Hiển thị thời gian hiện tại ở góc dưới bên phải
                current_time = datetime.now().strftime("%H:%M:%S")  # Lấy thời gian hiện tại
                time_text = f"Thời gian: {current_time}"
                time_text_size = cv2.getTextSize(time_text, font, 0.9, 2)[0]
                time_text_position = (w - time_text_size[0] - 10, h - 50)  # Góc dưới bên phải
                image = draw_text(image, time_text, time_text_position, font_path, font_size, color)

                if color == red:
                    if neck_inclination >= 40:
                        error_message += "Cổ quá cúi. "
                    if torso_inclination >= 10:
                        error_message += "Lưng quá nghiêng. "

                # Vẽ các kết nối và điểm keypoint (chỉ vẽ nếu các điểm tồn tại)
                connections = [
                    # Kết nối phần thân
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
                    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
                    (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
                    (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
                    (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
                    (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.NOSE),
                    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.NOSE),
                    (mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.LEFT_EAR),
                    (mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.RIGHT_EAR),

                    # Kết nối cánh tay
                    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
                    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
                    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
                    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
                ]

                for point1, point2 in connections:
                    if point1.name in keypoints and point2.name in keypoints:
                        cv2.line(image, keypoints[point1.name], keypoints[point2.name], color, 3)

                # Vẽ các điểm keypoint (chỉ vẽ nếu điểm tồn tại)
                for point_name, point in keypoints.items():
                    cv2.circle(image, point, 5, color, -1)

                if bad_frames > 180:
                    # Chạy hàm sendWarning trong một luồng riêng biệt
                    warning_thread = threading.Thread(target=sendWarning, args=(error_message,))
                    warning_thread.start()
                    bad_frames = 0
            else:
                image = draw_text(image, "Không thể nhận diện tư thế", (10, 30), font_path, font_size, red)

        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_error')
def get_error():
    return jsonify(error_message=error_message)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)