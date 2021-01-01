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
ICON = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAFOElEQVRoge2ZXWwUVRTHf3e6/ZJtQUA+CwYiH1KUD0sEXyHGEGk0WrSm+iCBgIQH4gOGaNIYNbyYEAUMGoHEKBGBl6KJYkASDCaEEJSgaIJaCALChna77X7MPceH2S7bdj9mt1tKYk9yM5kzc2d+/3vPPXNmBkZsxP7fZkp1ofgxFojLcpSlCHMQpqkQVAGELpR2VX43LqdEORZ8kXOluO+gBOhJamIJ1hnLGoSHVQCFJHRqm8mnygUjfNpdyccTVtN1VwXocQIJwyYV3kQYmwLzD+8d83y3VHin9jI7TCvukAuIHWeuMexXYSHpYMXBp2/PGktz7WtcLITHKeTk6AkajeF0yeEVVM0iwZwO7WTVkAiI/8DLjnJIhWDJ4cX07tcYaw6HttPil8tXCEVP0JiEDwwhfHp/F9Fnx77OkUELiJ5glqOcUaHmLsH3+ro0oUvGb+W3XHw5Q0iPE3CUA8MAD0IQx3yurQSKFpBMlaVfsPnhe/svDpWxMRdj1hDSbxkVK+cvI4wfJngQEOGWqdQZD2whXNAMxCpYP9zwKmCEcXSxNhtnVgHJ8mBY4Xu3gllTkID4MRZQeG0zJPB4/nnXtjLftwBxWXGvwKf6WZb7FoDy+D0FL4A4yzKhZs6xwtyhhBcLrgvROCRczx8wUFUGZYDpB+9dU+f4FqDKlKGCj8ahk8lUP7ae2jkrqbh/BmLjRG9eouOXNqJn9zHGvU6FGTAbdZlYMz4HetqIqVBRavhwD8SmNzGlcQdOZQ2qmmqiioriRkJcO7iJ0e1HKDd9+scmb9eq/qwZ18BQjXx0WhN1z+3DlAexVvo0sYKIYKpGM6F5Dx1TnyIcha4ouDZ5nQyWbQ2EUcaVcsHe1onUrfoAmzbqfUY/vWEY17wHFSURvk7416PYkx/1wJ8DUDPOgFGulgredSEShcpH10J5EBHB9muS1lI+dRAcnOAkgg0tBDd8V3up/eqTA1gzCYgc4gCWpsHAuwkIxaopX7SZmvlNlI95EIyDiqJK9tHPNTMqYSP2kZkzZ/6dM4SM5ScRmoqFTyTgRqSa8avbqK5bcgdApB8UeYAH+GtEzRvAhpwCxOV7KA5eLdyOQFXDZqqmNmBFfI5wHjGS8q9MZ824BoIv8bPC+WKzTXcMgvVNWeO7T+wnM5C1NtnSslLqWJ8+E/MKSIbR3mKyTcL10l7ZqEmZU2U6lM20kC1WbMZFnty/5ktAl7JblZuF1jbWetvY7Sv5Rz/nMTtAjIggar/xJWDSK0TU8m7BhZl6F+04d2DgzfOJ6Tdjd2YtFV6dFt3mSwBA7WV2IJwtpKoM4BVmHT9+SHf7aW8U02I7ayjZ3EJFpVOsfb6hvr49nTHvZ5WOnTykxpxRodZPeRGNezVPJAY9UkVw6Qbum/cMzug6MA7SL9vkyfuiyhUR/dqxzraGhr7wvgQAhHayylhzGCWQ7wkt1oPvjkEsAbG457PJWqb3/EyzmXz7wihuVYW+sOxLDudj8/1xN7SdFtTsRdJEZHlOuDZZ6ye8rGRtEr7fud430QH93YDVdQsPstcPV0Ffp0Pv87SK+QKhJt+blFiwSXj183bn7Xei2jLrM9r8MhX8ef3f95htHLMfYXE2eLL4ciUBlDMq2jxtH38UwlPcD45WAqEyNlo1bxlJlt3Fw99Uq2/XRdhlvsIWyjKoX0w3Wgkayzowr4pQXxC8ch6reyoq+WTCrrv8iymT/bOFegMrUOcJRGerMJ07P/nCKJdVzEUjcsrA0cm7uVCqe4/YiI3YiA2f/QfuwWUprzQc8gAAAABJRU5ErkJggg=='
window = sg.Window("WeatherOnline", layout, icon=ICON, finalize=True)
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
