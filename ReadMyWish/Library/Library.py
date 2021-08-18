from ReadMyWish.Library.Book import Book
import json
import time
import os.path

try: import operator
except: ImportError: keyfunc = lambda x: x.timesSuggested
else: keyfunc = operator.attrgetter("timesSuggested")

class Library():
    def __init__(self, filepath='lib.json'):
        self.books = {}
        self.filepath = filepath
        if os.path.isfile(self.filepath):
            self.LoadLibrary()

    def AddEntry(self, bookInfo, name, id):
        idString = bookInfo['title'] + ' - ' + bookInfo['authors'][0]
        idString = idString.lower()
        if not idString in self.books.keys():
            self.ForceAdd(idString, bookInfo)

        self.books[idString].SuggestedBy(name, id)
        self.SaveLibrary()

    def ForceAdd(self, idString, bookInfo):
        book = Book(bookInfo)
        self.books[idString] = book

    def AddBook(self, book):
        idString = book.title + ' - ' + book.authors[0]
        idString = idString.lower()
        if not idString in self.books.keys():
            self.books[idString] = book
            self.SaveLibrary()

    def GetBook(self, bookInfo):
        idString = bookInfo['title'] + ' - ' + bookInfo['authors'][0]
        idString = idString.lower()
        if idString in self.books.keys():
            return self.books[idString]

    def SaveLibrary(self):
        libDict = {}
        libDict['totalBooks'] = len(self.books)
        booksList = []
        for id in self.books:
            booksDict = {}
            booksDict['idString'] = id
            booksDict['bookInfo'] = self.books[id].bookInfo
            booksDict['suggestedBy'] = self.books[id].suggestNames
            booksDict['timesSuggested'] = self.books[id].timesSuggested
            booksList.append(booksDict)
        libDict['books'] = booksList
        self.lastSave = time.time()
        libDict['saveTime'] = self.lastSave

        with open(self.filepath, 'w') as fp:
            json.dump(libDict, fp, indent=2)

    def LoadLibrary(self):
        fp = open(self.filepath, 'r')
        libDict = json.load(fp)

        for bookDict in libDict['books']:
            if bookDict['idString'] not in self.books.keys():
                book = Book(bookDict['bookInfo'])

                book.suggestNames = bookDict['suggestedBy']
                book.timesSuggested = bookDict['timesSuggested']

                self.books[bookDict['idString']] = book

        fp.close()
        return libDict['saveTime']

    def GetBooksByTimesSuggested(self, num=10):
        sortedList = sorted(list(self.books.values()), key=keyfunc, reverse=True)
        if len(sortedList) > num:
            return sortedList[:num]
        return sortedList
