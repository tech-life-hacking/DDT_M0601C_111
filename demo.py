import usart
import time

port_name = "/dev/serial/by-id/PORTNAME"
cp = usart.CommunicationProtocol(port_name)

Speed, Mode, ID, Acce, Brake_P = 150, 2, 1, 0, 0
cp.Set_MotorID(ID)
cp.Set_MotorMode(Mode, ID)
mode, Current, Velocity, Angle, Fault_value = cp.Control_Motor(Speed, ID, Acce, Brake_P)
print('mode: '+ str(mode) + ' ' + 'Velocity ' + str(Velocity) + '(RPM/0.1ms) ' + 'Angle ' + str(Angle / 32767 * 360) + '(degree) ' + 'Fault_value ' + str(Fault_value))
time.sleep(1)
mode, Current, Velocity, Angle, Fault_value = cp.Check_Motor()
print('mode: '+ str(mode) + ' ' + 'Velocity ' + str(Velocity) + '(RPM/0.1ms) ' + 'Angle ' + str(Angle / 32767 * 360) + '(degree) ' + 'Fault_value ' + str(Fault_value))
time.sleep(1)
Speed, Mode, ID, Acce, Brake_P = 0, 2, 1, 0, 0
mode, Current, Velocity, Angle, Fault_value = cp.Control_Motor(Speed, ID, Acce, Brake_P)
print('mode: '+ str(mode) + ' ' + 'Velocity ' + str(Velocity) + '(RPM/0.1ms) ' + 'Angle ' + str(Angle / 32767 * 360) + '(degree) ' + 'Fault_value ' + str(Fault_value))
time.sleep(1)
mode, Current, Velocity, Angle, Fault_value = cp.Check_Motor()
print('mode: '+ str(mode) + ' ' + 'Velocity ' + str(Velocity) + '(RPM/0.1ms) ' + 'Angle ' + str(Angle / 32767 * 360) + '(degree) ' + 'Fault_value ' + str(Fault_value))
