__author__ = 'Rostislav Varzar'

import thread

# Output devices
# fname1 = "000.txt"
fname1 = "/dev/ttyACM0"
fname2 = "/dev/ttyACM1"

# Flag to work thread
fflg = 0x01

# Received packet
fstmp = ""

# Timeout of receiving packet
timeout = 1000

# Thread to read device answer
def thread1_read_device():
    global fname1
    global fflg
    global fstmp
    ff1 = open(fname1, "r")
    while fflg:
        if fflg == 0x01:
            fstmp = ff1.readline()
    ff1.close()
    thread.exit_thread()

# Function to recognize response packets
def get_reg_value(stmp):
    regval = 0x00000000
    devaddr = 0x00
    respcode = 0x00
    errcode = 0x00
    if len(stmp) == 18:
        devaddr = int(("0x" + stmp[1] + stmp[2]), 16)
        respcode = int(("0x" + stmp[3] + stmp[4]), 16)
        regaddr = int(("0x" + stmp[5] + stmp[6]), 16)
        regval = int(("0x" + stmp[7] + stmp[8] + stmp[9] + stmp[10] + stmp[11] + stmp[12] + stmp[13] + stmp[14]), 16)
        crc1 = int(("0x" + stmp[15] + stmp[16]), 16)
        crc2 = (0xFF - (devaddr + respcode + regaddr + (regval & 0xFF) + ((regval >> 8) & 0xFF) + ((regval >> 16) & 0xFF) + ((regval >> 24) & 0xFF)) + 1) & 0xFF
        if crc1 != crc2:
            errcode = 100
        else:
            errcode = 0
    else:
        errcode = 200
    return regval, devaddr, respcode, errcode

# Write single register
"""
def write_reg(devaddr, regaddr, regval):
    try:
        f2 = open(fname1, "rb")
        funcnum = 0x03
        crc = (0xFF - (devaddr + funcnum + regaddr + (regval & 0xFF) + ((regval >> 8) & 0xFF) + ((regval >> 16) & 0xFF) + ((regval >> 24) & 0xFF)) + 1) & 0xFF
        stmp = ":%02X%02X%02X%08X%02X\n" % (devaddr, funcnum, regaddr, regval, crc)
        f1 = open(fname1, "wb")
        f1.write(stmp)
        f1.close()
        stmp = ""
        sidx = 0
        ss = ""
        while ss != "\n" or sidx < 18:
            ss = str(f2.read(1))
            stmp = stmp + ss
            sidx = sidx + 1
        f2.close()
        return stmp
    except IOError, e:
        return stmp
"""
def write_reg(devaddr, regaddr, regval):
    global fstmp
    global timeout
    try:
        fstmp = ""
        funcnum = 0x03
        crc = (0xFF - (devaddr + funcnum + regaddr + (regval & 0xFF) + ((regval >> 8) & 0xFF) + ((regval >> 16) & 0xFF) + ((regval >> 24) & 0xFF)) + 1) & 0xFF
        stmp = ":%02X%02X%02X%08X%02X\n" % (devaddr, funcnum, regaddr, regval, crc)
        f1 = open(fname1, "wb")
        f1.write(stmp)
        f1.close()
        i = 0
        while fstmp == "" or i < timeout:
            i = i + 1
        return fstmp
    except IOError, e:
        return fstmp

# Read single register
"""
def read_reg(devaddr, regaddr):
    try:
        f2 = open(fname1, "rb")
        funcnum = 0x05
        crc = (0xFF - (devaddr + funcnum + regaddr) + 1) & 0xFF
        stmp = ":%02X%02X%02X%02X\n" % (devaddr, funcnum, regaddr, crc)
        f1 = open(fname1, "wb")
        f1.write(stmp)
        f1.close()
        stmp = ""
        sidx = 0
        ss = ""
        while ss != "\n" or sidx < 18:
            ss = str(f2.read(1))
            stmp = stmp + ss
            sidx = sidx + 1
        f2.close()
        return stmp
    except IOError, e:
        return stmp
"""
def read_reg(devaddr, regaddr):
    global fstmp
    global timeout
    try:
        fstmp = ""
        funcnum = 0x05
        crc = (0xFF - (devaddr + funcnum + regaddr) + 1) & 0xFF
        stmp = ":%02X%02X%02X%02X\n" % (devaddr, funcnum, regaddr, crc)
        f1 = open(fname1, "wb")
        f1.write(stmp)
        f1.close()
        i = 0
        while fstmp == "" or i < timeout:
            i = i + 1
        return fstmp
    except IOError, e:
        return fstmp




