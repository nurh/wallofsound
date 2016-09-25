#!/bin/bash

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
