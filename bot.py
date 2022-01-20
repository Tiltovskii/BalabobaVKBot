from vkbottle.bot import Bot, Message
from config import *
from Balaboba import zabalobobit
import pandas as pd
from toxic import *
import os
bot = Bot(token=token)


@bot.on.chat_message(func=lambda message: message.is_mentioned and message.text == 'clear')
async def clear_handler(message: Message):
    if message.from_id == admin_id:
        try:
            os.remove(root + r'neutral_toxic_rate' + str(message.chat_id) + '.csv')
            await message.answer('Рейтинг токсичности обнулен')
        except:
            await message.answer('Ошибочка, дружок, директории не существует')
    else:
        await message.answer('Ты не обладаешь правами, дружок')


@bot.on.chat_message(func=lambda message: message.is_mentioned and message.text == 'help')
async def help_handler(message: Message):
    keys = []
    for key in intros_for_help.keys():
        keys.append(key)
    string_of_keys = '\n'.join(f'{i}) {key}' for i, key in enumerate(keys, start=1))
    users_info = await bot.api.users.get(message.from_id)
    username = users_info[0].first_name
    await message.answer(f'Привет, {username}, одна из функций этого бота - это '
                         f'подсчёт самых токсичных членов беседы. \n'
                         f'Команда list с упоминанием выдаст список '
                         f'самых главных токсиков чата.\n'
                         f'Если хочешь почистить рейтинг, то с упоминанием напиши clear. \n'
                         f'Вторая функция - это балабоба от Яндекса (надеюсь вы с ней знакомы), чтоб вызвать'
                         f'упоминаешь меня, указывая '
                         f'стиль, который хочешь.  \n'
                         f'{string_of_keys}')


@bot.on.chat_message(func=lambda message: message.is_mentioned and message.fwd_messages != [])
async def balaboba_fwd_handler(message: Message):
    if message.text != "" and message.text.lower() in intros_for_help.keys():
        intros = intros_for_help[message.text.lower()]
    else:
        intros = 1
    response = await zabalobobit(message.fwd_messages[-1].text, intros)
    await message.answer(response)


@bot.on.chat_message(func=lambda message: message.is_mentioned and message.reply_message is not None)
async def balaboba_response_handler(message: Message):
    if message.text != "" and message.text.lower() in intros_for_help.keys():
        intros = intros_for_help[message.text.lower()]
    else:
        intros = 1
    response = await zabalobobit(message.reply_message.text, intros)
    await message.answer(response)


@bot.on.chat_message(func=lambda message: message.is_mentioned and message.text == 'list')
async def toxic_list_handler(message: Message):
    try:
        df = pd.read_csv(root + r'neutral_toxic_rate' + str(message.chat_id) + '.csv', delimiter=',')
        df.sort_values(by=0, axis=1, inplace=True, ascending=False)
        text = ''
        sum = df.iloc[0].sum()
        for i in list(df.columns.values):
            text += f'{i} имеет рейтинг токсичности {round(df[i][0] / sum * 100, 2)}%\n'
        await message.answer(text)
    except:
        await message.answer('Ошибочка, дружок, нет списочка')


@bot.on.chat_message()
async def neutral_toxic_rate_rec(message: Message):
    text_of_the_message = message.text
    neutral, toxic = await toxic_site(text_of_the_message)
    if toxic > neutral:
        try:
            df = pd.read_csv(root + r'neutral_toxic_rate' + str(message.chat_id) + '.csv', delimiter=',')
        except:
            df = pd.DataFrame()
        users_info = await bot.api.users.get(message.from_id)
        if users_info:
            username = users_info[0].first_name
            surname = users_info[0].last_name
            name = username + ' ' + surname
            if name in set(df.columns.values):
                df[name][0] += 1
            else:
                df[name] = [1]
            print('check ' + name)
            df.to_csv(root + r'neutral_toxic_rate' + str(message.chat_id) + '.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    print('Bot is starting...')
    bot.run_forever()
