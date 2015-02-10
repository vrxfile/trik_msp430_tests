__author__ = 'Rostislav Varzar'

import trik_protocol

# Encoder addresses
sensor1 = 0x04
sensor2 = 0x05
sensor3 = 0x06
sensor4 = 0x07
sensor5 = 0x08
sensor6 = 0x09
sensor7 = 0x0A
sensor8 = 0x0B
sensor9 = 0x0C
sensor10 = 0x0D
sensor11 = 0x0E
sensor12 = 0x0F
sensor13 = 0x10
sensor14 = 0x11
sensor15 = 0x12
sensor16 = 0x13
sensor17 = 0x14
sensor18 = 0x15

# Encoder registers
sctl = 0x00
sidx = 0x01
sval = 0x02

# SCTL bits
sens_enable = 0x8000
sens_async = 0x4000
sens_pull = 0x2000
sens_read = 0x0001

# Sensor type
sens_dig = 0x0000
sens_ana = 0x0001

# Enable sensor
def enable_sensor(sensnum, pullup):
    sensctl = sens_enable + sens_read
    if pullup:
        sensctl = sensctl + sens_pull
    trik_protocol.write_reg(sensnum, sctl, sensctl)

# Enable sensor in async mode
def enable_sensor_in_async(sensnum, pullup):
    sensctl = sens_enable + sens_read + sens_async
    if pullup:
        sensctl = sensctl + sens_pull
    trik_protocol.write_reg(sensnum, sctl, sensctl)

# Set sensor type
def set_sensor_type(sensnum, senstype):
    trik_protocol.write_reg(sensnum, sidx, senstype)

# Read sensor value
def read_sensor(sensnum):
    return trik_protocol.read_reg(sensnum, sval)

# Get SCTL register
def get_sensor_control(sensnum):
    return trik_protocol.read_reg(sensnum, sctl)

# Get SIDX register (type of sensor)
def get_sensor_type(sensnum):
    return trik_protocol.read_reg(sensnum, sidx)
