import json
from urllib.request import urlopen

def BookSearch(title):
    search_api = "https://www.googleapis.com/books/v1/volumes?q="
    search_string = title.lower().replace(' ', '+')

    response = urlopen(search_api + search_string)
    item_list = json.load(response)

    for item in item_list['items']:
        if ('description' in item['volumeInfo'].keys()) and (item['kind'] == 'books#volume'):
            return item
