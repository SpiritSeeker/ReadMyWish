import json
from urllib.request import urlopen

def BookSearch(title):
    search_api = "https://www.googleapis.com/books/v1/volumes?q="
    search_string = title.lower().replace(' ', '+')

    response = urlopen(search_api + search_string)
    item_list = json.load(response)

    return item_list
