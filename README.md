# smbc-scraper
Scrape [Saturday Morning Breakfast Cereal comics](https://www.smbc-comics.com/) (cartoons + title text). Scraper uses the Beautiful Soup 4 library.

To run, install [Python 3.x](https://www.python.org/downloads/) and [bs4](https://pypi.org/project/beautifulsoup4/). Then hit: `python3 smbc-scraper.py`

A new directory is created for each page where the cartoons are stored in the original format (PNG for the more recent comics and GIF for older ones) and the titles are stored in a text file. Everything is stored in the current directory from which the script is invoked.

As of this writing, the server doesn't block automated requests. If you get blocked, try increasing the random delay range in line 91. Else, you'll need to resort to some IP rotation.
