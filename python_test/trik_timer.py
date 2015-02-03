__author__ = 'Rostislav Varzar'

import trik_protocol

# Timer address
timer1 = 0x26

# Timer registers
atctl = 0x00
atper = 0x01
atval = 0x02

# ATCTL bits
at_en = 0x0003

# Enable timer
def timer_enable():
    trik_protocol.write_reg(timer1, atctl, at_en)

# Disable timer
def timer_disable():
    trik_protocol.write_reg(timer1, atctl, 0x0000)

# Set timer period
def set_timer_period(tmper):
    trik_protocol.write_reg(timer1, atper, tmper)

# Get TCTL register
def get_timer_control():
    return trik_protocol.read_reg(timer1, atctl)

# Get TVAL register
def get_timer_value():
    return trik_protocol.read_reg(timer1, atval)

