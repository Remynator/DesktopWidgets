import os
import time
from tkinter import *


class PomodoroTimer:

    # timer
    def __init__(self, hours, minutes, seconds):
        self.h = hours
        self.m = minutes
        self.s = seconds
        self.total_time = self.h * 3600 + self.m * 60 + self.s
        self.print_time = self.convert()

    def __int__(self):
        self.label = None

    def convert(self):
        # seconds = self.total_time % (24 * 3600)  # without days
        seconds = self.total_time
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)


def start_stop_clock(event):
    global run
    # print(event)

    run = not run
    if run:
        root.overrideredirect(1)
    else:
        root.overrideredirect(0)
    run_timer()


def run_timer():
    global pomodoro

    while run:
        root.geometry("%dx%d" % (size_x, size_y))

        while pomodoro.total_time >= 0:
            # print(pomodoro.convert() + "\n" + pomodoro.label)

            timer_time.config(text=f"{pomodoro.convert()}")
            timer_label.config(text=f"{pomodoro.label}")

            pomodoro.total_time -= 1
            time.sleep(1)
            root.update()

        # alternate between timers, add elif statement to add timer
        if pomodoro.label == label1:
            pomodoro = PomodoroTimer(time2[0], time2[1], time2[2])
            pomodoro.label = label2
        # elif pomodoro.label == label2:
        #     pomodoro = PomodoroTimer(time3[0], time3[1], time3[2])
        #     pomodoro.label = label3
        else:
            pomodoro = PomodoroTimer(time1[0], time1[1], time1[2])
            pomodoro.label = label1


root = Tk()

root.title("Timer")
# root.iconbitmap(os.path.join(os.path.dirname(__file__), "Images", "clock_256.ico"))
root.config(bg="black")
root.wm_attributes("-topmost", 1) # always on top
# root.wm_attributes("-alpha", 0.5)
# root.wm_attributes("-transparentcolor", "black") # all black pixels become transparent, in this case the bg

root.bind("<space>", start_stop_clock)

time1, label1 = [0, 25, 0], "Time until Break"    # [hours, minutes, seconds], "label"
time2, label2 = [0,  5, 0], "Break!!!"
# time3, label3 = [0,  0, 0], ""

run = False

size_x = 250
size_y = 80
size_font = 24

pomodoro = PomodoroTimer(time1[0], time1[1], time1[2])
pomodoro.label = label1

timer_time = Label(root, text=f"{pomodoro.print_time}", fg="cyan", bg="black", font=("helvetica", size_font))
timer_time.pack()
timer_label = Label(root, text=f"{pomodoro.label}", fg="cyan", bg="black", font=("helvetica", size_font))
timer_label.pack()

root.mainloop()
