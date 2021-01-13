# Khinsider Scraper
This script is a very simple and barebones khinsider scraper to download video game OST.  
There are two different options you can launch this script with:  
  
  -s : searches using the string provided and returns a list of albums , if the string contains whitespace it should be quoted.
  -d : download the provided album.

**There is no cap on threads for now, so it can be ressource hungry.*  *

- If you want to extend this feel free to fork it and go crazy.  
- If you want a binary to execute directly you can compile this project with PyInstaller.  

### Installation
```bash
git clone git@github.com:Ramoreik/khinsider_scraper.git
cd khinsider_scraper
pip3 install -r requirements.txt
```

### Usage
```bash
# Example of search:
python main.py -s "zelda majora"
=-=-=-=-=-=-=-=-=-=-
KH1NS1D3R SCR4P3R
=-=-=-=-=-=-=-=-=-=-
====================
Searching for Albums with the keyword : zelda majora
====================
legend-of-zelda-the-majora-s-mask-2000-n64-gamerip
legend-of-zelda-the-majora-s-mask-the-complete-soundtrack-collection
legend-of-zelda-the-majora-s-mask-3d-2015-3ds-gamerip
legend-of-zelda-the-majora-s-mask-3d-original-soundtrack
legend-of-zelda-the-majora-s-mask-3d-original-sound-track
zelda-reorchestrated-06-majora-s-mask
mario-zelda-big-band-live-cd
====================

Use the following to download: python3 main.py -d <album>

Finished ...

# Once you know which album you want you can download it:
python main.py -d legend-of-zelda-the-majora-s-mask-2000-n64-gamerip
# Can take only a few seconds even for large albums if your internet connection is good.
```

Enjoy the nostalgic songs of your childhood!