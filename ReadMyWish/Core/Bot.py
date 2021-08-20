import discord
from ReadMyWish.API import SearchAPI
from ReadMyWish.Library import Library
from ReadMyWish.Utils.Functions import GetEmbed

class Bot():
    def __init__(self, api='GoogleBooks', commandPrefix='r!', libSavePath='lib.json'):
        self.api = SearchAPI.SearchAPI(api)
        self.commandPrefix = commandPrefix
        self.lib = Library.Library(libSavePath)

    async def MessageHandler(self, message):
        self.currentMessage = message
        if message.content.lower().startswith(("{{", self.commandPrefix + 'suggest')):
            stringEnd = message.content.find('}}')
            if stringEnd != -1:
                suggestString = message.content[2:stringEnd]
            else:
                suggestString = message.content.split(None, 1)[1]
            await self.BookSuggestion(suggestString)

        elif message.content.lower().startswith(self.commandPrefix):
            if message.content.lower().startswith(self.commandPrefix + 'help ') or message.content.lower() == (self.commandPrefix + 'help'):
                helpList = message.content.split(None)
                if len(helpList) == 1:
                    await self.HelpPage()
                else:
                    await self.HelpPage(helpList[1].lower())

            elif message.content.lower().startswith((self.commandPrefix + 'info ', self.commandPrefix + 'i ')):
                searchString = message.content.split(None, 1)[1]
                await self.BookInfo(searchString)

            elif message.content.lower().startswith((self.commandPrefix + 'search ', self.commandPrefix + 's ')):
                searchString = message.content.split(None, 1)[1]
                await self.BookSearch(searchString)

            elif (message.content.lower().startswith((self.commandPrefix + 'top ', self.commandPrefix + 't '))) or (message.content in {self.commandPrefix + 'top', self.commandPrefix + 't'}):
                contentList = message.content.split(None)
                if len(contentList) == 2:
                    await self.GetTopBooks(int(contentList[1]))
                else:
                    await self.GetTopBooks(10)

    async def BookSuggestion(self, suggestString):
        ret = self.api.Search(suggestString)

        self.lib.AddEntry(ret, self.currentMessage.author.name, self.currentMessage.author.id)
        book = self.lib.GetBook(ret)

        embed = GetEmbed(ret)
        footer = '\n\nThis book was suggested '
        if book.timesSuggested == 1:
            footer += '1 time.'
        else:
            footer += str(book.timesSuggested) + ' times.'
        embed.set_footer(text=footer)
        await self.currentMessage.reply(embed=embed)

    async def BookInfo(self, searchString):
        ret = self.api.Search(searchString)

        embed = GetEmbed(ret)
        await self.currentMessage.reply(embed=embed)

    async def BookSearch(self, searchString):
        await self.currentMessage.channel.send('Search feature not implemented yet. Consider contributing to see this and other cool features implemented in the near future!')

    async def GetTopBooks(self, num):
        sortedList = self.lib.GetBooksByTimesSuggested(num)
        print_string = 'Title - Times suggested\n\n'
        for book in sortedList:
            print_string += book.bookInfo['title'] + ' - ' + str(book.timesSuggested) + '\n'
        embed = discord.Embed()
        embed.description = print_string
        await self.currentMessage.channel.send(embed=embed)

    async def HelpPage(self, command='all'):
        if command == 'all':
            displayString = '`' + self.commandPrefix + 'help [optional command]`\nDisplays the help text\n\n'
            displayString += '`' + self.commandPrefix + 'info <name>`\nDisplays information of a book by name\n\n'
            displayString += '`' + self.commandPrefix + 'search <search_string>`\nSearches for books\n\n'
            displayString += '`' + self.commandPrefix + 'top [optional number]`\nDisplays most suggested books\n\n'
            displayString += '`' + self.commandPrefix + 'suggest <name>`\nAdds book to suggested list\n\n'
            displayString += 'Type `' + self.commandPrefix + 'help <command>` for more info on a command'
            embed = discord.Embed()
            embed.title = 'Commands:'
            embed.description = displayString
            await self.currentMessage.channel.send(embed=embed)

        elif command == 'help':
            embed = discord.Embed()
            embed.title = self.commandPrefix + 'help'
            embed.description = 'Displays the help text'
            embed.add_field(name='Usage:', value='`' + self.commandPrefix + 'help [command]`')
            await self.currentMessage.channel.send(embed=embed)

        elif command == 'info':
            embed = discord.Embed()
            embed.title = self.commandPrefix + 'info'
            embed.description = 'Searches and displays info of the most relevant book'
            embed.add_field(name='Usage:', value='`' + self.commandPrefix + '[info|i] <name>`')
            await self.currentMessage.channel.send(embed=embed)

        elif command == 'search':
            embed = discord.Embed()
            embed.title = self.commandPrefix + 'search'
            embed.description = 'Searches and displays the most relevant books'
            embed.add_field(name='Usage:', value='`' + self.commandPrefix + '[search|s] <search_string>`')
            await self.currentMessage.channel.send(embed=embed)

        elif command == 'top':
            embed = discord.Embed()
            embed.title = self.commandPrefix + 'top'
            embed.description = 'Displays the most suggested books'
            embed.add_field(name='Usage:', value='`' + self.commandPrefix + '[top|t] [number]`')
            await self.currentMessage.channel.send(embed=embed)

        elif command == 'suggest':
            embed = discord.Embed()
            embed.title = self.commandPrefix + 'suggest'
            embed.description = 'Adds book to the suggested list'
            embed.add_field(name='Usage:', value='`' + self.commandPrefix + 'suggest <name>`', inline=False)
            embed.add_field(name='Alternate usage:', value='`' + '{{name}}`', inline=False)
            await self.currentMessage.channel.send(embed=embed)
