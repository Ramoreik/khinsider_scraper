#These are custom beautifulSoup filtersd
def has_href_and_mp3(tag):
    is_valid = False
    if tag.name == "a" and\
            tag.get('href', None) and\
            '.mp3' in tag['href']:
        is_valid = True
    return is_valid

def has_game_soundtrack_in_name(tag):
    is_valid = False
    if tag.name == "a" and tag.get('href', None) \
            and 'game-soundtracks/album' in tag['href'] \
            and '.mp3' not in tag['href']:
        is_valid = True
    return is_valid

