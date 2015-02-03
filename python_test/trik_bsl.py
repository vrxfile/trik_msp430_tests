__author__ = 'Rostislav Varzar'

import os
import trik_protocol

# BSL address
bsl1 = 0xEE

# BSL registers
bsl_pswd = 0x00

# BSL password
bsl_password = 0xA480E917

# Enable calibartion
def enter_bsl(passwrd):
    if passwrd == bsl_password:
        trik_protocol.write_reg(bsl1, bsl_pswd, passwrd)

