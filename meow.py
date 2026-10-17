import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

TOKEN = "token"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("weather"))
async def get_weather(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Please specify a city. Example: /weather poznan")
        return

    city = command.args

    async with aiohttp.ClientSession() as session:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        async with session.get(geo_url) as geo_resp:
            geo_data = await geo_resp.json()

            if not geo_data.get("results"):
                await message.answer(f"City {city} not found.")
                return

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        async with session.get(weather_url) as weather_resp:
            weather_data = await weather_resp.json()
            temp = weather_data["current_weather"]["temperature"]

            if temp < 10:
                feeling = "Cold"
            elif 10 <= temp < 25:
                feeling = "Warm"
            else:
                feeling = "Hot"

            await message.answer(
                f"City: {city_name} ({country})\n"
                f"Temperature: {temp}°C\n"
                f"Condition: {feeling}"
            )

async def main():
    print("Bot is ready!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
