#!/usr/bin/env zsh
# Example command to launch Brave Browser for macOS
cd "${0:A:h}"
python3 crlaunch.py -d ~/Library/Application\ Support/BraveSoftware/Brave-Browser -e "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
