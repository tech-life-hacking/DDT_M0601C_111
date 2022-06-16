# DDT_M0601C_111
Sample Code of  Direct Drive Motor made by Direct Drive Tech.

The detail is [my articles](https://www.techlife-hacking.com/?p=1422).
## Hardware
Wire each hardwares like below.
![HardwareSetup](https://www.techlife-hacking.com/wp-content/uploads/2022/06/DDT-1.png)
* [Direct Drive Motor](https://www.switch-science.com/catalog/7646/)
* RaspberryPi
* USB to RS485 Converter
* AC Adapter
* DC-DC Converter

## Setup
install python libraries
```
# install dependency
pip3 install pyserial
pip3 install numpy
```
After inserting a USB-RS485 converter to PC or RaspberryPi, confirm a port name.
```
# confirm port name
ls -lrt /dev/serial/by-id/

output: PORTNAME
```
permit serial port
```
# permit serial port
sudo chmod 666 /dev/serial/by-id/PORTNAME
```

## Usage
After cloning this repository, excute demo.

```
git clone https://github.com/tech-life-hacking/DDT_M0601C_111.git
cd DDT_M0601C_111
python3 demo.py
```
Demo code
```
import usart
import time

# set port name to open the port
port_name = "/dev/serial/by-id/PORTNAME"
cp = usart.CommunicationProtocol(port_name)

Speed, Mode, ID, Acce, Brake_P = 150, 2, 1, 0, 0
# set ID
cp.Set_MotorID(ID)
# set motor mode 2: velocity loop
cp.Set_MotorMode(Mode, ID)
# control motor
mode, Current, Velocity, Angle, Fault_value = cp.Control_Motor(Speed, ID, Acce, Brake_P)
print('mode: '+ str(mode) + ' ' + 'Velocity ' + str(Velocity) + '(RPM/0.1ms) ' + 'Angle ' + str(Angle / 32767 * 360) + '(degree) ' + 'Fault_value ' + str(Fault_value))
time.sleep(1)
# check motor velocity
mode, Current, Velocity, Angle, Fault_value = cp.Check_Motor()
print('mode: '+ str(mode) + ' ' + 'Velocity ' + str(Velocity) + '(RPM/0.1ms) ' + 'Angle ' + str(Angle / 32767 * 360) + '(degree) ' + 'Fault_value ' + str(Fault_value))
```

## Reference
[User Manual](https://d2air1d4eqhwg2.cloudfront.net/media/files/a48110eb-432c-4083-a159-9e0f35913b23.pdf)