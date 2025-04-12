import discord
import random
import requests
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio

# Настройки бота
TOKEN = "***"
intents = discord.Intents.default()
intents.guilds = True  # Нужно для работы с серверами
intents.message_content = True  # Для получения текста сообщений
intents.messages = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Автоответы
AUTO_RESPONSES = {
    "америка": "СВОБОДА! 🇺🇸",
    "свобода": "Да здравствует свобода! 🦅",
    "дядя сэм": "I WANT YOU for the U.S. Army! 🎖️"
}


@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    for key, response in AUTO_RESPONSES.items():
        if key in msg:
            await message.channel.send(response)
            break

    await bot.process_commands(message)


# Викторина
QUIZ_QUESTIONS = [
    {"question": "Сколько штатов в США?", "answer": "50"},
    {"question": "Какой цвет у Белого дома?", "answer": "белый"},
    {"question": "Кто изображён на 1-долларовой купюре?", "answer": "вашингтон"}
]


@bot.command()
async def quiz(ctx):
    question = random.choice(QUIZ_QUESTIONS)
    await ctx.send(f'Вопрос: {question["question"]}')

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=15.0, check=check)
        if msg.content.lower() == question["answer"].lower():
            await ctx.send("Правильно! 🎉")
        else:
            await ctx.send(f'Неправильно! Ответ: {question["answer"]}')
    except:
        await ctx.send("Время вышло! ⏳")


# Мемы
@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme")
    if response.status_code == 200:
        meme_url = response.json()["url"]
        await ctx.send(meme_url)
    else:
        await ctx.send("Не удалось получить мем 😢")


# Цитаты демократов
DEMOCRATIC_QUOTES = [
    "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
    "Ask not what your country can do for you – ask what you can do for your country. - John F. Kennedy",
    "We can’t help everyone, but everyone can help someone. - Ronald Reagan",
    "Change is never easy, but always possible. - Barack Obama",
    "We are the change that we seek. - Barack Obama"
]


@bot.command()
async def democracy(ctx):
    quote = random.choice(DEMOCRATIC_QUOTES)
    await ctx.send(quote)


@bot.command()
async def anthem(ctx):
    if not ctx.author.voice:
        await ctx.send("Вы должны быть в голосовом канале!")
        return

    channel = ctx.author.voice.channel
    print(f"Подключаюсь к каналу: {channel.name}")  # Для отладки
    voice_client = await channel.connect()

    print("Подключен!")  # Для отладки

    source = FFmpegPCMAudio("anthem.mp3")
    voice_client.play(source)

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()
    print("Отключен!")  # Для отладки


bot.run(TOKEN)
