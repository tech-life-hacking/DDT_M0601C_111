import serial
import crc
import numpy as np

class CommunicationProtocol():
    def __init__(self, port_name):
        self.s = serial.Serial(port_name, 115200)
        self.s.parity = serial.PARITY_NONE
        self.s.bytesize = serial.EIGHTBITS
        self.s.stopbits = serial.STOPBITS_ONE
        self.s.timeout = 5

        self._Tx = np.zeros(10)

        self.crc8 = crc.CRC8()

    def Control_Motor(self, Speed, ID, Acce, Brake_P):
        ID = np.array(ID).astype(np.uint8)
        Speed_high = np.array(np.array(Speed).astype(np.uint16) >> 8).astype(np.uint8)
        Speed_low = np.array((np.array(Speed).astype(np.uint16) & 0x00ff)).astype(np.uint8)
        Acce = np.array(Acce).astype(np.uint8)
        Brake_P = np.array(Brake_P).astype(np.uint8)
        self._Tx = np.array([ID, np.array(0x64).astype(np.uint8), Speed_high, Speed_low, 0, 0, Acce, Brake_P, 0])
        self._Tx = np.append(self._Tx, self.crc8.calculate(self._Tx, 9)).astype(np.uint8)

        self.Send_Motor()
        Rx = self.Receive_Motor()

        BMode = Rx[1]
        ECurru = (Rx[2].astype(np.int8) << 8) + Rx[3]
        BSpeed = (Rx[4].astype(np.int8) << 8) + Rx[5]
        Position = (Rx[6].astype(np.int8) << 8) + Rx[7]
        ErrCode = Rx[8]
        return BMode, ECurru, BSpeed, Position, ErrCode

    def Get_Motor(self, ID):
        ID = np.array(ID).astype(np.uint8)
        self._Tx = np.array([ID, np.array(0x74).astype(np.uint8), 0, 0, 0, 0, 0, 0, 0])
        self._Tx = np.append(self._Tx, self.crc8.calculate(self._Tx, 9)).astype(np.uint8)

        self.Send_Motor()
        Rx = self.Receive_Motor()

        BMode = Rx[1]
        ECurru = (Rx[2].astype(np.int8) << 8) + Rx[3]
        BSpeed = (Rx[4].astype(np.int8) << 8) + Rx[5]
        Temp = Rx[6]
        Position = Rx[7]
        ErrCode = Rx[8]
        return BMode, ECurru, BSpeed, Temp, Position, ErrCode

    def Set_MotorMode(self, Mode, ID):
        self._Tx = np.array([ID, 0xA0, 0, 0, 0, 0, 0, 0, 0, Mode], dtype=np.uint8)
        self.Send_Motor()

    def Set_MotorID(self, ID):
        self._Tx = np.array([0xAA, 0x55, 0x53, ID, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
        self.Send_Motor()

    def Check_Motor(self):
        self._Tx = np.array([0xc8, 0x64, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
        self._Tx = np.append(self._Tx, self.crc8.calculate(self._Tx, 9)).astype(np.uint8)

        self.Send_Motor()
        Rx = self.Receive_Motor()

        BMode = Rx[1]
        ECurru = (Rx[2].astype(np.int8) << 8) + Rx[3]
        BSpeed = (Rx[4].astype(np.int8) << 8) + Rx[5]
        Position = (Rx[6].astype(np.int8) << 8) + Rx[7]
        ErrCode = Rx[8]
        return BMode, ECurru, BSpeed, Position, ErrCode

    def Send_Motor(self):
        self.s.write(self._Tx.tobytes())
        self.s.flush()

    def Receive_Motor(self):
        Rx = self.s.read(10)
        Rx = np.frombuffer(Rx, dtype=np.uint8)
        if Rx.size == 0:
            raise Exception("No Communication!")

        return Rx