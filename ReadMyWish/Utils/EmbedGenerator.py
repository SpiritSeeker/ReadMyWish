import discord

def GetBookInfoEmbed(item):
    embed = discord.Embed()
    embed.title = item['title']
    embed.url = item['link']

    description_string = 'by '
    authors = item['authors']
    description_string += authors[0]
    if len(authors) > 1:
        for i in range(len(authors) - 1):
            description_string += ', ' + authors[i+1]
    if 'pageCount' in item.keys():
        description_string += ' | ' + str(item['pageCount']) + ' pages'
    if 'publishedDate' in item.keys():
        description_string += ' | Published: ' + str(item['publishedDate'])
    if 'genres' in item.keys():
        string_segment = ' | Genre: '
        for i in range(len(item['genres'])):
            if i == 0:
                string_segment += item['genres'][i]
            else:
                string_segment += ', ' + item['genres'][i]
        description_string += string_segment

    description_string += '\n\n> {}'.format(item['synopsis'])
    embed.description = description_string

    if 'imageLink' in item.keys():
        embed.set_image(url=item['imageLink'])

    return embed

def GetSearchEmbed(item, searchString):
    embed = discord.Embed()
    embed.title = 'Displaying search results for \'' + searchString + '\''

    if len(item) < 10:
        numTitles = len(item)
    else:
        numTitles = 10

    displayString = ''

    for i in range(numTitles):
        book = item[i]
        displayString += '**' + str(i+1) + '. '
        displayString += '[' + book['title'] + '](' + book['link'] + ')**\n'
        description_string = 'by '
        authors = book['authors']
        description_string += authors[0]
        if len(authors) > 1:
            for i in range(len(authors) - 1):
                description_string += ', ' + authors[i+1]
        if 'pageCount' in book.keys():
            description_string += ' | ' + str(book['pageCount']) + ' pages'
        if 'publishedDate' in book.keys():
            description_string += ' | Published: ' + str(book['publishedDate'])
        if 'genres' in book.keys():
            string_segment = ' | Genre: '
            for i in range(len(book['genres'])):
                if i == 0:
                    string_segment += book['genres'][i]
                else:
                    string_segment += ', ' + book['genres'][i]
            description_string += string_segment
        description_string += '\n\n'
        displayString += description_string

    embed.description = displayString
    return embed

def GetHelpEmbed(command, commandPrefix):
    if command == 'all':
        displayString = '`' + commandPrefix + 'help [optional command]`\nDisplays the help text\n\n'
        displayString += '`' + commandPrefix + 'info <name>`\nDisplays information of a book by name\n\n'
        displayString += '`' + commandPrefix + 'search <search_string>`\nSearches for books\n\n'
        displayString += '`' + commandPrefix + 'top [optional number]`\nDisplays most suggested books\n\n'
        displayString += '`' + commandPrefix + 'suggest <name>`\nAdds book to suggested list\n\n'
        displayString += 'Type `' + commandPrefix + 'help <command>` for more info on a command'
        embed = discord.Embed()
        embed.title = 'Commands:'
        embed.description = displayString
        return embed

    if command == 'help':
        embed = discord.Embed()
        embed.title = commandPrefix + 'help'
        embed.description = 'Displays the help text'
        embed.add_field(name='Usage:', value='`' + commandPrefix + 'help [command]`')
        return embed

    if command == 'info':
        embed = discord.Embed()
        embed.title = commandPrefix + 'info'
        embed.description = 'Searches and displays info of the most relevant book'
        embed.add_field(name='Usage:', value='`' + commandPrefix + '[info|i] <name>`')
        return embed

    if command == 'search':
        embed = discord.Embed()
        embed.title = commandPrefix + 'search'
        embed.description = 'Searches and displays the most relevant books'
        embed.add_field(name='Usage:', value='`' + commandPrefix + '[search|s] <search_string>`')
        return embed

    if command == 'top':
        embed = discord.Embed()
        embed.title = commandPrefix + 'top'
        embed.description = 'Displays the most suggested books'
        embed.add_field(name='Usage:', value='`' + commandPrefix + '[top|t] [number]`')
        return embed

    if command == 'suggest':
        embed = discord.Embed()
        embed.title = commandPrefix + 'suggest'
        embed.description = 'Adds book to the suggested list'
        embed.add_field(name='Usage:', value='`' + commandPrefix + 'suggest <name>`', inline=False)
        embed.add_field(name='Alternate usage:', value='`' + '{{name}}`', inline=False)
        return embed

    return None
