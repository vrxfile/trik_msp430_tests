__author__ = 'Rostislav Varzar'

import trik_protocol

# I2C addresses
i2c1 = 0x28
i2c2 = 0x29
i2c3 = 0x2A
i2c4 = 0x2B
i2c5 = 0x2C
i2c6 = 0x2D
i2c7 = 0x2E

# I2C registers
ictl = 0x00
idev = 0x01
ireg = 0x02
idat = 0x03
ierr = 0x04
iidx = 0x05
ival = 0x06
idel = 0x07
ipar = 0x09

# ICTL bits
i2c_disable = 0x80
i2c_enable = 0x80
i2c_read = 0x20
i2c_write = 0x40
i2c_sens = 0x10
i2c_pull = 0x08

# Sensor type
nxttemp = 0x0000
hmc5883l_x = 0x0001
hmc5883l_y = 0x0002
hmc5883l_z = 0x0003
mcp3424_ch1 = 0x0004
mcp3424_ch2 = 0x0005
mcp3424_ch3 = 0x0006
mcp3424_ch4 = 0x0007

# MCP3424 PGA gain
mcp3424_gain1 = 0x0000
mcp3424_gain2 = 0x0001
mcp3424_gain4 = 0x0002
mcp3424_gain8 = 0x0003

# Enable I2C
def enable_i2c(i2cnum):
    trik_protocol.write_reg(i2cnum, ictl, i2c_enable + i2c_pull)

# Disable I2C
def disable_i2c(i2cnum):
    trik_protocol.write_reg(i2cnum, ictl, i2c_disable)

# Read I2C device register
def read_i2c(i2cnum, i2cdev, i2creg):
    trik_protocol.write_reg(i2cnum, idev, i2cdev)
    trik_protocol.write_reg(i2cnum, ireg, i2creg)
    trik_protocol.write_reg(i2cnum, idat, 0x00)
    trik_protocol.write_reg(i2cnum, ictl, i2c_enable + i2c_pull + i2c_read)
    return trik_protocol.read_reg(i2cnum, idat)

# Write I2C device register
def write_i2c(i2cnum, i2cdev, i2creg, i2cdat):
    trik_protocol.write_reg(i2cnum, idev, i2cdev)
    trik_protocol.write_reg(i2cnum, ireg, i2creg)
    trik_protocol.write_reg(i2cnum, idat, i2cdat)
    trik_protocol.write_reg(i2cnum, ictl, i2c_enable + i2c_pull + i2c_write)

# Set I2C sensor type
def set_i2c_sensor_type(i2cnum, i2csenstype):
    trik_protocol.write_reg(i2cnum, iidx, i2csenstype)

# Set I2C sensor ext. parameter
def set_i2c_sensor_parameter(i2cnum, i2csenspar):
    trik_protocol.write_reg(i2cnum, ipar, i2csenspar)

# Read I2C sensor
def read_i2c_sensor(i2cnum):
    trik_protocol.write_reg(i2cnum, ictl, i2c_enable + i2c_pull + i2c_sens)
    return trik_protocol.read_reg(i2cnum, ival)

# Get SCTL register
def get_i2c_control(i2cnum):
    return trik_protocol.read_reg(i2cnum, ictl)

# Get SIDX register (type of sensor)
def get_i2_sensor_type(i2cnum):
    return trik_protocol.read_reg(i2cnum, iidx)
