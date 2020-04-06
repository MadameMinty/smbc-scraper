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

import os
from bs4 import BeautifulSoup
import urllib
import requests
import shutil
import random
import time

print("Sunday Morning Breakfast Cereal Scraper (smbc-comics.com) V0.1")
print("***")
print("If you enjoy Zach Weinersmith's work, please consider supporting him on Patreon. https://www.patreon.com/ZachWeinersmith?ty=h
print("Alternatively, buy some SMBC merchandise: https://hivemill.com/collections/smbc")
print("Pretty please with sugar on top. Patronage is what helps artists continue doing what they do best. Thank you!")
print("***")
print("Initializing...")

# Hard-coding the initial URL
first_url = 'https://www.smbc-comics.com/comic/2002-09-05'
current_url = first_url
next_url = first_url
page_request = requests.get( first_url )
parent_directory = os.getcwd()
i = 1

# While page exists, proceed
while( page_request.status_code != 404 ):

	if next_url == 'https://www.smbc-comics.com/comic/2002-09-05':
		current_page = requests.get( first_url )
	else:
		current_page = requests.get( next_url )
	# Grab content of current page
	html_content = current_page.text
	soup = BeautifulSoup( html_content,'lxml' )
	# Retrieving title text of the image. Use web developer tools to inspect the DOM.
	title_text = soup.find( 'div', {'id':'cc-comicbody'} ).img['title'].encode('ascii','ignore').decode()
	# Retrieving URL of the comic image
	comic_image_url = soup.find( 'div',{'id':'cc-comicbody'} ).img['src']	
	print("...")
	print("Processing comic number ", i)
	print("Image URL is: ", comic_image_url)

	# Numbering the directories
	comic_directory = str( i )
	os.mkdir( comic_directory )
	i = i + 1
	os.chdir( comic_directory )
	directory = os.getcwd()
	# DEBUG LOG	print("Current directory is: ", directory )
	
	title_text_file = open( comic_directory + '.txt', 'w' )
	title_text_file.write( title_text )
	title_text_file.close()
	# DEBUG LOG	print("Title text successfully written")
	
	# SMBC uses different image formats
	if ( "png" in comic_image_url ):
	# urllib.request.urlretrieve is considered deprecated https://docs.python.org/3/library/urllib.request.html#legacy-interface
	# Using urlopen instead
		with urllib.request.urlopen( comic_image_url ) as response, open( ( comic_directory + '.png'), 'wb') as out_file:
		    shutil.copyfileobj(response, out_file)
	elif ( "gif" in comic_image_url ):
	# urllib.request.urlretrieve is considered deprecated https://docs.python.org/3/library/urllib.request.html#legacy-interface
	# Using urlopen instead
		with urllib.request.urlopen( comic_image_url ) as response, open( ( comic_directory + '.gif'), 'wb') as out_file:
		    shutil.copyfileobj(response, out_file)
	else:
		print("Not a recognized image format!")
	
	next_url = soup.find('a',{'class':'cc-next'})['href']	
	os.chdir( parent_directory )
	
	# Basic pseudo-random wait to avoid detection by the target server. Change the range of values to go faster
	delay = random.randrange(3, 30)
	print("Comic number successfully scraped.")
	print("Waiting for ", delay, "seconds between requests to throw off anti-bot mitigation measures...")
	time.sleep( delay )
