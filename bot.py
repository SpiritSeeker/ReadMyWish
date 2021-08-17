import discord
from ReadMyWish.API import GoogleBooksAPI
from ReadMyWish.Library import Library, Book
from ReadMyWish.Utils.Functions import GetEmbed

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

        embed = GetEmbed(ret)
        footer = '\n\nThis book was suggested '
        if book.timesSuggested == 1:
            footer += '1 time.'
        else:
            footer += str(book.timesSuggested) + ' times.'
        embed.set_footer(text=footer)
        await message.reply(embed=embed)

async def CommandHandler(message):
    if message.content.startswith(commandPrefix + 'search '):
        ret = GoogleBooksAPI.BookSearch(message.content.replace(commandPrefix + 'search ', ''))
        embed = GetEmbed(ret)
        await message.reply(embed=embed)
    if message.content.startswith(commandPrefix + 's '):
        ret = GoogleBooksAPI.BookSearch(message.content.replace(commandPrefix + 's ', ''))
        embed = GetEmbed(ret)
        await message.reply(embed=embed)
    if (message.content.startswith(commandPrefix + 'info ')) or (message.content.startswith(commandPrefix + 'i ')):
        num = int(message.content.split(' ')[1])
        sortedList = lib.GetBooksByTimesSuggested(num)
        print_string = 'Title - Times suggested\n\n'
        for book in sortedList:
            print_string += book.title + ' - ' + str(book.timesSuggested) + '\n'
        embed = discord.Embed()
        embed.description = print_string
        await message.channel.send(embed=embed)
    if (message.content == commandPrefix + 'info') or (message.content == commandPrefix + 'i'):
        sortedList = lib.GetBooksByTimesSuggested()
        print_string = 'Title - Times suggested\n\n'
        for book in sortedList:
            print_string += book.title + ' - ' + str(book.timesSuggested) + '\n'
        embed = discord.Embed()
        embed.description = print_string
        await message.channel.send(embed=embed)

client.run(TOKEN)
