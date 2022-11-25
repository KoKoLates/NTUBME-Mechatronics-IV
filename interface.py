import serial

class Interface(object):
    def __init__(self) -> None:
        self.ser = serial.Serial('COM3', 9600, timeout=0.1)
        self.ser.open()

        # create a dictionary for mission
        self.list = {'w': 1, 'd': 2, 'a': 3, 's': 4}

    # def __del__(self) -> None:
    #     self.ser.close()

    def read(self) -> None:
        try:
            response = self.ser.readline().decode().rstrip()
            print(response)
        except:
            print('error')

    def write(self, event: str) -> None:
        mission = 0
        if event in self.list:
            mission = self.list[event]

        self.ser.write(b'%d\n' %mission)
        print(mission)
        






