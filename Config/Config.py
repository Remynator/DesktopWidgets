import os
import time
import geocoder
import json
from datetime import datetime
from tkinter import *
from tkinter import colorchooser
from tkinter.font import Font
from PIL import ImageTk

root = Tk()
clock_date = Label(root)
clock_date.pack()
clock_time = Label(root)
clock_time.pack()
weather_frame = Frame(root)
set_pop = 0

img, weather_info, exclude = "", [], ""

start_time = time.time()
font_type, font_size, font_color = "helvetica", 32, "#000000"
font = Font(family=font_type, size=font_size)

bg_color, bg_trans, alpha = "#000000", False, 1

clock_run, weather_active, settings_active = False, False, False
clock_size_x, clock_size_y, weather_x, weather_y = 0, 0, 0, 0

home_city, lat, lon = "", 0, 0
url, api_key = "", ""


class WeatherObject:

    def __init__(self, dt, temp, feels_like, icon, description, rain, snow):
        self.dt = dt
        self.date = self.convert_date()
        self.time = self.convert_time()
        self.temp_kelvin = temp
        self.temp_celsius = self.temp_kelvin - 273.15
        self.feels_like = feels_like - 273.15
        self.icon = ImageTk.PhotoImage(file="../Images/{}.png".format(icon))
        self.description = description
        self.rain = "rain {:.3f} mm".format(rain) if rain is not None else None
        self.snow = "snow {:.3f} mm".format(snow) if snow is not None else None
        self.frame = self.create_frame()

    def convert_date(self):
        date_time = datetime.fromtimestamp(self.dt)

        return date_time.strftime("%d/%m/%Y")

    def convert_time(self):
        date_time = datetime.fromtimestamp(self.dt)

        return date_time.strftime("%X")

    def create_frame(self):
        frame = Frame(weather_frame, bg=bg_color)

        if "rain" in self.description:
            rain_text = self.rain
        elif "snow" in self.description:
            rain_text = self.snow
        else:
            rain_text = ""

        date_label = Label(frame, text=self.date, fg=font_color, bg=bg_color)
        time_label = Label(frame, text=self.time, fg=font_color, bg=bg_color)
        icon_label = Label(frame, image=self.icon, bg=bg_color)
        desc_label = Label(frame, text=self.description, fg=font_color, bg=bg_color)
        temp_label = Label(frame, text="{:.2f}°C/{:.2f}°C".format(self.temp_celsius, self.feels_like),
                           fg=font_color, bg=bg_color)
        rain_label = Label(frame, text=rain_text, fg=font_color, bg=bg_color)

        date_label.pack()
        time_label.pack()
        icon_label.pack()
        desc_label.pack()
        temp_label.pack()
        rain_label.pack()

        return frame


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


def pick_fc():
    global font_color
    font_color = colorchooser.askcolor()[1]
    update_exp()


def update_exp():
    Label(set_pop, text="example text", bg=bg_color, fg=font_color, font=font).grid(row=3, column=2)


def settings(event):
    global settings_active, set_pop
    global font_type, font_size, font_color

    settings_active = not settings_active

    if set_pop == 0:
        set_pop = Toplevel(bg=bg_color)
        set_pop.title("Settings")
        set_pop.geometry("%dx%d" % (weather_x, weather_y))

        set_pop.bind("<Control-Key-s>", settings)

        # font_type
        # font_size
        Button(set_pop, text="font color", command=pick_fc).grid(row=1, column=2)
        #
        # bg_color_label
        # bg_trans_label
        # alpha_label

    else:
        if settings_active:
            set_pop.deiconify()

        else:
            set_pop.withdraw()
            clock_date.config(fg=font_color)
            clock_time.config(fg=font_color)


def init():
    global img, weather_info, exclude
    global start_time
    global font_type, font_size, font_color, font
    global bg_color, bg_trans, alpha
    global clock_run, weather_active
    global clock_size_x, clock_size_y, weather_x, weather_y
    global home_city, lat, lon
    global url, api_key

    with open("../Config/config.json") as config_file:
        config = json.load(config_file)

    api_key = config["api_key"]["key"]

    try:
        home_city, lat, lon = geocoder.ip("me").city, geocoder.ip("me").lat, geocoder.ip("me").lng
    except json.decoder.JSONDecodeError as loc_err:
        home_city, lat, lon = "London", 0, 0

    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}"

    img = ""
    weather_info = []

    start_time = time.time()
    font_type, font_size, font_color = "helvetica", 32, "#00ffff"
    font = Font(family=font_type, size=font_size)

    bg_color = "#000000"
    bg_trans = False
    alpha = 1

    clock_run = False
    clock_size_x = 8 * font_size + 32  # 740
    clock_size_y = 3 * font_size + 16  # 360

    exclude = "minutely,daily,alerts"  # current,minutely,hourly,daily,alerts
    weather_active = False
    weather_x = 740  # clock_size_x + 256
    weather_y = 360  # clock_size_y + 192
