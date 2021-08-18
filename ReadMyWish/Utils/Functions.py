import discord

def GetEmbed(item):
    embed = discord.Embed()
    embed.title = item['title']
    embed.url = item['link']

    description_string = 'by '
    authors = item['authors']
    description_string += authors[0]
    if len(authors) > 1:
        for i in range(len(authors) - 1):
            description_string += ', ' + authors[i+1]
    if 'pageCount' in item.keys():
        description_string += ' | ' + str(item['pageCount']) + ' pages'
    if 'publishedDate' in item.keys():
        description_string += ' | Published: ' + str(item['publishedDate'])
    if 'genres' in item.keys():
        string_segment = ' | Genre: '
        for i in range(len(item['genres'])):
            if i == 0:
                string_segment += item['genres'][i]
            else:
                string_segment += ', ' + item['genres'][i]
        description_string += string_segment

    description_string += '\n\n> {}'.format(item['synopsis'])
    embed.description = description_string

    if 'imageLink' in item.keys():
        embed.set_image(url=item['imageLink'])

    return embed
