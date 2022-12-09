#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Author: Po-Ting Ko
# Date: 2022-12-07

import cv2, json, interface
from flask import Flask, Response, render_template, jsonify

class App:
    def __init__(self, name) -> None:
        self.app: Flask = Flask(name)
        self.complemented: bool = False
        self.interface = interface.Interface('/dev/ttyACM0', 9600, 0.1)

        @self.app.route('/')
        def index():
            """
            Index of home pages
            Return
            -------
                render_template: Render a template by name with the given context.
            """
            return render_template('index.html')

        @self.app.route('/video_feed')
        def video_feed() -> Response:
            """
            The function update the video frame to indicate url
            and update frequently to let it look like video stream
            Return
            -------
                Response: The response object that is used by default in Flask
            """
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/ProcessUserinfo/<string:userinfo>', methods=['POST'])
        def ProcessUserinfo(userinfo: str):
            """
            The function to sending command that recieve from user (frontend)
            to the controller through the serial interface.
            Parameters
            ----------
                userinfo(str): the control command

            Return
            -------
                index: the home page index
            """
            userinfo = json.loads(userinfo)
            if userinfo == 'c' or userinfo == 'C':
                self.complemented = not self.complemented
            else:
                self.interface.write(userinfo)
            return('/')

        @self.app.route('/ProcessSendinfo', methods=['GET'])
        def ProcessSendinfo():
            """
            The function to sending data to frontend by JSON type.
            Return
            -------
                data: the jsonify data 
            """
            value = self.interface.read()
            if len(value) != 3:
                data = {"TEMP": "", "DISTL": "", "DISTR": ""}
            else:
                data = {"TEMP": value[0], "DISTL": value[1], "DISTR": value[2]}
            
            return jsonify(data)
    
    def run(self, host:str) -> None:
        """
        Running the backend side server.
        Parameters
        ----------
            host(str): The address string of host. 
        """
        self.app.run(debug=True, host=host)
        self.interface.open()
        
    def gen_frames(self) -> None:
        """
        Using the OpenCV library to capture the video frames from indicate camera index
        """
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            elif self.complemented:
                # get the complementary color
                frame = 255 - frame
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    
    
        cap.release()
        cv2.destroyAllWindows()

def main():
    server = App(__name__)
    server.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
