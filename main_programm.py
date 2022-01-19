import pandas as pd
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import vk_bot
import Balaboba
import re
from toxic import get_neut_toxic_rate
from config import root, token


def write_msg_to_chat(chat_id, message):
    authorize.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': get_random_id()})


def write_help(chat_id, username):  # выводит список команд в help
    global intros_for_help
    keys = []
    for key in intros_for_help.keys():
        keys.append(key)
    string_of_keys = '\n'.join(f'{i}) *{key}' for i, key in enumerate(keys, start=1))
    write_msg_to_chat(chat_id, f'Смотри, {username}, одна из функций это '
                               f'подсчёт самых токсичных членов беседы. \n'
                               f'Команда *list с упоминанием выдаст список '
                               f'самых токсичных.\n'
                               f'Вторая функция - это балабоба, чтоб вызвать'
                               f'упоминаешь меня, указывая '
                               f'стиль, который хочешь.  \n'
                               f'{string_of_keys}')


intros = {'без': 0,
          'теории': 1,
          'тв': 2,
          'тосты': 3,
          'пацанские': 4,
          'рекламные': 5,
          'короткие': 6,
          'подписи': 7,
          'короче': 8,
          'синопсисы': 9,
          'гороскоп': 10,
          'народные': 11}  # словарик для перевода стилей в числа

intros_for_help = {'без стиля': 0,
                   'теории заговора': 1,
                   'тв репортажи': 2,
                   'тосты': 3,
                   'пацанские цитаты': 4,
                   'рекламные слоганы': 5,
                   'короткие истории': 6,
                   'подписи в инстаграм': 7,
                   'короче википедия': 8,
                   'синопсисы фильмов': 9,
                   'гороскоп': 10,
                   'народные мудрости': 11}  # тот же словарик но выводится при вызове команды help

authorize = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(authorize, group_id=207826436)
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
        if event.message.get('text') != '':
            message_from_chat = event.message.get('text')
            mention_sobaka = re.findall(r'@(\w+)', message_from_chat)
            mention_zvezda = re.findall(r'\*(\w+)', message_from_chat) # оба смотрят есть ли упоминание бота
            # if mention_zvezda != [] and mention_zvezda[-1] == 'list':
            #     df = pd.read_csv(root + r'/neutral_toxic_rate' + str(event.chat_id) + '.csv', delimiter=',')
            #     df.sort_values(by=0, axis=1, inplace=True, ascending=False)
            #     text = ''
            #     sum = df.iloc[0].sum()
            #     for i in list(df.columns.values):
            #         text += f'{i} имеет рейтинг токсичности {round(df[i][0] / sum * 100, 2)}%\n'
            #     chat_id = event.chat_id
            #     write_msg_to_chat(chat_id, text)

            if (mention_sobaka != [] and mention_sobaka[0] == 'balabibba') \
                    or (mention_zvezda != [] and mention_zvezda[0] == 'balabibba'):
                if event.message.get('reply_message') is None \
                        and event.message.get('fwd_messages') == []:  # если мэссэдж без ответов и пересылок
                    bot = vk_bot.VkBot(event.message.get('from_id'))
                    recieved_message = event.message.get('text')
                    # text_of_balaboba = Balaboba.zabalobobit(recieved_message)
                    chat_id = event.chat_id
                    command = re.findall(r'\*(\w+)', recieved_message)
                    if command[-1] != 'help':
                        write_msg_to_chat(chat_id, f'{bot._USERNAME}, *help пропиши')
                    else:
                        write_help(chat_id, bot._USERNAME)

                elif event.message.get('reply_message') is not None:  # сообщением с ответом
                    text_of_reply = event.message.get('reply_message').get('text')
                    print(text_of_reply)
                    intro = re.findall(r'\*(\w+)', event.message.get('text'))
                    if intro != [] and intro[-1] in intros:
                        number_of_intro = intros.get(intro[-1])
                    else:
                        number_of_intro = 0
                    text_of_balaboba = Balaboba.zabalobobit(text_of_reply, number_of_intro)
                    chat_id = event.chat_id
                    bot = vk_bot.VkBot(event.message.get('reply_message').get('from_id'))
                    # write_msg_to_chat(chat_id, f'{bot._USERNAME}, вот что придумал балабоба')
                    write_msg_to_chat(chat_id, f'{text_of_balaboba}')

                elif event.message.get('fwd_messages') != []:  # собщение с пересылкой
                    fwd_messages = event.message.get('fwd_messages')
                    text_of_reply = ' '.join([fwd_messages[i].get('text') for i in range(len(fwd_messages))])
                    intro = re.findall(r'\*(\w+)', event.message.get('text'))
                    if intro != [] and intro[-1] in intros:
                        number_of_intro = intros.get(intro[-1])
                    else:
                        number_of_intro = 0
                    text_of_balaboba = Balaboba.zabalobobit(text_of_reply, number_of_intro)
                    chat_id = event.chat_id
                    bot = vk_bot.VkBot(event.message.get('fwd_messages')[0].get('from_id'))
                    # write_msg_to_chat(chat_id, f'{bot._USERNAME}, вот что придумал балабоба')
                    write_msg_to_chat(chat_id, f'{text_of_balaboba}')

            # else:
            #     message = event.message.get('text')
            #     neutral, toxic = get_neut_toxic_rate(message)
            #     if toxic > neutral:
            #         try:
            #             df = pd.read_csv(root + r'/neutral_toxic_rate' + str(event.chat_id) + '.csv', delimiter=',')
            #         except:
            #             df = pd.DataFrame()
            #         bot = vk_bot.VkBot(event.message.get('from_id'))
            #         name = bot._USERNAME_WITH_SURNAME.strip()
            #         if name in set(df.columns.values):
            #             df[name][0] += 1
            #         else:
            #             print('check')
            #             df[name] = [1]
            #         df.to_csv(root + r'/neutral_toxic_rate' + str(event.chat_id) + '.csv', index=False, encoding='utf-8-sig')
