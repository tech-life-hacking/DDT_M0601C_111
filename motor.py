import usart
import time

class Motor():
    def __init__(self, port_name, ID):
        self.cp = usart.CommunicationProtocol(port_name)
        self.id = ID

    def stop(self):
        try:
            _, _, Speed, _, Fault_value = self.cp.Check_Motor()
            if Speed > 0:
                speedlist = list(range(Speed))
                speedlist.reverse()
            else:
                Speed *= -1
                speedlist = list(range(0, Speed, 2))
                speedlist.reverse()
                speedlist = [n*(-1) for n in speedlist]

            for speed in speedlist:
                mode, Current, Velocity, Angle, Fault_value = self.cp.Control_Motor(speed, self.id, 0, 0)
                time.sleep(0.01)
        except:
            pass

    def rotate(self, speed, rotatetime):
        self.cp.Control_Motor(speed, self.id, 0, 0)
        time.sleep(rotatetime)
