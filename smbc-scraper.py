"""
Web scraper for Sunday Morning Breakfast Cereal comics (smbc-comics.com) -- apienx

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from os import makedirs
from bs4 import BeautifulSoup, Tag
from urllib.request import urlopen
from urllib.parse import quote, urlsplit, urlunsplit
from requests import get as requests_get
from shutil import copyfileobj
from random import randrange
from time import sleep


DIRECTORY: str = 'comics'
EXTENSIONS: set = {'png', 'gif', 'jpg', 'jpeg',}
def parse_img(element: Tag, stem: str):
    url: str = element['src']
    print("Downloading image from", url)
    # SMBC uses different image formats
    ext: str = url.split('.')[-1]
    if ext not in EXTENSIONS:
        print("Not a recognized image format!")
        return

    # URL-encode the URL path to avoid issues with special characters,
    # including a space (ref. https://www.smbc-comics.com/comic/a-monster-2),
    # in image names. Encoding the whole thing would break scheme.
    url_split = urlsplit(url)
    url = urlunsplit(url_split._replace(
        path=quote(url_split.path)
        ))

    with urlopen(url) as response, \
         open(f'{stem}.{ext}', 'wb') as f:
            copyfileobj(response, f)


# Random user agent to calm down any anti-bot measures
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
def request(url):
    return requests_get(url, headers=headers)


print("""
Sunday Morning Breakfast Cereal Scraper (smbc-comics.com) V0.2
***
If you enjoy Zach Weinersmith's work, please consider supporting him on Patreon. https://www.patreon.com/ZachWeinersmith?ty
Alternatively, buy some SMBC merchandise: https://hivemill.com/collections/smbc
Pretty please with sugar on top. Patronage is what helps artists continue doing what they do best. Thank you!
***
Initializing...
""")


i: int
try:
    with open('history.txt', 'r') as f:
        i = int(f.readline())
        current_url = f.readline().strip()
except FileNotFoundError:
    print("No history file found. Starting from the beginning.")
    i = 1
    current_url = 'https://www.smbc-comics.com/comic/2002-09-05'


# While page exists, proceed
while True:
    print("Processing comic number", i)
    id: str = str(i).zfill(4)
    stem: str = f'{DIRECTORY}/{id}'
    makedirs(stem, exist_ok=True)

    # Request current page
    page = request(current_url)
    if page.status_code != 200:
        print(f"HTTP error encountered: {page.status_code}. Exiting...")
        break

    with open(f'{stem}/url.txt', 'w') as f:
        f.write(current_url)

    # Grab content of current page
    soup = BeautifulSoup(page.text, 'lxml')

    # Retrieving title text
    comic_image_element: Tag = soup.find(
        'div', {'id': 'cc-comicbody'}).img
    title: str = comic_image_element['title'].encode('ascii', 'ignore').decode()

    with open(f'{stem}/title.txt', 'w') as f:
        f.write(title)

    # Retrieve main comic image
    parse_img(comic_image_element, f'{stem}/comic')

    # Check for aftercomic (red button) image
    try:
        aftercomic_image_element: Tag = soup.find(
            'div', {'id': 'aftercomic'}).img
        parse_img(aftercomic_image_element, f'{stem}/aftercomic')
    except AttributeError:
        print("No aftercomic image found!")

    # Check for next comic URL
    next_element: Tag = soup.find(
        'a', {'class': 'cc-next'})
    if not next_element:
        print("No more comics found. Exiting...")
        break

    # Move on to next comic
    i += 1
    current_url = next_element['href']
    with open('history.txt', 'w') as f:
        f.write(f'{i}\n{current_url}')

    # Basic pseudo-random wait to avoid detection by the target server. Change the range of values to go faster
    print("Comic successfully scraped.")
    print("Waiting for ", delay := randrange(6, 60),
          "seconds between requests to throw off anti-bot mitigation measures...")
    sleep(delay)
