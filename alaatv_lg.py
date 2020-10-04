#!/bin/python3

# Written By Amirreza Firoozi under the license of GPLv3+
# For more information refer to the license file you've received with this file

import sys
import requests
import re
from bs4 import BeautifulSoup

# get course_link as a sys argument or internal input
if len(sys.argv) > 1 and sys.argv[1] != '--save':
    course_link = sys.argv[1]
else:
    course_link = input('please enter set url. scheme: https://alaatv.com/set/000' + os.linesep)

if (len(sys.argv) > 1 and sys.argv[1] == '--save') or (len(sys.argv) > 2 and sys.argv[2] == '--save'):
    save_it = 1
else:
    save_it = 0

# exit if link not provided
if course_link == '':
    print('No Valid link entered. Exitting...')
    sys.exit(1)
try:
    page = requests.get(course_link)
except:
    print(
        f'cannot GET url {course_link}. Valid URL scheme: https://alaatv.com/set/000')
    sys.exit(1)

if page.status_code != 200:
    print(
        f'Error {page.status_code} while fetching url {course_link}. Exitting...')
    sys.exit(2)

soup = BeautifulSoup(page.content, 'html.parser')
for script_tag in soup.find_all('script'):
    script_tag = str(script_tag)
    if 'var videos' not in script_tag:
        continue
    thumbnail_links = re.findall("photo: ('.+?')", script_tag)
    for thumbnail_link in thumbnail_links:
        parts = re.findall('/([0-9]+/.+).jpg', thumbnail_link)[0].split('/')

        media_link_hd = f'https://cdn.alaatv.com/media/{parts[0]}/HD_720p/{parts[1]}.mp4?download=1'
        media_link_hq = f'https://cdn.alaatv.com/media/{parts[0]}/hq/{parts[1]}.mp4?download=1'
        media_link_240p = f'https://cdn.alaatv.com/media/{parts[0]}/240p/{parts[1]}.mp4?download=1'

        print('-' * 70)
        print('HD: ', media_link_hd, end=os.linesep)
        print('hq: ', media_link_hq, end=os.linesep)
        print('240p: ', media_link_240p, end=os.linesep)
        if save_it:
            links = list()
            links.append(media_link_hd)
            links.append(media_link_hq)
            links.append(media_link_240p)
            data[parts[1]] = links
    if save_it:
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
