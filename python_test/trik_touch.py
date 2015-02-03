__author__ = 'Rostislav Varzar'

import os
import trik_protocol

# Touch address
touch1 = 0x27

# Touch registers
tmod = 0x00
minx = 0x01
maxx = 0x02
miny = 0x03
maxy = 0x04
scrx = 0x05
scry = 0x06
curx = 0x07
cury = 0x08

# TMOD bits
t_en = 0x0001

# Enable calibartion
def touch_cal_on():
    trik_protocol.write_reg(touch1, tmod, t_en)

# Disable calibartion
def touch_cal_off():
    trik_protocol.write_reg(touch1, tmod, 0x0000)

# Get TMOD register
def get_touch_control():
    return trik_protocol.read_reg(touch1, tmod)

# Get MINX
def get_touch_minx():
    return trik_protocol.read_reg(touch1, minx)

# Get MAXX
def get_touch_maxx():
    return trik_protocol.read_reg(touch1, maxx)

# Get MINY
def get_touch_miny():
    return trik_protocol.read_reg(touch1, miny)

# Get MAXY
def get_touch_maxy():
    return trik_protocol.read_reg(touch1, maxy)

# Get SCRX
def get_touch_scrx():
    return trik_protocol.read_reg(touch1, scrx)

# Get SCRY
def get_touch_scry():
    return trik_protocol.read_reg(touch1, scry)

# Get POSX
def get_touch_posx():
    return trik_protocol.read_reg(touch1, curx)

# Get POSY
def get_touch_posy():
    return trik_protocol.read_reg(touch1, cury)

# Activate ts drivers
def activate_touch_driver():
    os.system("export QWS_MOUSE_PROTO=tslib:/dev/input/event0")







