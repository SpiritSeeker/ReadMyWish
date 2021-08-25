from ReadMyWish.API import GoogleBooksAPI
from ReadMyWish.Utils.APIHelpers import GoogleToDict

class SearchAPI():
    def __init__(self, api):
        self.api = api

    def GetBook(self, search_string):
        if self.api == 'GoogleBooks':
            itemList = GoogleBooksAPI.BookSearch(search_string)

            for item in itemList['items']:
                if ('description' in item['volumeInfo'].keys()) and (item['kind'] == 'books#volume'):
                    return GoogleToDict(item)

    def Search(self, search_string):
        if self.api == 'GoogleBooks':
            returnList = []
            itemList = GoogleBooksAPI.BookSearch(search_string)

            for item in itemList['items']:
                if ('description' in item['volumeInfo'].keys()) and (item['kind'] == 'books#volume'):
                    returnList.append(GoogleToDict(item))

            return returnList
