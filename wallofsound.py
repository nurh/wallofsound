#!/usr/local/src/virtualenv/wall/bin/python
#
#   Copyright 2016-2021 Nur Hussein (hussein@unixcat.org)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from rake_nltk import Rake
from nltk.corpus import stopwords
from flickrapi import FlickrAPI
import requests
import validators
import lyricsgenius
import random
import re
import sys
import os
import subprocess

# Keys

FLICKR_PUBLIC = INSERT_YOUR_KEY_HERE
FLICKR_SECRET = INSERT_YOUR_KEY_HERE
GENIUS_ACCESS_TOKEN = INSERT_YOUR_KEY_HERE

# Tunables

MAX_NGRAM_SIZE = 2
MIN_WIDTH = 1024
MIN_HEIGHT = 900
MAX_PHRASES = 3

# Data directory

HOMEDIR = os.getenv('HOME')
DATADIR = HOMEDIR + "/.wallofsound"

# Init Rake

r = Rake(max_length=MAX_NGRAM_SIZE)

# Create Flickr object

flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
extras='url_o'

# Create Genius object and turn off status messages

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
genius.verbose = False

def filterForExif(id):
	try:
		getexif = flickr.photos.getExif(photo_id=id)
		if getexif:
			if getexif['photo']['camera']:
				return True
			else:
				return False
		else:
			return False
	except:
		return False

def getFlickrPics(keyword):

	photo_set = []

	wallcandidate = flickr.photos.search(text=keyword, content_type=1, per_page=10, extras=extras, sort='interestingness-desc', license='2,3,4,5,6,7')
	result = wallcandidate['photos']

	photos = result['photo']

#	print(photos)

	for item in photos:
		if item['width_o'] >= MIN_WIDTH and item['height_o'] >= MIN_HEIGHT:
			if filterForExif(item['id']):
				photo_set.append(item['url_o'])

	return photo_set

def getLyrics(song_artist, song_title):
	song = genius.search_song(title=song_title,artist=song_artist)

	if song is not None:
		x = song.lyrics
		return x.replace("EmbedShare URLCopyEmbedCopy", "")
	else:
		return None

def buildSearchString(song_title, song_keywords):
	x = random.randint(0,100)

	if x<33:
		return song_title
	else:
		flickr_search_string = random.choice(song_keywords) 
		return flickr_search_string

def getPicFromWeb(url):
	if(validators.url(url)):
		r = requests.get(url, allow_redirects=True)
		open(DATADIR+"/"+os.path.basename(url), 'wb').write(r.content)
	else:
		print("Malformed URL. No file downloaded.")


def getWall(song):
	song = re.sub(r'\(.*?\)', "", song)
	song = re.sub(r'\[.*?\]', "", song)
	artist, song_title = song.split(' - ')

	print(song)
	print("---")
	song_lyrics = getLyrics(artist, song_title)

	if song_lyrics:
		r.extract_keywords_from_text(song_lyrics)

		phrases_list_raw = r.get_ranked_phrases()

		phrases_list=[s for s in phrases_list_raw if not s.startswith('verse')]

	
		if phrases_list:
			if len(phrases_list) > MAX_PHRASES:
				phrases_list = phrases_list[:MAX_PHRASES]
	
			print("Candidate phrases to search for:")
			print(phrases_list)
			search_term = random.choice(phrases_list)
			print("---")
		else:
			search_term = song_title
	else:
		search_term = song_title


	print("Searching Flickr for search term "+search_term)
	pics = getFlickrPics(search_term)

	if pics:
		selected_pic = random.choice(pics)
		print(selected_pic)
		getPicFromWeb(selected_pic)
		subprocess.call(["./setwall.sh", "file://"+DATADIR+"/"+os.path.basename(selected_pic)])
	else:
		print("No picture found.")


# Create the data dir if it doesn't exist
if not os.path.exists(DATADIR):
	os.makedirs(DATADIR)

if len(sys.argv)<2:
	sys.exit(1)
else:
	song = ' '.join([str(foo) for foo in sys.argv[1:]])
	getWall(song)

