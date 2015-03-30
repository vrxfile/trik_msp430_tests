__author__ = 'Rostislav Varzar'

import termios, fcntl, sys, os, thread, time
import trik_protocol, trik_stty, trik_power

# Async reading registers
aflg = 0x01

# Soft PWM registers
pwmper = 200
pwmdut = 0

# Print text in certain coordinates
def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y + 1, x + 1, text))
     sys.stdout.flush()

# Init async key press input without press <ENTER>
def init_key_press():
    global fd
    global oldterm
    global oldflags
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

# Print text of menu
def print_menu():
    print_there(0, 1, "Software PWMs MENU")
    print_there(0, 2, "Select menu item:")
    print_there(0, 3, "<1/2> Set PWM duty")
    print_there(0, 4, "<C>   Redraw screen")
    print_there(0, 5, "<ESC> Exit/Quit")

# Print register values
def print_registers():
    global pwmper
    global pwmdut
    print_there(25, 3, "%05u / %05u " % (pwmdut,  pwmper))

# Init software PWM #5
def init_spwm_5():
    trik_protocol.write_reg(0x33, 0x02, pwmper)
    trik_protocol.write_reg(0x33, 0x01, pwmdut)
    trik_protocol.write_reg(0x33, 0x00, 0x8000)

# Init Serial TTY device
trik_stty.init_stty()

# Init 12 V power in ARM controller
trik_power.enable_power()

# Init async key press
init_key_press()

thread.start_new_thread(trik_protocol.thread1_read_device, ())
time.sleep(5)

# Clear screen
os.system("clear")

# Print menu
print_menu()
print_registers()

# Init PWM
init_spwm_5()

# Main cycle
try:
    while 1:
        try:
            c = sys.stdin.read(1)
            if c == "1":
                pwmdut = pwmdut - 1
                if pwmdut <= 0:
                    pwmdut = 0
                trik_protocol.write_reg(0x33, 0x01, pwmdut)
            if c == "2":
                pwmdut = pwmdut + 1
                if pwmdut >= pwmper:
                    pwmdut = pwmper
                trik_protocol.write_reg(0x33, 0x01, pwmdut)
            if c.upper() == "C":
                os.system("clear")
                print_menu()
                print_registers()
            if c == chr(0x1B):
                trik_protocol.fflg = 0x00
                time.sleep(5)
                break
            print_registers()
        except IOError: pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)





