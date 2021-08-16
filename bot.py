import discord
from GoogleBooksAPI import BookSearch
from Library import Library
from Book import Book

TOKEN = open('token.secret', 'r').readline().strip()

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

lib = Library()

def GetString(item):
    return_str = ''
    return_str += '[' + item['volumeInfo']['title'] + ']('
    return_str += item['volumeInfo']['previewLink'] + ')'
    if 'subtitle' in item['volumeInfo'].keys():
        return_str += ' - ' + item['volumeInfo']['subtitle']
    return_str += '\n'
    return_str += 'by '
    authors = item['volumeInfo']['authors']
    return_str += authors[0]
    if len(authors) > 1:
        for i in range(len(authors) - 1):
            return_str += ', ' + authors[i+1]
    try:
        return_str += ' | ' + str(item['volumeInfo']['pageCount']) + ' pages'
    except:
        pass
    try:
        return_str += ' | Published: ' + str(item['volumeInfo']['publishedDate'])
    except:
        pass
    try:
        string_segment = ' | Genre: '
        for i in range(len(item['volumeInfo']['categories'])):
            if i == 0:
                string_segment += item['volumeInfo']['categories'][i]
            else:
                string_segment += ', ' + item['volumeInfo']['categories'][i]
        return_str += string_segment
    except:
        pass
    return_str += '\n\n' + '> {}'.format(item['volumeInfo']['description'])
    return return_str

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('rmw!'):
        await CommandHandler(message)

    if message.content.startswith('{{'):
        search_str = message.content[2:].rpartition('}}')[0]
        ret = BookSearch(search_str)

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
    if message.content.startswith('rmw!search'):
        ret = BookSearch(message.content.replace('rmw!search ', ''))
        print_string = GetString(ret)
        embed = discord.Embed()
        embed.description = print_string
        await message.reply(embed=embed)

client.run(TOKEN)
