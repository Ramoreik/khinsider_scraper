from urllib.parse import unquote_plus
from bs4 import BeautifulSoup
from os import path, mkdir
import argparse
import platform
import requests
import sys

# Script to download a precise set of OST from khinsider.com
# arg1 = name of the game found on khinsider.com exemple: pokemon-platinum

# TODO:
# use something other than beautifulSoup, it looks like its too slow for this basic grep-like usage.
# use threading to make getting links faster.

DOWNLOAD_DIR = path.join(".","downloads")
KHINSIDER_BASE_URL = "https://downloads.khinsider.com"
KHINSIDER_OST_SECTION = "game-soundtracks/album"
KHINSIDER_SEARCH_SECTION = "search?search="
UNIQUE_SONGS = {}

def has_href_and_mp3(tag):
    is_valid = False
    if tag.name == "a" and\
            tag.get('href', None) and\
            '.mp3' in tag['href']:
        is_valid = True
        handle_song_link(tag)
    return is_valid

def has_game_soundtrack_in_name(tag):
    is_valid = False
    if tag.name == "a" and tag.get('href', None) and 'game-soundtracks/album' in tag['href'] and '.mp3' not in tag['href']:
        is_valid = True
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

def search_albums(album):
    r = requests.get("{}/{}{}".format(KHINSIDER_BASE_URL, KHINSIDER_SEARCH_SECTION, album))
    if "album" not in r.url:
        soup = BeautifulSoup(r.text, features="html5lib")
        links = soup.find_all(has_game_soundtrack_in_name)
        for link in links:
            print(link['href'].split('/')[-1])
        print("=" * 20)
        print("\nUse the following to download: python3 main.py -d <album>")
    else:
        print(r.url.split('/')[-1])

def find_unique_songs(url):
    global UNIQUE_SONGS
    print("Looking for songs ...")
    r = requests.get(url)
    if 'Ooops!' not in r.text and r.status_code == 200:
        soup = BeautifulSoup(r.text, features="html5lib")
        links = soup.find_all(has_href_and_mp3)
    elif 'Ooops!' in r.text:
        print("This album doesn't seem to exist")
        exit(1)
    else:
        print("Unknown error : {}".format(r.status_code))

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
            print("\nDownloading : {}".format(song))
            print("Using URL : {}".format(UNIQUE_SONGS[song]))
            open(path.join(album_dir, song), 'wb').write(download_r.content)
        else:
            print("There seems to have a problem with the download link, status_code was: {}"\
                .format(download_r.status_code))

def print_banner():
    print("=-" * 10)
    print("KH1NS1D3R SCR4P3R")
    print("=-" * 10)

def directory_setup(album_dir):
    if not path.exists(DOWNLOAD_DIR):
        print("Creating Download directory {} ...".format(DOWNLOAD_DIR))
        mkdir(DOWNLOAD_DIR)

    if not path.exists(album_dir):
        print("Creating Album Download directory {} ...".format(album_dir))
        mkdir(album_dir)

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='Search for an album')
    parser.add_argument('-d', '--download', help='Download')
    args = parser.parse_args()

    if args.search:
        print("=" * 20)
        print("Searching for Albums with the keyword : {}".format(args.search))
        print("=" * 20)
        search_albums(args.search)
    elif args.download and not args.search:
        album = args.download
        album_dir = path.join(DOWNLOAD_DIR, album)
        url = "{}/{}/{}".format(KHINSIDER_BASE_URL, KHINSIDER_OST_SECTION, album)

        print("=" * 20)
        find_unique_songs(url)


        print("=" * 20)
        find_download_link()

        print("=" * 20)
        directory_setup(album_dir)
        download_songs(album_dir)

    else:
        print("Invalid parameters.")

    print("\nFinished ...")


    
