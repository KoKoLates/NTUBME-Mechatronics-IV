import cv2, json
import interface
from flask import Flask, Response, jsonify, render_template

app = Flask(__name__)
cap = cv2.VideoCapture(0)

def gen_frames() -> None:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
    cv2.destroyAllWindows()

def complementary():
    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask for four color
        maskR = cv2.inRange(hsv, ( 0, 50, 70), ( 9, 255, 255))
        maskG = cv2.inRange(hsv, (36, 50, 70), (89, 255, 255))
        maskB = cv2.inRange(hsv, (25, 50, 70), (130,255, 255))
        maskY = cv2.inRange(hsv, (110,50, 50), (130,255, 255))

        mask = cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(maskG, maskY), maskR), maskB)
        imgs = cv2.bitwise_and(frame, frame, mask)
        image = 255 - imgs
        ret, buffer = cv2.imencode('.jpg', image)
        image = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
    
@app.route('/')
def index() -> str:
    # interface.open('COM3', 9600, 0.1)    
    return render_template('index.html')

@app.route('/video_feed')
def video_feed() -> Response:
    return Response(gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# The route function for color complementary use.
@app.route('/complementary_feed')
def complementary_feed() -> Response:
    return Response(complementary(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ProcessUserinfo/<string:userinfo>', methods=['POST'])
def ProcessUserinfo(userinfo: str):
    userinfo = json.loads(userinfo)
    # print(userinfo)
    # interface.write(userinfo)
    return('/')

if __name__ == '__main__':
    app.run(debug=True)