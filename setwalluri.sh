#!/bin/bash
#
#   Copyright 2016 Nur Hussein (hussein@unixcat.org)
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

WALLDIR=${HOME}/.musicwall

if [ ! -d "$WALLDIR" ]; then
	mkdir $WALLDIR
fi

if [[ ${1:0:4} == "http" ]] ; then 
	WALLFILE=$WALLDIR/$(basename "$1")
	if [ -e $WALLFILE ]; then
		rm -f $WALLFILE
	fi
	
	cd $WALLDIR
	wget -q $1
elif [[ $1 == /* ]] ; then
	WALLFILE=$1
else
	WALLFILE="default"
fi

if [[ $WALLFILE == "default" ]]; then
	WALLURI=`gsettings get org.gnome.desktop.background picture-uri`
else
	WALLURI=\'file://$WALLFILE\'
fi

echo $WALLURI > $WALLDIR/WALLURI
#gsettings set org.gnome.desktop.background picture-uri $WALLURI
