import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
import telebot

# Токен вашего бота
TOKEN = "6505063153:AAEIwRLdqBrLP_BwfUiPTw7LkSORYTirXCs"

# Создание бота
bot = telebot.TeleBot(TOKEN)

# Объявление состояний для конечного автомата
START, AWAITING_BUS_NUMBER = range(2)

# Функция обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Чтобы создать билет, введите номер автобуса:")
    bot.register_next_step_handler(message, process_bus_number)

# Функция обработки номера автобуса
def process_bus_number(message):
    text = message.text
    image_path = create_ticket(text)
    if image_path:
        bot.send_photo(message.chat.id, open(image_path, 'rb'))
        # После отправки билета снова запрашиваем номер автобуса
        bot.send_message(message.chat.id, "Введите номер автобуса:")
        bot.register_next_step_handler(message, process_bus_number)
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так. Попробуйте еще раз.")

# Функция создания билета
def create_ticket(bus: str) -> str:
    # Открытие изображения
    image = Image.open("MAIN-PICTURE\\final_onay.jpg")
    font_path = "font/din-alternate-bold.ttf"

    # Создание объекта ImageDraw
    draw = ImageDraw.Draw(image)

    # Загрузка шрифта DIN Alternate Bold
    font = ImageFont.truetype(font_path, 36)  
    font2 = ImageFont.truetype("arial.ttf", 28)

    # Координаты, где будет находиться текст "103"
    x_text = 75
    y_text = 225

    # Координаты, где будет находиться время
    x_time = 215
    y_time = 310

    # Координаты, где будет находиться текущая дата
    x_date = 50
    y_date = 310

    # Получение текущего времени в часовом поясе Алматы (UTC+6)
    almaty_tz = pytz.timezone('Asia/Almaty')
    now = datetime.now(almaty_tz)

    # Форматирование времени в нужный вид
    time_str = now.strftime("%H %M")  # Добавляем двоеточие между часами и минутами

    # Форматирование текущей даты в нужный вид
    date_str = now.strftime("%d.%m.%Y")

    # Добавление текста номера автобуса на изображение
    draw.text((x_text, y_text), bus, fill=(0, 0, 0), font=font)  # Преобразуем номер автобуса в строку

    # Добавление времени на изображение
    draw.text((x_time, y_time), time_str, fill=(0, 0, 0), font=font)

    # Создание пути для сохранения изображения
    save_path = f"tickets/ticket_{bus}_{now.strftime('%Y%m%d_%H%M%S')}.png"

    # Добавление текущей даты на изображение
    draw.text((x_date, y_date), date_str, fill=(0, 0, 0), font=font)

    # Добавление двоеточия между часами и минутами времени
    #draw.text((x_time + 50, y_time), ":", fill=(0, 0, 0), font=font2)
    draw.text((249,314), ":", fill=(0,0,0),font=font2)
    # Сохранение изображения
    image.save(save_path)
    return save_path

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
