import os
from datetime import datetime
from tkinter import *
from tkinter.font import Font

# pyinstaller --onefile -w --icon="Images\Clock_256.ico" Clock_onScreen.py  # create executable
# https://weather.com/weather/today/l/51.52,5.40?par=google&temp=c


def top_right_screen(event):
    # print(event)
    x = root.winfo_screenwidth() - (root.winfo_width())
    y = 0
    root.geometry('%dx%d+%d+%d' % (root.winfo_width(), root.winfo_height(), x, y))


def top_right_browser(event):
    # print(event.keysym)
    x = root.winfo_screenwidth() - (root.winfo_width()) - 32
    y = 168
    root.geometry('%dx%d+%d+%d' % (root.winfo_width(), root.winfo_height(), x, y))


def bottom_right_browser(event):
    # print(event)
    x = root.winfo_screenwidth() - (root.winfo_width()) - 32
    y = root.winfo_screenheight() - (root.winfo_height()) - 104
    root.geometry('%dx%d+%d+%d' % (root.winfo_width(), root.winfo_height(), x, y))


def reposition(event):
    # print(event)
    x = root.winfo_x()
    y = root.winfo_y()

    if event.keysym.lower() == "w":
        if event.keysym == "W":
            y -= 32
        else:
            y -= 4

    if event.keysym.lower() == "s":
        if event.keysym == "S":
            y += 32
        else:
            y += 4

    if event.keysym.lower() == "a":
        if event.keysym == "A":
            x -= 32
        else:
            x -= 4

    if event.keysym.lower() == "d":
        if event.keysym == "D":
            x += 32
        else:
            x += 4

    root.geometry('%dx%d+%d+%d' % (root.winfo_width(), root.winfo_height(), x, y))


def run_clock(event):
    global clock_run
    # print(event)
    # print(root.winfo_rootx(), root.winfo_y())

    clock_run = not clock_run
    if clock_run:
        root.overrideredirect(1)
    else:
        root.overrideredirect(0)

    while clock_run:
        update_clock()


def open_clock():

    root.title("Time")
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "../Images", "clock_256.ico"))
    root.config(bg=bg_color)
    root.wm_attributes("-topmost", 1)  # always on top
    root.wm_attributes("-alpha", alpha)
    if bg_trans:
        root.wm_attributes("-transparentcolor", bg_color)
    root.lift()

    root.bind("<Control-Button-1>", top_right_screen)
    root.bind("<Shift-Button-1>", top_right_browser)
    root.bind("<Alt-Button-1>", bottom_right_browser)
    root.bind("<Key-w>", reposition)
    root.bind("<Key-s>", reposition)
    root.bind("<Key-a>", reposition)
    root.bind("<Key-d>", reposition)
    root.bind("<Key-W>", reposition)
    root.bind("<Key-S>", reposition)
    root.bind("<Key-A>", reposition)
    root.bind("<Key-D>", reposition)
    root.bind("<space>", run_clock)

    update_clock()


def update_clock():
    root.geometry("%dx%d" % (clock_size_x, clock_size_y))

    clock_date.config(text=f"{datetime.now():%a, %b-%d}", fg=font_color, bg="black", font=font)
    clock_time.config(text=f"{datetime.now():%H:%M:%S  #%V}", fg=font_color, bg="black", font=font)

    root.update()


root = Tk()

clock_date = Label(root)
clock_date.pack()
clock_time = Label(root)
clock_time.pack()

font_size = 32
font_color = "#00ffff"
font = Font(family="helvetica", size=font_size)

bg_color = "#000000"
bg_trans = False
alpha = 1

clock_run = False
clock_size_x = 8 * font_size + 32  # 740
clock_size_y = 3 * font_size + 16  # 360

open_clock()
root.mainloop()
