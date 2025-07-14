#!/usr/bin/env python

import argparse
from datetime import datetime
import json
import os
import sys
import zipfile

def get_bookmarks(users, list, zip, descriptions):
	for user in users:
		filename = 'bookmarks.html' if len(users) < 2 else f'bookmarks-{user['Username']}.html'
		write_files = False
		while write_files == False:
			if os.path.isfile(os.path.join(os.path.curdir, filename)):
				response = None
				while not (response == 'y' or response == 'n'):
					response = input(f'Bookmarks file {filename} exists in current directory. Overwrite? (y/n) ').lower()
				if(response == 'y'):
					write_files = True
				else:
					print('No changes made to existing bookmarks file.')
					break
			else:
				write_files = True
		if write_files == True:
			try:
				with open(filename, 'w') as bookmarks:
					bookmarks.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!--This is an automatically generated file.\nIt will be read and overwritten.\nDo Not Edit! -->\n<Title>Bookmarks</Title>\n<H1>Bookmarks</H1>\n\n')
					bookmarks.write('<DL><p>\n')
					count = 0
					for item in list:
						with zip.open(item) as bookmark_file:
							data = json.loads(bookmark_file.read())
							if user['ID'] == data['UserID']:
								title = data['Title']
								url = data['URL'].split('?')[0]
								created_date = int(datetime.strptime(data['Created'][:data['Created'].rfind(':')], '%Y-%m-%dT%H:%M').timestamp())
								updated_date = int(datetime.strptime(data['Updated'][:data['Updated'].rfind(':')], '%Y-%m-%dT%H:%M').timestamp())
								tags = ','.join(tag for tag in data['Labels']) if data.get('Labels') != None else ''
								bookmarks.write(f'<DT><A HREF="{url}" ADD_DATE="{created_date}" LAST_MODIFIED="{updated_date}" TAGS="{tags}">{title}</A>\n')
								if descriptions == True:
									description = data.get('Description')
									if description != None:
										bookmarks.write(f'<DD>{description}\n')
								count += 1
					bookmarks.write('</DL><p>')
				print(f'{count} bookmark{'s' if count > 1 else ''} exported to {filename}.')
			except Exception as e:
				print(f'Failed to extract data from archive: {str(e)}')

def main():
	try:
		parser = argparse.ArgumentParser(description='Generates Netscape HTML bookmarks files from Readeck (https://readeck.org) backups.')
		parser.add_argument('file', help='path to Readeck backup file (.zip format)')
		parser.add_argument('-d', '--descriptions', help='keep descriptions from Readeck in HTML bookmarks', action='store_true')
		args = parser.parse_args()

		try:
			with zipfile.ZipFile(args.file) as zip:
				try:
					with zip.open('data.json') as data_file:
						data = json.loads(data_file.read())
						users = data['Users']
						list = [name for name in zip.namelist() if name.endswith('info.json')]
						if len(list) > 0:
							get_bookmarks(users, list, zip, args.descriptions)
						else:
							print('No valid bookmarks found in archive.')
				except:
					print('No Readeck data file found in archive.')
			
		except Exception as e:
			print(f'Failed to write bookmarks file: {str(e)}')

	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
