import discord

def GetLargestThumbnail(item):
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

def GetEmbed(item):
    embed = discord.Embed()
    embed.title = item['volumeInfo']['title']
    embed.url = item['volumeInfo']['previewLink']

    description_string = 'by '
    authors = item['volumeInfo']['authors']
    description_string += authors[0]
    if len(authors) > 1:
        for i in range(len(authors) - 1):
            description_string += ', ' + authors[i+1]
    try:
        description_string += ' | ' + str(item['volumeInfo']['pageCount']) + ' pages'
    except:
        pass
    try:
        description_string += ' | Published: ' + str(item['volumeInfo']['publishedDate'])
    except:
        pass
    try:
        string_segment = ' | Genre: '
        for i in range(len(item['volumeInfo']['categories'])):
            if i == 0:
                string_segment += item['volumeInfo']['categories'][i]
            else:
                string_segment += ', ' + item['volumeInfo']['categories'][i]
        description_string += string_segment
    except:
        pass

    description_string += '\n\n> {}'.format(item['volumeInfo']['description'])
    embed.description = description_string

    thumbnailUrl = GetLargestThumbnail(item)
    if not thumbnailUrl == None:
        embed.set_thumbnail(url=thumbnailUrl)

    return embed
