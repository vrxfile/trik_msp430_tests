__author__ = 'Rostislav Varzar'

import termios, fcntl, sys, os, thread, time
import trik_protocol, trik_motor, trik_encoder, trik_timer, trik_sensor, trik_touch, trik_bsl
import trik_stty, trik_power
import random
import datetime

freport1 = "trik_report_big.txt"
freport2 = "trik_report_small.txt"

# Device addresses
motor1 = 0x00
motor2 = 0x01
motor3 = 0x02
motor4 = 0x03
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
encoder1 = 0x16
encoder2 = 0x17
encoder3 = 0x18
encoder4 = 0x19
port1 = 0x1A
port2 = 0x1B
port3 = 0x1C
port4 = 0x1D
port5 = 0x1E
port6 = 0x1F
portJ = 0x20
pwm1 = 0x21
pwm2 = 0x22
pwm3 = 0x23
pwm4 = 0x24
pwm5 = 0x25
a_timer = 0x26
touch = 0x27
bsl = 0xEE
maxdevices = touch

# Test register values
testregvals = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D,
               0x0E, 0x0F, 0x10, 0x20, 0x40, 0x80,
               0xFE, 0xFF, 0x100, 0x200, 0x400, 0x800,
               0xFFE, 0xFFF, 0x1000, 0x2000, 0x4000, 0x8000,
               0xFFFE, 0xFFFF, 0x10000, 0x20000, 0x40000, 0x80000,
               0xFFFFE, 0xFFFFF, 0x100000, 0x200000, 0x400000, 0x800000,
               0xFFFFFE, 0xFFFFFF, 0x1000000, 0x2000000, 0x4000000, 0x8000000,
               0xFFFFFFE, 0xFFFFFFF, 0x10000000, 0x20000000, 0x40000000, 0x80000000,
               0xFFFFFFFE, 0xFFFFFFFF]

# Errors descriptions
testerrors = ["No error",
              "Illegal Function Code",
              "Illegal Register Address",
              "Illegal Register Value",
              "Slave Device Failure",
              "Undefined",
              "Slave Device Busy",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Undefined",
              "Illegal Device Address",
              "CRC Error",
              "Start condition error",
              "Incorrect packet length",
              "Inconsistency of Multiple Registers"]

# Init Serial TTY device
trik_stty.init_stty()

# Init 12 V power in ARM controller
trik_power.enable_power()

# Start thread to read response data from device
thread.start_new_thread(trik_protocol.thread1_read_device, ())
time.sleep(5)

# Clear screen
os.system("clear")

# Make report files
f1 = open(freport1, "w")
f2 = open(freport2, "w")
f1.write("")
f2.write("")
f1.close()
f2.close()

# Test all device addresses and all register addresses and some registers values (writing mode)
def stress_test_writing():
    global testregvals
    devaddr = 0x00
    while devaddr <= 0xFF:
        f1 = open(freport1, "a")
        f2 = open(freport2, "a")
        stmp1 = "\n----------" + datetime.datetime.now().isoformat() + "----------\n"
        f2.write(stmp1)
        regaddr = 0x00
        while regaddr <= 0xFF:
            stmp1 = "\n----------" + datetime.datetime.now().isoformat() + "----------\n"
            f1.write(stmp1)
            stmp1 = "----------Device address: 0x%02X---------------- \n" % (devaddr)
            f1.write(stmp1)
            stmp1 = "----------Register address: 0x%02X-------------- \n" % (regaddr)
            f1.write(stmp1)
            stmp1 = "DEV=0x%02X REG=0x%02X" % (devaddr, regaddr)
            print stmp1
            ridx = 0x00
            while ridx < len(testregvals):
                regval = testregvals[ridx]
                stmp1 = "\n Writing... \n"
                f1.write(stmp1)
                stmp1 = "Register value: 0x%08X \n" % (regval)
                f1.write(stmp1)
                stmp2 = stmp1 = trik_protocol.write_reg(devaddr, regaddr, regval)
                rval, daddr, rcode, ecode = trik_protocol.get_reg_value(stmp1)
                # Report only if anomaly is present
                errflg = 1
                if devaddr >= motor1 and devaddr <= motor4 and regaddr <= 0x06 and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr >= sensor1 and devaddr <= sensor18 and regaddr <= 0x02 and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr >= encoder1 and devaddr <= encoder4 and regaddr <= 0x01 and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr >= port1 and devaddr <= portJ and regaddr <= 0x08 and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr == a_timer and regaddr <= 0x02 and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr == touch and regaddr <= 0x08 and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr == bsl and rcode == 0x03 and rval == 0x00:
                    errflg = 0
                if devaddr >= motor1 and devaddr <= motor4 and regaddr > 0x06 and rcode == 0x83 and rval == 0x02:
                    errflg = 0
                if devaddr >= sensor1 and devaddr <= sensor18 and regaddr > 0x02 and rcode == 0x83 and rval == 0x02:
                    errflg = 0
                if devaddr >= encoder1 and devaddr <= encoder4 and regaddr > 0x01 and rcode == 0x83 and rval == 0x02:
                    errflg = 0
                if devaddr >= port1 and devaddr <= portJ and regaddr > 0x08 and rcode == 0x83 and rval == 0x02:
                    errflg = 0
                if devaddr == a_timer and regaddr > 0x02 and rcode == 0x83 and rval == 0x02:
                    errflg = 0
                if devaddr == touch and regaddr > 0x08 and rcode == 0x83 and rval == 0x02:
                    errflg = 0
                if devaddr == bsl and rcode == 0x83:
                    errflg = 0
                if devaddr > maxdevices and rcode == 0x83 and rval == 0x11:
                    errflg = 0
                if ecode != 0:
                    errflg = 1
                if devaddr != daddr:
                    errflg = 1
                if errflg != 0:
                    if rcode < 0x80:
                        stmp1 = "No error \n"
                    else:
                        stmp1 = "Error flag set \n"
                    f1.write(stmp1)
                    if rval <= 0x15:
                        stmp1 = "Error code: 0x%08X, %s \n" % (rval, testerrors[rval])
                    else:
                        stmp1 = "Error code: 0x%08X, %s \n" % (rval, "Undefined")
                    f1.write(stmp1)
                    stmp1 = "Packet error: 0x%02X \n" % (ecode)
                    f1.write(stmp1)
                    f1.write("Received string: " + stmp2 + "\n")
                    stmp1 = "DEV=0x%02X REG=0x%02X SEND=0x%08X RECV=0x%08X PACK=0x%02X STR=%s" % (devaddr, regaddr, regval, rval, ecode, stmp2)
                    f2.write(stmp1 + "\n")
                    print stmp1
                ridx = ridx + 1
            regaddr = regaddr + 1
        f1.close()
        f2.close()
        devaddr = devaddr + 1

stress_test_writing()

