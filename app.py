import cv2, json, interface
from flask import Flask, Response, render_template, jsonify

class App:
    def __init__(self, name) -> None:
        self.app: Flask = Flask(name)
        self.complemented: bool = False
        self.interface = interface.Interface('COM10', 9600, 0.1)

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/video_feed')
        def video_feed() -> Response:
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/ProcessUserinfo/<string:userinfo>', methods=['POST'])
        def ProcessUserinfo(userinfo: str):
            userinfo = json.loads(userinfo)
            if userinfo == 'c' or userinfo == 'C':
                self.complemented = not self.complemented
            else:
                self.interface.write(userinfo)
            return('/')

        @self.app.route('/ProcessSendinfo', methods=['GET'])
        def ProcessSendinfo():
            value = self.interface.read()
            if len(value) != 3:
                data = {"TEMP": "", "DISTL": "", "DISTR": ""}
            else:
                data = {"TEMP": value[0], "DISTL": value[1], "DISTR": value[2]}
            
            return jsonify(data)
    
    def run(self) -> None:
        self.app.run(debug=True)
        self.interface.open()
        

    def gen_frames(self) -> None:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            elif self.complemented:
                # frame = self.complementary_effect(frame)
                frame = 255 - frame
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    
    
        cap.release()
        cv2.destroyAllWindows()
    
    def complementary_effect(self, frame: cv2.Mat) -> cv2.Mat:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Mask for four color
        maskR = cv2.inRange(hsv, ( 0, 50, 70), ( 9, 255, 255))
        maskG = cv2.inRange(hsv, (36, 50, 70), (89, 255, 255))
        maskB = cv2.inRange(hsv, (25, 50, 70), (130,255, 255))
        maskY = cv2.inRange(hsv, (110,50, 50), (130,255, 255))
        mask = cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(maskG, maskY), maskR), maskB)
        imgs = cv2.bitwise_and(frame, frame, mask)
        return 255 -imgs

def main():
    server = App(__name__)
    server.run()

if __name__ == '__main__':
    main()
