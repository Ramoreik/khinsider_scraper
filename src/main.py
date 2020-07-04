from bs4 import BeautifulSoup
from urllib.parse import unquote_plus
import requests
import sys
import os
# Script to download a precise set of OST from khinsider.com
# arg1 = name of the game found on khinsider.com exemple: pokemon-platinum
KHINSIDER_BASE_URL = "https://downloads.khinsider.com"
KHINSIDER_OST_SECTION = "game-soundtracks/album"
UNIQUE_SONGS = {}

def has_href_and_mp3(tag):
    is_valid = False
    if tag.get('href', None) and '.mp3' in tag['href'] and tag['href'] not in UNIQUE_SONGS:
        is_valid = True
    return is_valid


def find_unique_songs(url):
    global UNIQUE_SONGS
    print("Looking for songs ...")
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features="html5lib")
        links = soup.find_all(has_href_and_mp3)
        for link in links:
            clean_url = unquote_plus(unquote_plus("{}{}".format(KHINSIDER_BASE_URL, link['href'])))
            song_name = clean_url.split('/')[-1]
            UNIQUE_SONGS[song_name] = "{}{}".format(KHINSIDER_BASE_URL, link['href'])

def find_download_link():
    global UNIQUE_SONGS
    print("Finding download links.")
    for song in UNIQUE_SONGS.keys():
        print("Finding link for : {}".format(song))
        r = requests.get(UNIQUE_SONGS[song])
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features="html5lib")
            download_links = soup.find_all(has_href_and_mp3)
            for download_link in download_links:
                UNIQUE_SONGS[song] = download_link['href']
                print("Download link: {}\n".format(download_link['href']))

def download_songs():
    print("Downloading found unique songs ...")
    for song in UNIQUE_SONGS.keys():
        download_r = requests.get(UNIQUE_SONGS[song], allow_redirects=True)
        if download_r.status_code == 200:
            print("Downloading : {}".format(song))
            open('downloads/{}'.format(song), 'wb').write(download_r.content)
        else:
            print("There seems to have a problem with the download link ...")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        album = sys.argv[1]
        url = "{}/{}/{}".format(KHINSIDER_BASE_URL, KHINSIDER_OST_SECTION, album)
        print("URL : {}".format(url))
        find_unique_songs(url)
        find_download_link()
        download_songs()
    else:
        print("Incorrect number of arguments.")

    