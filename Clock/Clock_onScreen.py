import os
import time
from datetime import datetime
import Config.Config as cfg

# pyinstaller --onefile -w --icon="Images\Clock_256.ico" Clock_onScreen.py  # create executable
# https://weather.com/weather/today/l/51.52,5.40?par=google&temp=c


def run_clock(event):
    # print(event)
    # print(root.winfo_rootx(), root.winfo_y())

    cfg.clock_run = not cfg.clock_run
    if cfg.clock_run:
        cfg.root.overrideredirect(1)
        cfg.start_time = cfg.time.time()
    else:
        cfg.root.overrideredirect(0)

    while cfg.clock_run:
        time.sleep(10 / 1000)
        update_clock()

        cfg.root.geometry('%dx%d' % (cfg.clock_size_x, cfg.clock_size_y))


def open_clock():
    cfg.root.title("Time")
    cfg.root.iconbitmap(os.path.join(os.path.dirname(__file__), "../Images", "clock_256.ico"))
    cfg.root.config(bg=cfg.bg_color)
    cfg.root.wm_attributes("-topmost", 1)  # always on top
    cfg.root.wm_attributes("-alpha", cfg.alpha)
    if cfg.bg_trans:
        cfg.root.wm_attributes("-transparentcolor", cfg.bg_color)
    cfg.root.lift()

    cfg.root.bind("<Control-Button-1>", cfg.top_right_screen)
    cfg.root.bind("<Shift-Button-1>", cfg.top_right_browser)
    cfg.root.bind("<Alt-Button-1>", cfg.bottom_right_browser)
    cfg.root.bind("<Key-w>", cfg.reposition)
    cfg.root.bind("<Key-s>", cfg.reposition)
    cfg.root.bind("<Key-a>", cfg.reposition)
    cfg.root.bind("<Key-d>", cfg.reposition)
    cfg.root.bind("<Key-W>", cfg.reposition)
    cfg.root.bind("<Key-S>", cfg.reposition)
    cfg.root.bind("<Key-A>", cfg.reposition)
    cfg.root.bind("<Key-D>", cfg.reposition)
    cfg.root.bind("<space>", run_clock)

    update_clock()


def update_clock():
    x = cfg.clock_size_x
    y = cfg.clock_size_y

    cfg.root.geometry("%dx%d" % (x, y))

    cfg.clock_date.config(text=f"{datetime.now():%a, %b-%d}", fg=cfg.font_color, bg=cfg.bg_color, font=cfg.font)
    cfg.clock_time.config(text=f"{datetime.now():%H:%M:%S  #%V}", fg=cfg.font_color, bg=cfg.bg_color, font=cfg.font)

    cfg.root.update()


cfg.init()
open_clock()
cfg.root.mainloop()
