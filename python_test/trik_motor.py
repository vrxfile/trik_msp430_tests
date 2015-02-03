__author__ = 'Rostislav Varzar'

import trik_protocol

# Motor addresses
motor1 = 0x00
motor2 = 0x01
motor3 = 0x02
motor4 = 0x03

# Motor registers
mctl = 0x00
mdut = 0x01
mper = 0x02
mang = 0x03
mtmr = 0x04
mval = 0x05
merr = 0x06

# MCTL bits
mot_enable = 0x8000
mot_auto = 0x4000
mot_angle = 0x2000
mot_back = 0x0010
mot_brake = 0x0008
mot_power = 0x0003

# Set PWM period for motor
def set_motor_period(motnum, pwmper):
    trik_protocol.write_reg(motnum, mper, pwmper)

# Set PWM duty for motor
def set_motor_duty(motnum, pwmdut):
    trik_protocol.write_reg(motnum, mdut, pwmdut)

# Set rotation angle
def set_motor_angle(motnum, motangle):
    trik_protocol.write_reg(motnum, mang, motangle)

# Set rotation time
def set_motor_time(motnum, mottime):
    trik_protocol.write_reg(motnum, mtmr, mottime)

# Get PWM period of motor
def get_motor_period(motnum):
    return trik_protocol.read_reg(motnum, mper)

# Get PWM duty of motor
def get_motor_duty(motnum):
    return trik_protocol.read_reg(motnum, mdut)

# Get MCTL register
def get_motor_control(motnum):
    return trik_protocol.read_reg(motnum, mctl)

# Get ANGLE register
def get_motor_angle(motnum):
    return trik_protocol.read_reg(motnum, mang)

# Get TIME register
def get_motor_time(motnum):
    return trik_protocol.read_reg(motnum, mtmr)

# Get MERR register
def get_motor_overcurrent(motnum):
    return trik_protocol.read_reg(motnum, merr)

# Get Feed-Back register
def get_motor_feedback(motnum):
    return trik_protocol.read_reg(motnum, mval)

# Start motor
def start_motor(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_power)

# Reverse start motor
def reverse_motor(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_back + mot_power)

# Brake motor
def brake_motor(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_brake)

# Stop motor
def stop_motor(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable)

# Rotate motor by angle
def rotate_motor_angle(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_power + mot_auto + mot_angle + mot_brake)

# Reverse motor by angle
def reverse_motor_angle(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_power + mot_auto + mot_angle + mot_back + mot_brake)

# Rotate motor by time
def rotate_motor_time(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_power + mot_auto + mot_brake)

# Reverse motor by time
def reverse_motor_time(motnum):
    trik_protocol.write_reg(motnum, mctl, mot_enable + mot_power + mot_auto + mot_back + mot_brake)

