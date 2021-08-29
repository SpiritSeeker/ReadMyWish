import discord
from discord_components import DiscordComponents
from ReadMyWish.Core import Bot

TOKEN = open('token.secret', 'r').readline().strip()

intents = discord.Intents.default()
intents.messages = True

bot = Bot.Bot()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    DiscordComponents(client)
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        interaction = await client.wait_for('button_click')
        await bot.InteractionHandler(interaction)
        return

    await bot.MessageHandler(message)

client.run(TOKEN)
