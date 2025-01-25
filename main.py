# Импорт библиотек
import telebot
from telebot import types
from time import sleep
import datetime
from telebot.types import InputMediaPhoto
from info import *
from config import token

bot = telebot.TeleBot(token)

kol_vo = 0

mar = types.ReplyKeyboardMarkup(one_time_keyboard=True)
list_marsh = ["Путь освобождения", "Братские могилы", "Парки и скверы", "История города в памятниках",
              "Прогулка по музеям", "Развлекательный", "Классический", "Религиозный", "Гастрономический", "Искусство",
              "Ремесленный", "Сельскохозяйственный", "Природные красоты", "Водный отдых", "Испытать удачу", "В меню"]

for i in list_marsh:
    mar.add(types.KeyboardButton(i))

z = types.ReplyKeyboardMarkup(one_time_keyboard=True)
animals = ["Волк", "Лиса", "Кабан", "Лось", "Косуля", "Ласка", "Хорёк", "Суслик", "Бобр", "Журавль", "Воробей", "Утка",
           "Заяц-русак", "Вернуться к маршрутам", "В меню"]
for i in animals:
    z.add(types.KeyboardButton(i))


# Функция получения сообщения команды 'start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global kol_vo
    offset = datetime.timezone(datetime.timedelta(hours=3))
    fo_time = str(datetime.datetime.now(offset))
    f_time = fo_time.split('.')[0]
    f_time = f_time.split()
    test = open('user_information.txt', 'a')
    test.write(f"{f_time[1]} {f_time[0]} | id: {message.from_user.id}\n")
    test.close()
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    markup.add(button_yes)
    bot.reply_to(message,
                 'Привет! Ты турист или житель города Россошь? Сегодня я буду твоим гидом по нашему краю.\nРассказать тебе про него?',
                 parse_mode='html', reply_markup=markup)
    kol_vo = 0


# Функция получения сообщения нажатием кнопки
@bot.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.message:

        # Основное меню
        menu = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        but1 = types.KeyboardButton("Маршруты")
        but2 = types.KeyboardButton("Обратная связь")
        menu.add(but1, but2)

        if function_call.data in ['lasy', 'zry', 'wy']:
            h = k[function_call.data]
            n = marsh[h]
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Постороить маршрут", url=n[0])
            button2 = types.InlineKeyboardButton("Узнать подробнее про точки", url=n[1])
            markup.add(button1, button2)
            media = [InputMediaPhoto(n[3]), InputMediaPhoto(n[4])]
            bot.send_media_group(function_call.message.chat.id, media)
            bot.send_photo(function_call.message.chat.id, n[2], n[5], reply_markup=markup)

        if function_call.data not in ['lasy', 'zry', 'wy'] and function_call.data in k:
            h = k[function_call.data]
            n = marsh[h]
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Постороить маршрут", url=n[0])
            button2 = types.InlineKeyboardButton(text="Узнать подробнее про точки", callback_data=n[1])
            markup.add(button1, button2)
            media = [InputMediaPhoto(n[3]), InputMediaPhoto(n[4])]
            bot.send_media_group(function_call.message.chat.id, media)
            bot.send_photo(function_call.message.chat.id, n[2], n[5], reply_markup=markup)

        if function_call.data == "yes":
            m = 'Россошь - город с населением в 60 тыс. человек в Воронежской области. С 2014 года - "Населённый пункт воинской доблести". Название происходит от старославянского "рассоха" - развилка реки. Город расположен на реках Чёрная Калитва и Сухая Россошь.'
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            btn1 = types.KeyboardButton("Продолжить")
            markup.add(btn1)
            bot.send_message(function_call.message.chat.id, 'Продолжим?', reply_markup=markup)
            bot.send_photo(function_call.message.chat.id,
                           'AgACAgIAAxkBAAIPr2YeW6ag1yK_LA528A7PZ9IxdmQQAAKK1TEbDt7xSBZ-CWnz93YdAQADAgADcwADNAQ', m)
        elif function_call.data == "no":
            bot.send_message(function_call.message.chat.id, 'С кого начнём?', reply_markup=z)
            bot.delete_message(function_call.message.chat.id, function_call.message.id)

        elif function_call.data in tochc_in_marsh and function_call.data != 'pamat' and function_call.data != 'prirod_krasot':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Подробнее о локациях", callback_data=function_call.data[:-1])
            markup.add(button1)
            bot.send_message(function_call.message.chat.id,
                             'Что ж, давайте расскажу вам более подробно про маршрут нашего следования:')
            y = '✨' + '\n✨'.join(tochc_in_marsh[function_call.data])
            bot.send_message(function_call.message.chat.id, y, reply_markup=markup)

        elif function_call.data == 'pamat' or function_call.data == 'prirod_krasot':
            bot.send_message(function_call.message.chat.id,
                             'Что ж, давайте расскажу вам более подробно про маршрут нашего следования:')
            y = '✨' + '\n✨'.join(tochc_in_marsh[function_call.data])
            bot.send_message(function_call.message.chat.id, y)

        elif function_call.data in your:
            l = your[function_call.data][0]
            n = toch[l]
            bot.send_photo(function_call.message.chat.id, n[1], n[0])

            for i in range(1, len(your[function_call.data])):
                sleep(3)
                l = your[function_call.data][i]
                n = toch[l]
                bot.send_photo(function_call.message.chat.id, n[1], n[0])

            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="Построить маршрут", url=link[function_call.data])
            button2 = types.InlineKeyboardButton(text='Вернуться назад', callback_data='naz')
            markup.add(button1, button2)
            bot.send_message(function_call.message.chat.id,
                             'Это была последняя точка. Хотите построить маршрут или вернуться назад?',
                             reply_markup=markup)


        elif function_call.data == 'naz':
            bot.send_message(function_call.message.chat.id,
                             'Продолжим наше путешествие. Каким будет следующий маршрут?', reply_markup=mar)

        elif function_call.data == 'men':
            id = function_call.message.id
            bot.send_message(function_call.message.chat.id, 'Ваш выбор', reply_markup=menu)

        elif function_call.data == 'not_its_me':
            id = function_call.message.id
            bot.delete_message(function_call.message.chat.id, id - 1)
            bot.delete_message(function_call.message.chat.id, id)


@bot.message_handler(content_types=['text'])
def func(message):
    global kol_vo

    menu = types.ReplyKeyboardMarkup()
    but1 = types.KeyboardButton("Маршруты")
    but2 = types.KeyboardButton("Обратная связь")
    menu.add(but1, but2)

    if message.text in ['Религиозный', 'Путь освобождения', 'Братские могилы']:
        n = marsh[message.text]
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Постороить маршрут", url=n[0])
        button2 = types.InlineKeyboardButton("Узнать подробнее про точки", url=n[1])
        markup.add(button1, button2)
        media = [InputMediaPhoto(n[3]), InputMediaPhoto(n[4])]
        bot.send_media_group(message.chat.id, media)
        bot.send_photo(message.chat.id, n[2], n[5], reply_markup=markup)

    if message.text not in ['Религиозный', 'Путь освобождения', 'Братские могилы'] and message.text in marsh:
        n = marsh[message.text]
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Постороить маршрут", url=n[0])
        button2 = types.InlineKeyboardButton(text="Узнать подробнее про точки", callback_data=n[1])
        markup.add(button1, button2)
        media = [InputMediaPhoto(n[3]), InputMediaPhoto(n[4])]
        bot.send_media_group(message.chat.id, media)
        bot.send_photo(message.chat.id, n[2], n[5], reply_markup=markup)

    if message.text == "Продолжить":
        bot.delete_message(message.chat.id, message.message_id)
        m = "Герб города: В серебряном поле лазурный повышенный волнистый опрокинутый вилообразный крест. В клиновидном изумрудном окончании, окантованным сверху серебром, золотое яблоко с двумя таковыми же листьями."
        bot.send_photo(message.chat.id,
                       'AgACAgIAAxkBAAIRZ2YetRZVPCJ8OLDZKqL50kq_okFPAAIp2TEbtoj5SHTy7RFGihhJAQADAgADcwADNAQ', m)
        bot.send_message(message.chat.id, 'Что ж, начнём', reply_markup=menu)

    if message.text == 'Маршруты':
        if kol_vo == 1:
            bot.send_message(message.chat.id, 'Готовы начать наше путешествие? Выберите маршрут:', reply_markup=mar)
            bot.delete_message(message.chat.id, message.message_id)
        else:
            kol_vo += 1
            bot.send_message(message.chat.id, 'Готовы продолжить? Выберите маршрут:', reply_markup=mar)

    if message.text in zveri:
        n = zveri[message.text]
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Это про меня', callback_data=n[1])
        btn2 = types.InlineKeyboardButton(text='Это не про меня', callback_data='not_its_me')
        markup.add(btn1, btn2)
        bot.send_photo(message.chat.id, n[2], n[0], reply_markup=markup)

    if message.text == 'Испытать удачу':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Начать', callback_data='no')
        markup.add(button1)
        m = "Я расскажу вам про животных нашего края. А ваша задача - сказать, кто из них вам ближе."
        bot.send_message(message.chat.id, m, reply_markup=markup)

    if message.text == 'Вернуться к маршрутам':
        m = "Давайте продолжим наше путешествие. Выберите маршрут:"
        bot.send_message(message.chat.id, m, reply_markup=mar)

    if message.text == "Обратная связь":
        svaz = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="Оставить отзыв",
                                             url='https://forms.yandex.ru/u/66508675eb61467322b7cd86/')
        button2 = types.InlineKeyboardButton(text='Задать вопрос',
                                             url='https://forms.yandex.ru/u/665084e5eb614672f0b7cd66/')
        button3 = types.InlineKeyboardButton(text="Сообщить об ошибке",
                                             url='https://forms.yandex.ru/u/665084e5eb614672f0b7cd66/')
        button4 = types.InlineKeyboardButton(text='Отправить предложение',
                                             url='https://forms.yandex.ru/u/6650874feb6146733ab7cd8b/')
        button5 = types.InlineKeyboardButton(text='Назад', callback_data='men')
        svaz.add(button1, button2, button3, button4, button5)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id,
                         'Вы можете оставить отзыв, предложение, вопрос или сообщение об ошибке по формам ниже',
                         reply_markup=svaz)

    if message.text == 'В меню':
        bot.send_message(message.chat.id, 'Ваш выбор: ', reply_markup=menu)
        bot.delete_message(message.chat.id, message.message_id)


bot.infinity_polling()
