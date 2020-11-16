import requests
import os
from bs4 import BeautifulSoup

URL = 'https://www.timeserver.ru/cities/ru/irkutsk'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.198 Safari/537.36 ',
    'Accept': '*/*'
}


def getTime():
    html = requests.get(URL, headers=HEADERS).text
    data = BeautifulSoup(html, 'html.parser')
    time = data.find('div', class_='timeview-info-date')
    day = time.find_next('span', {'data-prop': 'week_day'}).get_text()
    date = time.find_next('span', {'data-prop': 'date_short'}).get_text()
    week = time.find_next('span', {'data-prop': 'week_num'}).get_text()
    if int(week) % 2 == 0:
        week = 'Числитель'
    else:
        week = 'Знаменатель'
    today = date + ', ' + day + ', ' + week
    if 'Понедельник' in day:
        day = 1
    elif 'Вторник' in day:
        day = 2
    elif 'Среда' in day:
        day = 3
    elif 'Четверг' in day:
        day = 4
    elif 'Пятница' in day:
        day = 5
    elif 'Суббота' in day:
        day = 6
    elif 'Воскресенье' in day:
        day = 7
    return today, day



