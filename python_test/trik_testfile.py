__author__ = 'Rostislav Varzar'

import time, os, thread
import trik_protocol, trik_stty, trik_power


# Init Serial TTY device
trik_stty.init_stty()

# Init 12 V power in ARM controller
trik_power.enable_power()

# Clear screen
os.system("clear")

thread.start_new_thread(trik_protocol.thread1_read_device, ())
time.sleep(5)

while True:
    print trik_protocol.write_reg(0x00, 0x00, 0x00)
    time.sleep(0.01)








