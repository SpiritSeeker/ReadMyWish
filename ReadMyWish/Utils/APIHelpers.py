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

def GoogleToDict(item):
    resultDict = {}
    resultDict['title'] = item['volumeInfo']['title']
    resultDict['link'] = item['volumeInfo']['previewLink']
    if 'subtitle' in item['volumeInfo'].keys():
        resultDict['subtitle'] = item['volumeInfo']['subtitle']
    if 'pageCount' in item['volumeInfo'].keys():
        resultDict['pageCount'] = item['volumeInfo']['pageCount']
    if 'publishedDate' in item['volumeInfo'].keys():
        resultDict['publishedDate'] = item['volumeInfo']['publishedDate']
    if 'categories' in item['volumeInfo'].keys():
        resultDict['genres'] = item['volumeInfo']['categories']
    resultDict['authors'] = item['volumeInfo']['authors']
    resultDict['synopsis'] = item['volumeInfo']['description']
    thumbnailUrl = _GetLargestThumbnail(item)
    if not thumbnailUrl == None:
        resultDict['imageLink'] = thumbnailUrl
    return resultDict
