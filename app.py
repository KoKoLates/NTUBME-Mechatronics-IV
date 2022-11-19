from camera import VideoCamera
from flask import Flask, render_templates, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_templates('index.html')

def gen(camera) -> None:
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), 
                    mimetype='mu;tipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0,0,0,0')