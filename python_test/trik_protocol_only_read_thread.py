__author__ = 'Rostislav Varzar'

import thread

# Output devices
fname1 = "/dev/ttyACM0"

# Flag to work thread
fflg = 0x01

# Received packet
fstmp = ""

# Thread to read device answer
def thread1_read_device():
    global fname1
    global fflg
    global fstmp
    ff1 = open(fname1, "r")
    while fflg:
      fstmp = ff1.readline()
    ff1.close()
    thread.exit_thread()

thread.start_new_thread(thread1_read_device, ())

