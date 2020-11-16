import requests
import getDate
from random import randint

token = ''  # enter the token (group or standalone application)
version = 5.126
group_id =
own_id =
masters =


def sendMessage(message, peer_id, attach=None):    # отправка сообщения, передаем: текст, id диалога, вложения
    random_id = randint(-2147483648, 2147483647)
    data = requests.get('https://api.vk.com/method/messages.send',
                        params={
                            'access_token': token,
                            'peer_id': peer_id,
                            'random_id': random_id,
                            'message': message,
                            'v': version,
                            'attachment': attach
                        })
    # print(data.json())


def getLongPull():   # получаем данные, необходимые для подключения к long pull
    data = requests.get('https://api.vk.com/method/groups.getLongPollServer',
                        params={
                            'access_token': token,
                            'group_id': group_id,
                            'v': version
                        })
    try:
        return data.json()['response']['server'], data.json()['response']['key'], data.json()['response']['ts']
    except:
        sendMessage('CAN`T CONNECT TO LONG PULL SERVER \n' + str(data.json()['error']['error_msg']), own_id)


def checkEvent():  # прослушиваем события, подключаясь к long pull
    long_pull_data = getLongPull()
    ts = long_pull_data[2]
    while True:
        data = requests.get(long_pull_data[0] +
                            '?act=a_check&key=' + long_pull_data[1] + '&ts=' + ts + '&wait=29')
        if 'failed' in data.json():  # раз в час ключ доступа сбрасывается, опять получаем данные для подключения
            sendMessage('need new long data', own_id)
            long_pull_data = getLongPull()
            continue
        try:
            if not data.json()['updates']:  # если событий нет, продолжаем прослушивание
                ts = data.json()['ts']
                sendMessage('wait', own_id)
            else:
                # print('have a new event')
                type_of_event = data.json()['updates'][0]['type']
                if type_of_event == 'message_new':   # пришло сообщение
                    message = data.json()['updates'][0]['object']['message']
                    isMessage(message)
                else:
                    print('another event')  # какое-то другое событие
                ts = data.json()['ts']
        except:
            sendMessage('ошибка_2', own_id)  # debug


def isMessage(message):  # обрабатываем пришедшее сообщение
    # print('it`s message')
    sender_id = message['from_id']  # id отправителя
    text = message['text'].lower()  # текст сообщения
    peer_id = message['peer_id']    # id диалога, если сообщение личное, то равен id отправитея
    sender_data = whoIs(sender_id)  # информция о отрпавителе
    # print('message -', text, '\n'
    #                          'from -', sender_data['name'], sender_data['last_name'], '\n'
    #                                                                                   'in -', peer_id)
    if 'reply_message' in message:  # проверяем: сообщение ответ на другое сообщение?
        if message['reply_message']['from_id'] == -group_id:  # если это ответ на сообщение группы, то не получаем инфу
            isCommand(text, sender_data, peer_id)             # о том, кому этот ответ адресован(группе)
        else:
            reply_data = whoIs(message['reply_message']['from_id'])  # иначе получаем такую информацию
            isCommand(text, sender_data, peer_id, reply_data)
    else:
        isCommand(text, sender_data, peer_id)


def isCommand(message, sender_data, peer_id, reply_data=None):  # проверяем: сообщение - команда боту?
    s_id = sender_data['id']
    dialog = peer_id
    # if message == '':
    # что-нибудь делаем


def whoIs(id):  # расширенная информацию о пользователе по его id
    data = requests.get(
        'https://api.vk.com/method/users.get?',
        params={
            'user_ids': id,
            'access_token': token,
            'v': version
        })
    user = dict()
    user['id'] = id
    user['name'] = data.json()['response'][0]['first_name']
    user['last_name'] = data.json()['response'][0]['last_name']
    user['link'] = '@id' + str(id) + '(' + user['name'] + ' ' + user['last_name'] + ')'
    return user


checkEvent()
