import json
import os
import time
import requests
from datetime import datetime
import Config.Config as cfg


# pyinstaller --onefile --windowed --icon="Images\Clock_256.ico" ClockWeather_onScreen.py  # create executable
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

        if cfg.weather_active and (time.time() - cfg.start_time) > 300:
            cfg.start_time = time.time()
            print("Weather update")
            update_weather()
        elif cfg.weather_active:
            cfg.root.geometry("%dx%d" % (cfg.weather_x, cfg.weather_y))
        else:
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
    cfg.root.bind("<Control-Key-w>", set_weather)
    cfg.root.bind("<Control-Key-s>", cfg.settings)

    update_clock()


def update_clock():
    x = cfg.clock_size_x if not cfg.weather_active else cfg.weather_x
    y = cfg.clock_size_y if not cfg.weather_active else cfg.weather_y

    cfg.root.geometry("%dx%d" % (x, y))

    cfg.clock_date.config(text=f"{datetime.now():%a, %b-%d}", fg=cfg.font_color, bg=cfg.bg_color, font=cfg.font)
    cfg.clock_time.config(text=f"{datetime.now():%H:%M:%S  #%V}", fg=cfg.font_color, bg=cfg.bg_color, font=cfg.font)

    cfg.root.update()


def set_weather(event):
    cfg.weather_active = not cfg.weather_active

    if cfg.weather_active:
        cfg.root.title("Weather {}, {}, {}".format(cfg.home_city, cfg.lat, cfg.lon))
        cfg.weather_frame.pack(pady=20)
        cfg.root.geometry("%dx%d" % (cfg.weather_x, cfg.weather_y))
        update_weather()
    else:
        cfg.weather_frame.forget()
        cfg.root.geometry("%dx%d" % (cfg.clock_size_x, cfg.clock_size_y))


def update_weather():
    cfg.weather_info.clear()

    try:
        # print(url.format(lat, lon, exclude, api_key))
        api = requests.get(cfg.url.format(cfg.lat, cfg.lon, cfg.exclude, cfg.api_key))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", err)
        api = None
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        api = None

    if api:
        api = api.json()

        # with open('api_data.json', 'w') as outfile:
        #     json.dump(api, outfile, indent=2)

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

                weather = cfg.WeatherObject(api["current"]["dt"],
                                            api["current"]["temp"],
                                            api["current"]["feels_like"],
                                            api["current"]["weather"][0]["icon"],
                                            api["current"]["weather"][0]["description"],
                                            rain, snow)
                cfg.weather_info.append(weather)
            else:
                try:
                    rain = api["hourly"][i - 1]["rain"]["1h"]
                except KeyError:
                    rain = None
                try:
                    snow = api["hourly"][i - 1]["snow"]["1h"]
                except KeyError:
                    snow = None

                weather = cfg.WeatherObject(api["hourly"][i - 1]["dt"],
                                            api["hourly"][i - 1]["temp"],
                                            api["hourly"][i - 1]["feels_like"],
                                            api["hourly"][i - 1]["weather"][0]["icon"],
                                            api["hourly"][i - 1]["weather"][0]["description"],
                                            rain, snow)
                cfg.weather_info.append(weather)

        cfg.root.geometry('%dx%d' % (cfg.weather_x, cfg.weather_y))

        cfg.weather_info[0].frame.grid(row=0, column=0)
        cfg.weather_info[2].frame.grid(row=0, column=1)
        cfg.weather_info[5].frame.grid(row=0, column=2)
        cfg.weather_info[8].frame.grid(row=0, column=3)
        cfg.weather_info[14].frame.grid(row=0, column=4)
        cfg.weather_info[20].frame.grid(row=0, column=5)
        cfg.weather_info[26].frame.grid(row=0, column=6)


cfg.init()
print(cfg.home_city, cfg.lat, cfg.lon)

open_clock()

cfg.root.mainloop()
