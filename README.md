# smbc-scraper
Scrape [Saturday Morning Breakfast Cereal comics](https://www.smbc-comics.com/) (cartoons, aftercomics, title text, URL). Scraper uses the Beautiful Soup 4 library.

To run, install [Python 3.x](https://www.python.org/downloads/) and [bs4](https://pypi.org/project/beautifulsoup4/). Then hit: `python3 smbc-scraper.py`

A new directory is created for each page where the cartoons and aftercomics are stored in the original format, and the URLs and titles are stored in text files. Everything is stored in the `comics` directory created where the script is invoked.

As of this writing, the server doesn't block automated requests. If you get blocked, try increasing the random delay range in line 135. Else, you'll need to resort to some IP rotation.
