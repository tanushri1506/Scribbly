from flask import Flask, Response, request, jsonify, send_file
import cv2, os, time
import numpy as np
import mediapipe as mp
from collections import deque
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

streaming = True

tool_settings = {
    "brushSize": 5,
    "color": "blue",
    "shape": "free" 
}
color_map = {"blue": 0, "green": 1, "red": 2, "yellow": 3}
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]


bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

paint_window = np.ones((471, 636, 3), dtype=np.uint8) * 255


mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils


def draw_buttons(frame):
    cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    for i, (name, color) in enumerate(color_map.items()):
        x1, x2 = 160 + i * 115, 255 + i * 115
        cv2.rectangle(frame, (x1, 1), (x2, 65), colors[color], 2)
        cv2.putText(frame, name.upper(), (x1 + 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)


@app.route('/video_feed')
def video_feed():
    global streaming
    streaming = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    global bpoints, gpoints, rpoints, ypoints, paint_window

    cap = cv2.VideoCapture(0)

    drawing_shape = False
    shape_start = None

    while streaming:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        draw_buttons(frame)

        color_index = color_map.get(tool_settings["color"], 0)
        brush_size = int(tool_settings["brushSize"])
        shape = tool_settings.get("shape", "free")

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                lmList = []
                for lm in handLms.landmark:
                    lmx = int(lm.x * frame.shape[1])
                    lmy = int(lm.y * frame.shape[0])
                    lmList.append((lmx, lmy))

                mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

                index_finger = lmList[8]
                thumb = lmList[4]
                center = index_finger

                if abs(center[1] - thumb[1]) < 30:
                
                    if drawing_shape and shape_start:
                        x1, y1 = shape_start
                        x2, y2 = center
                        if shape == "rectangle":
                            cv2.rectangle(paint_window, (x1, y1), (x2, y2), colors[color_index], brush_size)
                        elif shape == "line":
                            cv2.line(paint_window, (x1, y1), (x2, y2), colors[color_index], brush_size)
                        elif shape == "circle":
                            radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                            cv2.circle(paint_window, (x1, y1), radius, colors[color_index], brush_size)
                        drawing_shape = False
                        shape_start = None
                    for lst in [bpoints, gpoints, rpoints, ypoints]:
                        lst.append(deque(maxlen=1024))

                elif center[1] <= 65:
                    
                    if 40 <= center[0] <= 140:
                        bpoints, gpoints, rpoints, ypoints = [deque(maxlen=1024) for _ in range(4)]
                        paint_window[67:, :, :] = 255
                    else:
                        for i, name in enumerate(color_map.keys()):
                            x1, x2 = 160 + i * 115, 255 + i * 115
                            if x1 <= center[0] <= x2:
                                tool_settings["color"] = name

                else:
                   
                    if shape == "free":
                        points = [bpoints, gpoints, rpoints, ypoints]
                        if not points[color_index]:
                            points[color_index].append(deque(maxlen=1024))
                        points[color_index][-1].appendleft(center)
                    else:
                        if not drawing_shape:
                            shape_start = center
                            drawing_shape = True

        
        for i, pts in enumerate([bpoints, gpoints, rpoints, ypoints]):
            for j in range(len(pts)):
                for k in range(1, len(pts[j])):
                    if pts[j][k - 1] and pts[j][k]:
                        cv2.line(frame, pts[j][k - 1], pts[j][k], colors[i], brush_size)
                        cv2.line(paint_window, pts[j][k - 1], pts[j][k], colors[i], brush_size)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()


@app.route('/canvas_feed')
def canvas_feed():
    _, buffer = cv2.imencode('.jpg', paint_window)
    return Response(buffer.tobytes(), mimetype='image/jpeg')


@app.route('/set_tools', methods=['POST'])
def set_tools():
    data = request.json
    tool_settings.update(data)
    return jsonify({"status": "success", "settings": tool_settings})


@app.route('/clear', methods=['POST'])
def clear_canvas():
    global bpoints, gpoints, rpoints, ypoints, paint_window
    bpoints, gpoints, rpoints, ypoints = [deque(maxlen=1024) for _ in range(4)]
    paint_window[:, :, :] = 255
    return jsonify({"status": "cleared"})


@app.route('/save', methods=['POST'])
def save_image():
    filename = f"drawing_{int(time.time())}.png"
    path = os.path.join('static', 'drawings')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    cv2.imwrite(filepath, paint_window)
    return send_file(filepath, as_attachment=True)


@app.route('/end_session', methods=['POST'])
def end_session():
    global streaming, bpoints, gpoints, rpoints, ypoints, paint_window
    streaming = False
    bpoints, gpoints, rpoints, ypoints = [deque(maxlen=1024) for _ in range(4)]
    paint_window[:, :, :] = 255
    return jsonify({"status": "stopped and cleared"})


@app.route('/session_status', methods=['GET'])
def session_status():
    return jsonify({"active": streaming})


if __name__ == '__main__':
    app.run(debug=True)
