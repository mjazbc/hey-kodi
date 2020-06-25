#!/bin/bash
texturecache.py watched tvshows backup ./automation/watchedbackup.json "$1"
path=$(python ./automation/getlast.py "$1")
texturecache.py play "$path"