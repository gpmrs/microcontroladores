#!/bin/bash
cd "$(dirname "$0")"

cd extra/binarios/ffmpeg/mac
./ffmpeg -hide_banner -list_devices true -f avfoundation -i dummy
