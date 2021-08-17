def GetString(item):
    return_str = ''
    return_str += '[' + item['volumeInfo']['title'] + ']('
    return_str += item['volumeInfo']['previewLink'] + ')'
    if 'subtitle' in item['volumeInfo'].keys():
        return_str += ' - ' + item['volumeInfo']['subtitle']
    return_str += '\n'
    return_str += 'by '
    authors = item['volumeInfo']['authors']
    return_str += authors[0]
    if len(authors) > 1:
        for i in range(len(authors) - 1):
            return_str += ', ' + authors[i+1]
    try:
        return_str += ' | ' + str(item['volumeInfo']['pageCount']) + ' pages'
    except:
        pass
    try:
        return_str += ' | Published: ' + str(item['volumeInfo']['publishedDate'])
    except:
        pass
    try:
        string_segment = ' | Genre: '
        for i in range(len(item['volumeInfo']['categories'])):
            if i == 0:
                string_segment += item['volumeInfo']['categories'][i]
            else:
                string_segment += ', ' + item['volumeInfo']['categories'][i]
        return_str += string_segment
    except:
        pass
    return_str += '\n\n' + '> {}'.format(item['volumeInfo']['description'])
    return return_str
