import PySimpleGUI as sg
import sys
import requests
import http.client

#Создаю интерфейс
sg.theme('Dark Brown')
layout = [
    [sg.Text('City:'), sg.InputText(key='-IN-'), sg.Submit("Узнать погоду!")],
    [sg.Button("Москва", size=(20,1)), sg.Button("Санкт Пeтербург", size=(20,1)),	sg.Button("Новосибирск", size=(20,1))], 
    [sg.Button("Екатеринбург", size=(20,1)), sg.Button("Казань", size=(20,1)), sg.Button("Нижний Новгород", size=(20,1))], 
    [sg.Button("Челябинск", size=(20,1)), sg.Button("Самара", size=(20,1)), sg.Button("Омск", size=(20,1))], 
    [sg.Button("Ростов-на-Дону", size=(20,1)),	sg.Button("Уфа", size=(20,1)), sg.Button("Красноярск", size=(20,1))], 
    [sg.Button("Воронеж", size=(20,1)), sg.Button("Пермь", size=(20,1)), sg.Button("Волгоград", size=(20,1))],
    [sg.Button("Обнинск", size=(64,1))],
    [sg.Multiline(size=(45, 9), key='-OUTPUT-'+sg.WRITE_ONLY_KEY,font=('Helvetica', 14))],
    [sg.Cancel("Закрыть программу")]
]
window = sg.Window("Погода сейчас", layout, finalize=True)
#-------------------------------------------------------------------------------
#запрос и обработка ответа с сервера
url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
def get_weather(flag):
        if flag == False: #при flag = false создается запрос по ip пользователя
            try:
                tempQ =  requests.get("https://ramziv.com/ip").text
            except requests.exceptions.RequestException as e:
                return 2
            params = { 'key': '8d23d579b55f4b8f908131431202712',
               'q': tempQ,
               'format': 'json',
               'num_of_days': 1,
               'lang': 'ru'}
        else: #запрос по названию города
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
#--------------------------------------------------------------------------------
#первоначальное определение погоды по ip
weather = get_weather(False)
if weather != 1 and weather != 2:
    st = str(weather['lang_ru'])
    press = float(weather["pressure"]) * 0.75
    window['-OUTPUT-'+sg.WRITE_ONLY_KEY].print('                     Погода по вашему ip',
            f'\nВремя замера: {weather["observation_time"]}\nТемпература сейчас {weather["temp_C"]}, ощущается как {weather["FeelsLikeC"]}',
            f'\n{st[12:-3]}\nСкорость ветра(км/ч): {weather["windspeedKmph"]}\nОсадков(мм): {weather["precipMM"]}\nВлажность {weather["humidity"]}%\nДавление(мм рт. ст.): {press}') 
else:
    if weather == 1:
        window['-OUTPUT-'+sg.WRITE_ONLY_KEY].print('Не удалось распознать город, введите заново.')
    elif weather == 2:
        window['-OUTPUT-'+sg.WRITE_ONLY_KEY].print('Соединение с сервером разорванно, повторите попытку.')
#---------------------------------------------------------------------------------
# The Event Loop
while True:                             
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Закрыть программу'):
        break
    if event == 'Узнать погоду!':	
    	city = values['-IN-']  
    	window['-OUTPUT-'+sg.WRITE_ONLY_KEY].update('')
    else:
    	city = event
    	window['-OUTPUT-'+sg.WRITE_ONLY_KEY].update('')
    weather = get_weather(True)
    if weather != 1 and weather != 2:
        st = str(weather['lang_ru'])
        press = float(weather["pressure"]) * 0.75
        window['-OUTPUT-'+sg.WRITE_ONLY_KEY].print(f'                     {city}\nВремя замера: {weather["observation_time"]}\nТемпература сейчас {weather["temp_C"]}, ощущается как {weather["FeelsLikeC"]}',
            f'\n{st[12:-3]}\nСкорость ветра(км/ч): {weather["windspeedKmph"]}\nОсадков(мм): {weather["precipMM"]}\nВлажность {weather["humidity"]}%\nДавление(мм рт. ст.): {press}') 
    else:
        if weather == 1:
             window['-OUTPUT-'+sg.WRITE_ONLY_KEY].print('Не удалось распознать город, введите заново.')
        elif weather == 2:
             window['-OUTPUT-'+sg.WRITE_ONLY_KEY].print('Соединение с сервером разорванно, повторите попытку.')
