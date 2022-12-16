#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Author: Po-Ting Ko
# Date: 2022-12-07
#

import serial

class Interface:
    def __init__(self, COM_PORT: str, BAUD_RATES: int, TIME_OUT: float) -> None:
        self.port: str = COM_PORT
        self.baud: int = BAUD_RATES
        self.timeout: float = TIME_OUT
        self.ser: serial.Serial = None
        self.mission = {'Stop': 0, 'ArrowUp': 1, 'ArrowRight': 2, 
                        'ArrowLeft': 3, 'ArrowDown': 4, '+': 5}
    
    def open(self) -> None:
        """
        Open the serial port between server side and controller
        """
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        except Exception as ex:
            print('[ERROR] Open port fail:{}/{}'.format(self.port, self.baud))
            print('[ERROR] Exception:{}'.format(ex))
    
    def open_check(self) -> None:
        """
        Serial port open status check
        """
        if self.ser is None:
            self.open()

    def close(self) -> None:
        """
        Close the serial port.
        """
        if self.ser is not None and self.ser.isOpen():
            self.ser.close()

    def write(self, userinfo: str) -> None:
        """
        Write the data (command) to the controller
        Parameter
            userinfo(str): the command of indicate mission
        """
        self.open_check()
        if self.ser.isOpen() and (userinfo in self.mission):
            self.ser.write(b'%d\n' %self.mission[userinfo])

    def read(self) -> list:
        """
        Read the serial port update by controller that include sensor data
        Returns
            messages(list): the sensor data that update by controller.
        """
        self.open_check()
        data = self.ser.readline()
        decoded_values = str(data[0:len(data)].decode('utf-8')).replace('\r\n', '')
        values = decoded_values.split(',')
        messages = []
        for item in values:
                messages.append(item)

        self.ser.flushInput()       
        return messages
