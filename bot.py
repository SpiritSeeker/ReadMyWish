import discord
from ReadMyWish.Core import Bot

TOKEN = open('token.secret', 'r').readline().strip()

intents = discord.Intents.default()
intents.messages = True

bot = Bot.Bot()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await bot.MessageHandler(message)

client.run(TOKEN)
