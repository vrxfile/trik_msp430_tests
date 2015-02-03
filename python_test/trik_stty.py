__author__ = 'Rostislav Varzar'

import os
import trik_protocol

# Init Serial TTY device
def init_stty():
    sty1 = "stty 921600 -F %s -echo -onlcr" % (trik_protocol.fname1)
    os.system(sty1)
    sty1 = "stty 921600 -F %s -echo -onlcr" % (trik_protocol.fname2)
    os.system(sty1)

