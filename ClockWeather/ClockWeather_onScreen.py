import os
import time
import geocoder
import requests
import json
from configparser import ConfigParser
from datetime import datetime
from tkinter import *
from tkinter.font import Font
from PIL import ImageTk


# pyinstaller --onefile -w --icon="Images\Clock_256.ico" ClockWeather_onScreen.py  # create executable
# https://weather.com/weather/today/l/51.52,5.40?par=google&temp=c


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


def run_clock(event):
    global clock_run, weather_active, start_time
    # print(event)
    # print(root.winfo_rootx(), root.winfo_y())

    clock_run = not clock_run
    if clock_run:
        root.overrideredirect(1)
        start_time = time.time()
    else:
        root.overrideredirect(0)

    while clock_run:
        time.sleep(10 / 1000)
        update_clock()

        if weather_active and (time.time() - start_time) > 300:
            start_time = time.time()
            print("Weather update")
            update_weather()
        else:
            root.geometry('%dx%d' % (clock_size_x, clock_size_y))


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
    root.bind("<Control-Key-w>", set_weather)

    update_clock()


def update_clock():
    x = clock_size_x if not weather_active else weather_x
    y = clock_size_y if not weather_active else weather_y

    root.geometry("%dx%d" % (x, y))

    clock_date.config(text=f"{datetime.now():%a, %b-%d}", fg=font_color, bg=bg_color, font=font)
    clock_time.config(text=f"{datetime.now():%H:%M:%S  #%V}", fg=font_color, bg=bg_color, font=font)

    root.update()


def set_weather(event):
    global weather_active
    weather_active = not weather_active

    if weather_active:
        root.title("Weather {}, {}, {}".format(home_city, lat, lon))
        weather_frame.pack(pady=20)
        root.geometry("%dx%d" % (weather_x, weather_y))
        update_weather()
    else:
        weather_frame.forget()
        root.geometry("%dx%d" % (clock_size_x, clock_size_y))


def update_weather():
    global weather_info
    weather_info.clear()

    try:
        # print(url.format(lat, lon, exclude, api_key))
        api = requests.get(url.format(lat, lon, exclude, api_key))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", err)
        api = None
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        api = None

    if api:
        api = api.json()

        with open('api_data.json', 'w') as outfile:
            json.dump(api, outfile, indent=2)

        for i in range(49):
            if i == 0:
                try:
                    rain = api["current"]["rain"]["1h"]
                except KeyError:
                    rain = None
                try:
                    snow = api["current"]["snow"]["1h"]
                except KeyError:
                    snow = None

                weather = WeatherObject(api["current"]["dt"],
                                        api["current"]["temp"],
                                        api["current"]["feels_like"],
                                        api["current"]["weather"][0]["icon"],
                                        api["current"]["weather"][0]["description"],
                                        rain, snow)
                weather_info.append(weather)
            else:
                try:
                    rain = api["hourly"][i - 1]["rain"]["1h"]
                except KeyError:
                    rain = None
                try:
                    snow = api["hourly"][i - 1]["snow"]["1h"]
                except KeyError:
                    snow = None

                weather = WeatherObject(api["hourly"][i - 1]["dt"],
                                        api["hourly"][i - 1]["temp"],
                                        api["hourly"][i - 1]["feels_like"],
                                        api["hourly"][i - 1]["weather"][0]["icon"],
                                        api["hourly"][i - 1]["weather"][0]["description"],
                                        rain, snow)
                weather_info.append(weather)

        root.geometry('%dx%d' % (weather_x, weather_y))

        weather_info[0].frame.grid(row=0, column=0)
        weather_info[2].frame.grid(row=0, column=1)
        weather_info[5].frame.grid(row=0, column=2)
        weather_info[8].frame.grid(row=0, column=3)
        weather_info[14].frame.grid(row=0, column=4)
        weather_info[20].frame.grid(row=0, column=5)
        weather_info[26].frame.grid(row=0, column=6)


root = Tk()

config_file = "../Config/config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config["api_key"]["key"]

try:
    home_city, lat, lon = geocoder.ip("me").city, geocoder.ip("me").lat, geocoder.ip("me").lng
except json.decoder.JSONDecodeError as loc_err:
    home_city, lat, lon = "London", 0, 0

url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}"

clock_date = Label(root)
clock_date.pack()
clock_time = Label(root)
clock_time.pack()

img = ""
weather_info = []
weather_frame = Frame(root)

start_time = time.time()
font_size = 32
font_color = "#00ffff"
font = Font(family="helvetica", size=font_size)

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

print(home_city, lat, lon)

open_clock()

root.mainloop()
