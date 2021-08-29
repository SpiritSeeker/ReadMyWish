import discord
from discord_components import Button, ButtonStyle
from ReadMyWish.API import SearchAPI
from ReadMyWish.Library import Library
from ReadMyWish.Utils.EmbedGenerator import *

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
        ret = self.api.GetBook(suggestString)

        self.lib.AddEntry(ret, self.currentMessage.author.name, self.currentMessage.author.id)
        book = self.lib.GetBook(ret)

        embed = GetBookInfoEmbed(ret)
        footer = 'This book was suggested '
        if book.timesSuggested == 1:
            footer += '1 time.'
        else:
            footer += str(book.timesSuggested) + ' times.'
        embed.set_footer(text=footer)
        await self.currentMessage.reply(embed=embed)

    async def BookInfo(self, searchString):
        ret = self.api.GetBook(searchString)

        embed = GetBookInfoEmbed(ret)
        await self.currentMessage.reply(embed=embed)

    async def BookSearch(self, searchString):
        self.searchResults = self.api.Search(searchString)
        self.searchString = searchString
        self.searchPage = 0
        self.titlesPerPage = 3

        embed = GetSearchEmbed(self.searchResults, self.searchString, self.searchPage, self.titlesPerPage)

        components = []
        if len(self.searchResults) > self.titlesPerPage:
            components.append(Button(label='Next', custom_id='searchNext'))
        self.sentMessage = await self.currentMessage.reply(embed=embed, components=components)

    async def GetTopBooks(self, num):
        sortedList = self.lib.GetBooksByTimesSuggested(num)
        print_string = 'Title - Times suggested\n\n'
        for book in sortedList:
            print_string += book.bookInfo['title'] + ' - ' + str(book.timesSuggested) + '\n'
        embed = discord.Embed()
        embed.description = print_string
        await self.currentMessage.channel.send(embed=embed)

    async def HelpPage(self, command='all'):
        embed = GetHelpEmbed(command, self.commandPrefix)

        if embed == None:
            await self.currentMessage.channel.send('Invalid command \'' + command + '\'.')
        else:
            await self.currentMessage.channel.send(embed=embed)

    async def InteractionHandler(self, interaction):
        if interaction.user == self.currentMessage.author:
            print('Button Clicked!', interaction.custom_id)
            if interaction.custom_id == 'searchNext':
                self.searchPage += 1

                embed = GetSearchEmbed(self.searchResults, self.searchString, self.searchPage, self.titlesPerPage)

                components = [[Button(label='Previous', custom_id='searchPrev')]]
                if len(self.searchResults) > self.titlesPerPage * (self.searchPage + 1):
                    components[0].append(Button(label='Next', custom_id='searchNext'))
                self.sentMessage = await self.currentMessage.reply(embed=embed, components=components)

            elif interaction.custom_id == 'searchPrev':
                self.searchPage -= 1

                embed = GetSearchEmbed(self.searchResults, self.searchString, self.searchPage, self.titlesPerPage)

                components = [[]]
                if self.searchPage > 0:
                    components[0].append(Button(label='Previous', custom_id='searchPrev'))
                components[0].append(Button(label='Next', custom_id='searchNext'))
                self.sentMessage = await self.currentMessage.reply(embed=embed, components=components)
