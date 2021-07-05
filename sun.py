from config import token, open_weather_token
import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.answer("/getwheather - узнать погоду.")


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}\n"
                        f"Я - тестовый бот на ядре aiogram. 🌎"
                        f"\nМой функционал будет со времнем пополняться."
                        f"\n/help - что бы узнать доступные действия.")


@dp.message_handler(commands=["getwheather"])
async def getwheather(message: types.Message):
    await message.answer(f"\nНапиши название города, что бы узнать погоду. 🌤")
@dp.message_handler()
async def getwheather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, я хз что это! 🤔"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - \
                            datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure}мм.рт.ст\n"
              f"Скорость ветра: {wind}М/С\nВосход солнца: {sunrise_timestamp}\n"
              f"Закат солнца: {sunset_timestamp}\nПродолжительность дня: {lenght_of_the_day}"
              f"\nХорошего дня! 😘")


    except:
        await message.reply("\U00002620 Проверьте название города.\U00002620", reply=False)





















def main():
    executor.start_polling(dispatcher=dp)

if __name__ == '__main__':
    executor.start_polling(dp)