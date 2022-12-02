import serial
import threading

global ser

def open(COM_PORT: str, BAUD_RATES: int, TIME_OUT: float) -> None:
    global ser 
    ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=TIME_OUT)
    if not ser.is_open:
        ser.open()
    print('done')

def write(userinfo: str) -> None:
    mission = {'0': 0, 'ArrowUp': 1, 'ArrowRight': 2, 'ArrowLeft': 3, 'ArrowDown': 4, '+': 5}
    status = ser.isOpen()
    if status and (userinfo in mission):
        ser.write(b'%d\n' %mission[userinfo])
        # print(mission[userinfo])

