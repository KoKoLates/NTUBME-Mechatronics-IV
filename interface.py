import serial

class Interface:
    def __init__(self, COM_PORT: str, BAUD_RATES: int, TIME_OUT: float) -> None:
        self.port: str = COM_PORT
        self.baud: int = BAUD_RATES
        self.timeout: float = TIME_OUT
        self.ser: serial.Serial = None
        self.mission = {'ArrowUp': 1, 'ArrowRight': 2, 'ArrowLeft': 3, 'ArrowDown': 4, '+': 5}
    
    def open(self) -> None:
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
            self.ser.flush()
        except Exception as ex:
            print('[ERROR] Open port fail:{}/{}'.format(self.port, self.baud))
            print('[ERROR] Exception:{}'.format(ex))
    
    def open_check(self) -> None:
        if self.ser is None:
            self.open()

    def close(self) -> None:
        if self.ser is not None and self.ser.isOpen():
            self.ser.close()

    def write(self, userinfo: str) -> None:
        self.open_check()
        if self.ser.isOpen() and (userinfo in self.mission):
            self.ser.write(b'%d\n' %self.mission[userinfo])
            # print(self.mission[userinfo])

    def read(self) -> list:
        self.open_check()
        data = self.ser.readline()
        decoded_values = str(data[0:len(data)].decode('utf-8'))
        # values = decoded_values.split(',')
        # messages = []
        # for item in values:
        #     messages.append(float(item))

        # return messages
        return decoded_values
        
