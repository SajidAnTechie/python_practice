import requests
import threading
from io import BytesIO
from pytz import timezone
from random import randint
from urllib import request
from datetime import datetime
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from tkinter import messagebox, Label, Entry, PhotoImage, Tk, Button, BOTTOM, ttk, END


def api_thread():
    global current_value
    global process_id
    try:
        progress_bar.place(x=300, y=250)
        progress_percentage.place(x=450, y=250)
        progress_bar['value'] = 0
        progress_percentage.config(text='0%')
        search_icon_button.config(state='disabled')
        textField.config(state='disabled')

        update_progress()
        get_weather()
        progress_bar['value'] = 100
        progress_percentage.config(text='100%')
        root.after(1000, progress_percentage.place_forget)
        root.after(1000, progress_bar.place_forget)
    except Exception as e:
        root.after(0, progress_percentage.place_forget)
        root.after(0, progress_bar.place_forget)
        messagebox.showerror('Weather App', str(e))
    finally:
        search_icon_button.config(state='active')
        textField.config(state='normal')
        current_value = 0
        root.after_cancel(process_id)


def get_random_num_btw(num: int):
    return randint(num, num + 10)


current_value = 0
process_id = 0


def update_progress():
    global current_value
    global process_id

    next_value = get_random_num_btw(current_value)
    current_value = next_value
    progress_bar['value'] = current_value

    if progress_bar['value'] < 90:
        progress_percentage.config(text=(f'{int(progress_bar['value'])}%'))
        process_id = root.after(1000, update_progress)
    if progress_bar['value'] >= 90:
        progress_bar['value'] = 90
        progress_percentage.config(text=('90%'))


def get_current_time_by_city(city_name: str):
    try:
        geolocator = Nominatim(user_agent='geoapi')
        location = geolocator.geocode(city_name)
        tf = TimezoneFinder()
        tz = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        home = timezone(tz)
        time = datetime.now(home)
        return time

    except Exception as e:
        raise Exception(f"Unable to get weather for {city_name} city")


def get_weather_by_city_name(city_name: str):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=53dacc8f4ab77c24fab1a3dfd35e67ee&units=metric")
    data = response.json()
    return data


def get_weather():
    city_name = textField.get()
    if not city_name:
        raise Exception(f"City name is invalid")

    # time
    time = get_current_time_by_city(city_name)
    current_time = time.strftime('%I:%M %p')

    # API
    data = get_weather_by_city_name(city_name)
    icon_id = data['weather'][0]['icon']

    url = f'https://openweathermap.org/img/wn/{icon_id}@4x.png'
    image_data = request.urlopen(url).read()
    image = Image.open(BytesIO(image_data))
    tk_image = ImageTk.PhotoImage(image)

    if data['cod'] == '404':
        raise Exception(f'Unknown city name {city_name}')

    name.config(text='CURRENT WEATHER')
    clock.config(text=current_time)
    condition = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = float(data['main']['temp'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    feels_like = data['main']['feels_like']
    wind = data['wind']['speed']

    temp_label.config(text=(temp, '°C'))
    condition_label.config(text=(condition, '|', 'FEELS', 'LIKE', feels_like, '°C'))

    wind_label.config(text=wind)
    humidity_label.config(text=humidity)
    description_label.config(text=description)
    pressure_label.config(text=pressure)
    logo_label.config(image=tk_image)
    logo_label.image = tk_image


def start_api_call():
    thread = threading.Thread(target=api_thread)
    thread.start()


root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# search box
search_box = PhotoImage(file='./icons/search.png')
search_box_label = Label(image=search_box)
search_box_label.place(x=20, y=20)

textField = Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg='#404040', border=0.0, fg='#ffffff', highlightthickness=0)
textField.insert(0, 'Enter city name')
textField.place(x=50, y=40)
textField.bind("<FocusIn>", lambda event: textField.delete(0, END))
# textField.focus()

search_icon = PhotoImage(file='./icons/search_icon.png')
search_icon_button = Button(image=search_icon, borderwidth=0, border=0, cursor='hand2', bg='#404040', command=start_api_call, highlightthickness=0, height=40, justify='center', relief='raised')
search_icon_button.place(x=400, y=40)

# logo
logo = PhotoImage(file='./icons/logo.png')
logo_label = Label(image=logo)
logo_label.place(x=150, y=100)

# bottom box
frame_box = PhotoImage(file='./icons/box.png')
frame_box_label = Label(image=frame_box)
frame_box_label.pack(padx=5, pady=5, side=BOTTOM)

# time
name = Label(root, font=('arial', 15, 'bold'))
name.place(x=30, y=100)
clock = Label(root, font=('Helvetica', 20))
clock.place(x=30, y=130)

# label
label1 = Label(root, text='WIND', font=('Helvetica', 15, 'bold'), fg='#ffffff', bg='#1ab5ef')
label1.place(x=120, y=410)

label2 = Label(root, text='HUMIDITY', font=('Helvetica', 15, 'bold'), fg='#ffffff', bg='#1ab5ef')
label2.place(x=250, y=410)

label3 = Label(root, text='DESCRIPTION', font=('Helvetica', 15, 'bold'), fg='#ffffff', bg='#1ab5ef')
label3.place(x=430, y=410)

label4 = Label(root, text='PRESSURE', font=('Helvetica', 15, 'bold'), fg='#ffffff', bg='#1ab5ef')
label4.place(x=650, y=410)

temp_label = Label(font=('arial', 70, 'bold'), fg='#ee666d')
temp_label.place(x=400, y=150)
condition_label = Label(font=('arial', 15, 'bold'))
condition_label.place(x=400, y=250)

wind_label = Label(text='...', font=('arial', 13, 'bold'), bg='#1ab5ef')
wind_label.place(x=120, y=440)

humidity_label = Label(text='...', font=('arial', 13, 'bold'), bg='#1ab5ef')
humidity_label.place(x=250, y=440)

description_label = Label(text='...', font=('arial', 13, 'bold'), bg='#1ab5ef')
description_label.place(x=435, y=440)

pressure_label = Label(text='...', font=('arial', 13, 'bold'), bg='#1ab5ef')
pressure_label.place(x=650, y=440)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress_percentage = Label(font=('arial', 13, 'bold'))


root.mainloop()
