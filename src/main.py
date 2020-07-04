from bs4 import BeautifulSoup
from urllib.parse import unquote_plus
from os import path, mkdir
import platform
import requests
import sys

# Script to download a precise set of OST from khinsider.com
# arg1 = name of the game found on khinsider.com exemple: pokemon-platinum
DOWNLOAD_DIR = path.join(".","downloads")
KHINSIDER_BASE_URL = "https://downloads.khinsider.com"
KHINSIDER_OST_SECTION = "game-soundtracks/album"
UNIQUE_SONGS = {}

def has_href_and_mp3(tag):
    is_valid = False
    if tag.name == "a" and\
            tag.get('href', None) and\
            '.mp3' in tag['href']:
        is_valid = True
        handle_song_link(tag)
    return is_valid

def handle_song_link(link):
    raw_url = link['href']
    if "http" not in raw_url:
        raw_url = "{}{}".format(KHINSIDER_BASE_URL, link['href'])
    clean_url = double_unquote(raw_url)
    song_name = clean_url.split('/')[-1]
    UNIQUE_SONGS[song_name] = raw_url

def double_unquote(url):
    return unquote_plus(unquote_plus(url))

def find_unique_songs(url):
    global UNIQUE_SONGS
    print("Looking for songs ...")
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features="html5lib")
        links = soup.find_all(has_href_and_mp3)

def find_download_link():
    global UNIQUE_SONGS
    print("Finding download links.")
    for song in UNIQUE_SONGS.keys():
        print("Finding link for : {}".format(song))
        r = requests.get(UNIQUE_SONGS[song])
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features="html5lib")
            download_links = soup.find_all(has_href_and_mp3)

def download_songs(album_dir):
    print("Downloading found unique songs ...")
    for song in UNIQUE_SONGS.keys():
        download_r = requests.get(UNIQUE_SONGS[song], allow_redirects=True)
        if download_r.status_code == 200:
            print("Downloading : {}".format(song))
            print("Using URL : {}".format(UNIQUE_SONGS[song]))
            open(path.join(album_dir, song), 'wb').write(download_r.content)
        else:
            print("There seems to have a problem with the download link, status_code was: {}"\
                .format(download_r.status_code))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("=-" * 10)
        print("KH1NS1D3R SCR4P3R")
        print("=-" * 10)
        album = sys.argv[1]
        album_dir = path.join(DOWNLOAD_DIR, album)
        if not path.exists(DOWNLOAD_DIR):
            print("Creating Download directory {} ...".format(DOWNLOAD_DIR))
            mkdir(DOWNLOAD_DIR)
        if not path.exists(album_dir):
            print("Creating Album Download directory {} ...".format(album_dir))
            mkdir(album_dir)

        url = "{}/{}/{}".format(KHINSIDER_BASE_URL, KHINSIDER_OST_SECTION, album)
        print("=" * 20)
        find_unique_songs(url)

        print("=" * 20)
        find_download_link()

        print("=" * 20)
        download_songs(album_dir)
        print("\nFinished ...")
    else:
        print("Incorrect number of arguments.")

    