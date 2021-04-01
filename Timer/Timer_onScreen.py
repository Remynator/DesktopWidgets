import os
import time
from tkinter import *


class CountDownTimer:

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


def edit_timer(event):
    global run, set_timer_frame, count_down_timer
    global hour_label, minute_label, second_label
    # print(event)

    root.geometry("360x80")
    set_timer_frame.config()
    set_timer_frame.pack()


def set_timer(event):
    global run, set_timer_frame, count_down_timer
    global hour_label, minute_label, second_label
    # print(event)

    h = int(0) if hour_label.get() == "" else int(hour_label.get())
    m = int(0) if minute_label.get() == "" else int(minute_label.get())
    s = int(0) if second_label.get() == "" else int(second_label.get())

    count_down_timer = CountDownTimer(h, m, s)


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
    while run:
        time.sleep(1)
        set_timer_frame.forget()
        root.geometry("250x80")  # font 24

        count_down_timer.total_time -= 1
        d.config(text=f"{count_down_timer.convert()}")

        root.update()


root = Tk()

root.title("Timer")
# root.iconbitmap(os.path.join(os.path.dirname(__file__), "Images", "clock_256.ico"))
root.config(bg="black")
root.wm_attributes("-topmost", 1)  # always on top
# root.wm_attributes("-alpha", 0.5)
# root.wm_attributes("-transparentcolor", "black")  # all black pixels become transparent, in this case the bg

root.bind("<Control-Shift-A>", edit_timer)
root.bind("<Control-Shift-S>", set_timer)
root.bind("<space>", start_stop_clock)

count_down_timer = CountDownTimer(1, 0, 0)
# count_down_timer.label = "Time until Break!"

key_shift = 5
run = False
size_x = 200
size_y = 80
size_font = 24
x = root.winfo_screenwidth() - (root.winfo_width())
y = 105

d = Label(root, text=f"{count_down_timer.print_time}", fg="cyan", bg="black", font=("helvetica", 24))
d.pack()
# l = Label(root, text=f"{count_down_timer.label}", fg="cyan", bg="black", font=("helvetica", 24))
# l.pack()

set_timer_frame = Frame(root)
hour_label = Entry(set_timer_frame)
minute_label = Entry(set_timer_frame)
second_label = Entry(set_timer_frame)
hour_label.grid(row=1, column=0)
minute_label.grid(row=1, column=1)
second_label.grid(row=1, column=2)

root.mainloop()
