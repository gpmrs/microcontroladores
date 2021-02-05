#!/bin/bash
cd "$(dirname "$0")"

cd extra/binarios/ngrok/mac
./ngrok http 5000
