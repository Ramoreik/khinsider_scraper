#!/usr/bin/python3
import argparse
from libs.khinsider_scraper import KhinsiderScraper

# TODO:
# use something other than beautifulSoup, it looks like its too slow for this basic grep-like usage.

def print_banner():
    print("=-" * 10)
    print("KH1NS1D3R SCR4P3R")
    print("=-" * 10)

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='Search for an album')
    parser.add_argument('-d', '--download', help='Download')
    args = parser.parse_args()
    khinsider = KhinsiderScraper()

    if args.search:
        print("=" * 20)
        print("Searching for Albums with the keyword : {}".format(args.search))
        print("=" * 20)
        khinsider.search_albums(args.search)
    elif args.download and not args.search:
        album = args.download
        khinsider.download_album(album)
    else:
        print("Invalid parameters.")

    print("\nFinished ...")


    
