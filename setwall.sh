#!/bin/bash

WALLDIR=${HOME}/.musicwall

if [ ! -d "$WALLDIR" ]; then
	mkdir $WALLDIR
fi

WALLURI=`cat $WALLDIR/WALLURI`

gsettings set org.gnome.desktop.background picture-uri $WALLURI
