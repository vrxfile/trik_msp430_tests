__author__ = 'Rostislav Varzar'

import trik_protocol

# PWM addresses
pwm1 = 0x21
pwm2 = 0x22
pwm3 = 0x23
pwm4 = 0x24
pwm5 = 0x25

# PWM registers
pctl = 0x00
pdut = 0x01
pper = 0x02

# PCTL bits
pwm_disable = 0x0000
pwm_enable = 0x8000

# Set PWM period
def set_pwm_period(pwmnum, pwmper):
    trik_protocol.write_reg(pwmnum, pper, pwmper)

# Set PWM duty
def set_pwm_duty(pwmnum, pwmdut):
    trik_protocol.write_reg(pwmnum, pdut, pwmdut)

# Get PWM period
def get_pwm_period(pwmnum):
    return trik_protocol.read_reg(pwmnum, pper)

# Get PWM duty
def get_pwm_duty(pwmnum):
    return trik_protocol.read_reg(pwmnum, pdut)

# Get PCTL register
def get_pwm_control(pwmnum):
    return trik_protocol.read_reg(pwmnum, pctl)

# Start PWM
def start_pwm(pwmnum):
    trik_protocol.write_reg(pwmnum, pctl, pwm_enable)

# Stop PWM
def stop_pwm(pwmnum):
    trik_protocol.write_reg(pwmnum, pctl, pwm_disable)
