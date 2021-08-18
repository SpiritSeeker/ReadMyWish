from ReadMyWish.API import GoogleBooksAPI

def _GetLargestThumbnail(item):
    try:
        urls = item['volumeInfo']['imageLinks'].keys()
        if len(urls) == 0:
            return None

        sizes = ['largeThumbnail', 'thumbnail', 'smallThumbnail']
        for size in sizes:
            if size in urls:
                return item['volumeInfo']['imageLinks'][size]
        return None
    except:
        return None

class SearchAPI():
    def __init__(self, api):
        self.api = api

    def Search(self, search_string):
        if self.api == 'GoogleBooks':
            ret = GoogleBooksAPI.BookSearch(search_string)

            resultDict = {}
            resultDict['title'] = ret['volumeInfo']['title']
            resultDict['link'] = ret['volumeInfo']['previewLink']
            if 'subtitle' in ret['volumeInfo'].keys():
                resultDict['subtitle'] = ret['volumeInfo']['subtitle']
            if 'pageCount' in ret['volumeInfo'].keys():
                resultDict['pageCount'] = ret['volumeInfo']['pageCount']
            if 'publishedDate' in ret['volumeInfo'].keys():
                resultDict['publishedDate'] = ret['volumeInfo']['publishedDate']
            if 'categories' in ret['volumeInfo'].keys():
                resultDict['genres'] = ret['volumeInfo']['categories']
            resultDict['authors'] = ret['volumeInfo']['authors']
            resultDict['synopsis'] = ret['volumeInfo']['description']
            thumbnailUrl = _GetLargestThumbnail(ret)
            if not thumbnailUrl == None:
                resultDict['imageLink'] = thumbnailUrl
            return resultDict
