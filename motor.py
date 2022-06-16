import usart

class Motor():
    def __init__(self, port_name):
        self.cp = usart.CommunicationProtocol(port_name)

    def stop(self):
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
            mode, Current, Velocity, Angle, Fault_value = cp.Control_Motor(speed, ID, Acce, Brake_P)
            time.sleep(0.01)