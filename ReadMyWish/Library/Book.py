from copy import deepcopy

class Book():
    def __init__(self, bookInfo=None):
        if not bookInfo == None:
            self.bookInfo = deepcopy(bookInfo)

        self.suggestNames = {}
        self.timesSuggested = 0

    def SuggestedBy(self, name, id):
        if not id in self.suggestNames.keys():
            self.suggestNames[id] = name
        self.timesSuggested += 1
