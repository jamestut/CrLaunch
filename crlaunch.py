#!/usr/bin/env python3

import sys
import os
import argparse
import json
from collections import namedtuple

ProfileInfo = namedtuple('ProfileInfo', ['dirname', 'nickname'])

def start_launcher(datadir, exepath):
	with open(os.path.join(datadir, 'Local State'), 'r') as f:
		local_state_data = json.load(f)
	profile_infos = local_state_data.get('profile', {}).get('info_cache', {})
	profiles = sorted(ProfileInfo(dirname, pi['name']) for dirname, pi in profile_infos.items())

	if not len(profiles):
		print("(No profiles available)")
	print("Available profiles:")
	for i, profinfo in enumerate(profiles):
		if profinfo.dirname == profinfo.nickname:
			print(f" {i + 1}. {profinfo.dirname}")
		else:
			print(f" {i + 1}. {profinfo.nickname} ({profinfo.dirname})")
	print(" 0. (Cancel and exit)")

	while 1:
		try:
			rd = input('Select: ')
			idx = int(rd) - 1
			if idx < 0:
				sys.exit(0)
			if idx > len(profiles):
				raise ValueError()
			break
		except ValueError:
			print("Invalid input! Try again.")
	selected_profile = profiles[idx]

	os.execvp(exepath, [exepath, f"--profile-directory={selected_profile.dirname}"])

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
