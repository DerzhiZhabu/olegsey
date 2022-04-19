import telebot
bot = telebot.TeleBot('5162562935:AAHUjzT9k16Lo-xTqfKTpCIvC_4Af1WnnLw')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привет, это бот сайта https://olegsey.herokuapp.com/, он создан чтобы получить информацию о том, как пользоваться сайтом.\n"
                                               "Чтобы получить эту информацию напишите /help")
    elif message.text == '/help':
        bot.send_message(message.from_user.id,
                         'На главной странице вы можете видеть строку поиска, введите ваш запрос и вам выведут список имеющихся предложений с поддерживающихся площадок.')
        bot.send_message(message.from_user.id, 'Если вы зарегистрировались на сайте, то вы можете добавить товар в избранное, что позволит смотреть ваши товары в профиле в виде таблицы.'
                                               'Удалить товар из избранного можно так же в профиле.')


bot.polling(none_stop=True, interval=0)