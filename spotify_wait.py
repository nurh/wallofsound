#   Spotify Desktop Changer
#  
#   Copyright 2021 Nur Hussein (hussein@unixcat.org)
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

import os
import subprocess
import requests
import gi.repository.GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop

endpoint="http://127.0.0.1:5000/api/v1/wallpapers"
HOMEDIR = os.getenv('HOME')
DATADIR = HOMEDIR + "/.wallofsound"

def getPicFromWeb(url):
	file_name = os.path.basename(url)
	if not os.path.isfile(DATADIR+"/"+file_name):
		print("New file... downloading...")
		r = requests.get(url, allow_redirects=True)
		print("Getting file...")
		open(DATADIR+"/"+file_name, 'wb').write(r.content)
	else:
		print("File exists, no download required.")

def showSource(url):
	file_id = os.path.basename(url)
	token_list = file_id.split("_")
	print(f"Original picture from: http://flickr.com/photo.gne?id={token_list[0]}")


def notifications(bus, message):
	if message.get_destination() == bus_id:
		args = message.get_args_list()

		if str(args[0]) == "Spotify":
			songname=str(args[3])
			artist_album = str(args[4])
			artist_album_list = artist_album.split("-")
			artist = artist_album_list[0].strip()
			album = artist_album_list[1].strip()
			print(f"Now playing {songname} by {artist} from the album: {album}")
			response = requests.get(f"{endpoint}?song={songname}&artist={artist}")
			if response.status_code == 200:
				showSource(response.text)
				getPicFromWeb(response.text)
				subprocess.call(["./setwall.sh", "file://"+DATADIR+"/"+os.path.basename(response.text)])
			else:
				print("No picture found for query.")

if not os.path.exists(DATADIR):
	os.makedirs(DATADIR)

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

bus_id = bus.activate_name_owner("org.freedesktop.Notifications")

bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
