import PySimpleGUI as sg
import sys
import requests

sg.theme('Dark Brown')
layout = [
    [sg.Text('City:'), sg.InputText(key='-IN-'), sg.Submit("Узнать погоду!")],
    [sg.Button("Москва", size=(20,1)), sg.Button("Санкт Пeтербург", size=(20,1)),	sg.Button("Новосибирск", size=(20,1))], 
    [sg.Button("Екатеринбург", size=(20,1)), sg.Button("Казань", size=(20,1)), sg.Button("Нижний Новгород", size=(20,1))], 
    [sg.Button("Челябинск", size=(20,1)), sg.Button("Самара", size=(20,1)), sg.Button("Омск", size=(20,1))], 
    [sg.Button("Ростов-на-Дону", size=(20,1)),	sg.Button("Уфа", size=(20,1)), sg.Button("Красноярск", size=(20,1))], 
    [sg.Button("Воронеж", size=(20,1)), sg.Button("Пермь", size=(20,1)), sg.Button("Волгоград", size=(20,1))],
    [sg.Button("Обнинск", size=(64,1))],
    [sg.Output(size=(72, 9), key='-OUTPUT-')],
    [sg.Cancel("Закрыть программу")]
]
window = sg.Window("Погода сейчас", layout)
def get_weather():  
        url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
        params = { 'key': '8d23d579b55f4b8f908131431202712',
               'q': city,
               'format': 'json',
               'num_of_days': 1,
               'lang': 'ru'}
        try:
            r = requests.get(url, params=params)
            the_weather = r.json()
            if 'data' in the_weather and 'current_condition' in the_weather['data']:
                return the_weather['data']['current_condition'][0]
            else:
                return 1
        except requests.exceptions.RequestException as e:
            return 2

while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Закрыть программу'):
        break
    flag = 0
    if event == 'Узнать погоду!':	
    	city = values['-IN-']
    	window['-OUTPUT-'].update('')
    else:
    	city = event
    	window['-OUTPUT-'].update('')
    weather = get_weather()
    if weather != 1 and weather != 2:
        st = str(weather['lang_ru'])
        print('                     ',city,
            f'\nВремя замера: {weather["observation_time"]}\nТемпература сейчас {weather["temp_C"]}, ощущается как {weather["FeelsLikeC"]}\n{st[12:-3]}\nСкорость ветра(км/ч): {weather["windspeedKmph"]}\nОсадков(мм): {weather["precipMM"]}\nВлажность {weather["humidity"]}%\nДавление(мм рт. ст.): {weather["pressure"]}')#', font='Helvetica 14')   
    else:
        if weather == 1:
            print('Не удалось распознать город, введите заново.')
        elif weather == 2:
            print('Соединение с сервером разорванно, повторите попытку.')
