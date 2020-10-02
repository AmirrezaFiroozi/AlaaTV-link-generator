#!/bin/python3

# Written By Amirreza Firoozi under the license of GPLv3+
# For more information refer to the license file you've received with this file

import sys
import requests
import re
from bs4 import BeautifulSoup

SEPARATOR = '\n'

course_link = input('')
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
        media_link = f'https://cdn.alaatv.com/media/{parts[0]}/hq/{parts[1]}.mp4?download=1'
        print(media_link, end=SEPARATOR)
