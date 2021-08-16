class Book():
    def __init__(self, bookInfo=None):
        if not bookInfo == None:
            self.title = bookInfo['volumeInfo']['title']
            self.link = bookInfo['volumeInfo']['previewLink']
            if 'subtitle' in bookInfo['volumeInfo'].keys():
                self.subtitle = bookInfo['volumeInfo']['subtitle']
            else:
                self.subtitle = ''
            self.authors = bookInfo['volumeInfo']['authors']
            self.description = bookInfo['volumeInfo']['description']

        self.suggestNames = {}
        self.timesSuggested = 0

    def SuggestedBy(self, name, id):
        if not id in self.suggestNames.keys():
            self.suggestNames[id] = name
        self.timesSuggested += 1
