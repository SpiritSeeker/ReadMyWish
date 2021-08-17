import discord
from ReadMyWish.API import GoogleBooksAPI
from ReadMyWish.Library import Library, Book
from ReadMyWish.Utils.Functions import GetString

TOKEN = open('token.secret', 'r').readline().strip()

intents = discord.Intents.default()
intents.messages = True

commandPrefix = 'r!'

client = discord.Client(intents=intents)

lib = Library.Library()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(commandPrefix):
        await CommandHandler(message)

    if message.content.startswith('{{'):
        search_str = message.content[2:].rpartition('}}')[0]
        ret = GoogleBooksAPI.BookSearch(search_str)

        lib.AddEntry(ret, message.author.name, message.author.id)
        book = lib.GetBook(ret)

        print_string = GetString(ret)
        print_string += '\n\nThis book was suggested '
        if book.timesSuggested == 1:
            print_string += '1 time.'
        else:
            print_string += str(book.timesSuggested) + ' times.'
        embed = discord.Embed()
        embed.description = print_string
        await message.reply(embed=embed)

async def CommandHandler(message):
    if message.content.startswith(commandPrefix + 'search'):
        ret = GoogleBooksAPI.BookSearch(message.content.replace(commandPrefix + 'search ', ''))
        print_string = GetString(ret)
        embed = discord.Embed()
        embed.description = print_string
        await message.reply(embed=embed)
    if message.content.startswith(commandPrefix + 's'):
        ret = GoogleBooksAPI.BookSearch(message.content.replace(commandPrefix + 's ', ''))
        print_string = GetString(ret)
        embed = discord.Embed()
        embed.description = print_string
        await message.reply(embed=embed)

client.run(TOKEN)
