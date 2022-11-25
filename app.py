import cv2, json
from flask import Flask, Response, render_template

app = Flask(__name__)

def gen_frames() -> None:
    cap = cv2.VideoCapture(0)
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

@app.route('/')
def index() -> str:
    return render_template('index.html')

@app.route('/video_feed')
def video_feed() -> Response:
    return Response(gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ProcessUserinfo/<string:userinfo>', methods=['POST'])
def ProcessUserinfo(userinfo):
    userinfo = json.loads(userinfo)
    return('/')

if __name__ == '__main__':
    app.run(debug=True)