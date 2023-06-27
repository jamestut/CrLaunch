#!/usr/bin/env python3

import sys
import os
import argparse
import json
from collections import namedtuple

DirType = namedtuple('DirType', ['name', 'nickname'])

def start_launcher(datadir, exepath):
	exclusion = set(["System Profile"])

	available_dirs = []
	for e in os.scandir(datadir):
		if e.name in exclusion:
			continue
		try:
			pth = os.path.join(datadir, e.name, 'Preferences')
			with open(pth, 'rb') as f:
				pref = json.load(f)
		except (FileNotFoundError, NotADirectoryError):
			continue
		available_dirs.append(
			DirType(e.name, pref.get('profile', {}).get('name', None)))
	available_dirs.sort()

	print("Available profiles:")
	for i, cd in enumerate(available_dirs):
		if cd.nickname:
			print(f" {i + 1}. {cd.nickname} ({cd.name})")
		else:
			print(f" {i + 1}. {cd.name}")
	if not len(available_dirs):
		print("(No profiles available)")
		return

	while 1:
		try:
			rd = input('Select: ')
			idx = int(rd) - 1
			if idx < 0 or idx > len(available_dirs):
				raise ValueError()
			break
		except:
			print("Invalid selection! Try again.")
	cd = available_dirs[idx]

	os.execvp(exepath, [exepath, f"--profile-directory={cd.name}"])

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument( '-d', '--datadir',
		help='Location of Chromium\'s data directory.',
		required=True )
	parser.add_argument( '-e', '--exepath',
		help='Location of Chromium\'s executable.',
		required=True )
	args = parser.parse_args()
	start_launcher(args.datadir, args.exepath)

if __name__ == "__main__":
	main()
