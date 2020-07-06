import libs.bs4_filters as filters
from bs4 import BeautifulSoup
import concurrent.futures
import requests
from os import path, mkdir
from urllib.parse import unquote_plus

class KhinsiderScraper():
    DOWNLOAD_DIR = path.join(".","downloads")
    KHINSIDER_BASE_URL = "https://downloads.khinsider.com"
    KHINSIDER_OST_SECTION = "game-soundtracks/album"
    KHINSIDER_SEARCH_SECTION = "search?search="

    def __init__(self, album=""):
        self.album = album
        self.album_dir = path.join(self.DOWNLOAD_DIR, self.album)
        self.unique_songs = {}

    def search_albums(self, album):
        url = "{}/{}/{}".format(
            self.KHINSIDER_BASE_URL,
            self.KHINSIDER_OST_SECTION, album
        )
        r = requests.get(url)
        if "album" not in r.url:
            soup = BeautifulSoup(r.text, features="html5lib")
            links = soup.find_all(filters.has_game_soundtrack_in_name)
            for link in links:
                print(link['href'].split('/')[-1])
            print("=" * 20)
            print("\nUse the following to download: python3 main.py -d <album>")
        else:
            print(r.url.split('/')[-1])

    def download_album(self, album):
        self.album_dir = path.join(self.DOWNLOAD_DIR, album)
        url = "{}/{}/{}".format(
            self.KHINSIDER_BASE_URL,
            self.KHINSIDER_OST_SECTION, album
        )
        print("=" * 20)
        self.__find_unique_songs(url)
        print("=" * 20)
        self.__find_download_links()
        print("=" * 20)
        self.__directory_setup()
        self.__download_songs()

    def __find_unique_songs(self, url):
        print("Looking for songs ...")
        r = requests.get(url)
        if 'Ooops!' not in r.text and r.status_code == 200:
            soup = BeautifulSoup(r.text, features="html5lib")
            links = soup.find_all(filters.has_href_and_mp3)
            for link in links:
                self.__handle_song_link(link)
        elif 'Ooops!' in r.text:
            print("This album doesn't seem to exist")
            exit(1)
        else:
            print("Unknown error : {}".format(r.status_code))

    def __find_download_links(self):
        print("Finding download links.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.__find_download_link, self.unique_songs.keys())
    
    def __find_download_link(self, song):
        print("Finding link for : {}".format(song))
        r = requests.get(self.unique_songs[song])
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features="html5lib")
            links = soup.find_all(filters.has_href_and_mp3)
            for link in links:
                self.__handle_song_link(link)

    def __download_songs(self):
        print("Downloading found unique songs ...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.__download_song, self.unique_songs.keys())

    def __download_song(self, song):
        download_r = requests.get(self.unique_songs[song], allow_redirects=True)
        if download_r.status_code == 200:
                print("\nDownloading : {}".format(song))
                print("Using URL : {}".format(self.unique_songs[song]))
                open(path.join(self.album_dir, song), 'wb').write(download_r.content)
        else:
            print("There seems to have a problem with the download\
                link, status_code was: {}"\
                .format(download_r.status_code))

    def __directory_setup(self):
        if not path.exists(self.DOWNLOAD_DIR):
            print("Creating Download directory {} ...".format(self.DOWNLOAD_DIR))
            mkdir(self.DOWNLOAD_DIR)

        if not path.exists(self.album_dir):
            print("Creating Album Download directory {} ...".format(self.album_dir))
            mkdir(self.album_dir)

    def __handle_song_link(self, link):
        raw_url = link['href']
        if "http" not in raw_url:
            raw_url = "{}{}".format(self.KHINSIDER_BASE_URL, link['href'])
        clean_url = self.__double_unquote(raw_url)
        song_name = clean_url.split('/')[-1]
        self.unique_songs[song_name] = raw_url

    def __double_unquote(self, url):
        return unquote_plus(unquote_plus(url))
