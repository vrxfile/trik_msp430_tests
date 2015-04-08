__author__ = 'Rostislav Varzar'

import termios, fcntl, sys, os, thread, time
import trik_protocol, trik_stty, trik_power, trik_softi2c

# Async reading registers
aflg = 0x01

# Print text in certain coordinates
def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y + 1, x + 1, text))
     sys.stdout.flush()

# Init Serial TTY device
trik_stty.init_stty()

# Init 12 V power in ARM controller
trik_power.enable_power()

thread.start_new_thread(trik_protocol.thread1_read_device, ())
time.sleep(5)

# Clear screen
os.system("clear")

# Test ADC on port 1
trik_softi2c.i2c_pull = 0

trik_softi2c.enable_i2c(trik_softi2c.i2c4)
i2cctl, daddr, rcode, ecode = trik_protocol.get_reg_value(trik_softi2c.get_i2c_control(trik_softi2c.i2c4))
print_there(1, 1, "I2C ctl register: 0x%04X " % (i2cctl))

i = 0
trik_softi2c.set_i2c_sensor_parameter(trik_softi2c.i2c4, trik_softi2c.mcp3424_gain8)
trik_softi2c.set_i2c_sensor_parameter(trik_softi2c.i2c4, trik_softi2c.mcp3424_gain8)
trik_softi2c.set_i2c_sensor_parameter(trik_softi2c.i2c4, trik_softi2c.mcp3424_gain8)
while i < 1000:
    trik_softi2c.set_i2c_sensor_type(trik_softi2c.i2c4, trik_softi2c.mcp3424_ch1)
    ch1, daddr, rcode, ecode = trik_protocol.get_reg_value(trik_softi2c.read_i2c_sensor(trik_softi2c.i2c4))
    print_there(1, 2, "CH1=%010u, CH2=%010u, i=%010u " % (ch1, 0, i))
    i = i + 1

trik_protocol.fflg = 0x00
time.sleep(5)

