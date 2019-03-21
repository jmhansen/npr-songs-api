import logging
from datetime import datetime, timedelta
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_npr_links_from_archive_page(archive_url, show_urls=[], depth=10):
    r = requests.get(archive_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        shows_raw = soup.find_all(class_='program-show__title')
        show_urls += [show.find('a')['href'] for show in shows_raw]

        # dedupe show_urls
        if show_urls:
            show_urls = list(OrderedDict.fromkeys(show_urls))

        if len(show_urls) < depth:
            # parse 'https://www.npr.org/programs/morning-edition/2019/03/19/704683333/morning-edition-for-march-19-2019?showDate=2019-03-19'
            oldest_show_date = show_urls[-1].split('showDate=')[-1]
            episode_id = show_urls[-1].split('/')[8]
            # # strip the archive url of any url parameters
            cleaned_archive_url = archive_url.split('?date')[0]

            # the episode id is required, so this will add a duplicate url to the list each time
            # which is why we need to dedupe above
            if oldest_show_date and episode_id:
                oldest_show_archive_url = cleaned_archive_url + '?date={}&eid={}'.format(oldest_show_date, episode_id)
                logger.info('fetching links from {}'.format(oldest_show_archive_url))
                show_urls += get_npr_links_from_archive_page(oldest_show_archive_url, show_urls, depth=depth)

        # dedupe show_urls _again_
        if show_urls:
            show_urls = list(OrderedDict.fromkeys(show_urls))

        return show_urls


def get_songs_from_programs_page(url, program=None):
    # r = requests.get('http://www.npr.org/programs/morning-edition/')
    r = requests.get(url)

    if r.status_code == 200:

        soup = BeautifulSoup(r.text, 'lxml')
        raw_show_date = soup.find(class_='date').text
        show_date = raw_show_date.splitlines()[2].lstrip()

        if program:
            show_title = program.name
        else:
            show_title = soup.title.text.split(' : ')[0]
            show_title = show_title.split(' for ')[0]  # Should return u'Morning Edition'

        songs = soup.find_all(class_='song-meta-wrap')

        song_list = []

        for song in songs:
            # solve for empty song_title or artist tag
            if song.find(class_='song-meta-title'):
                song_title = song.find(class_='song-meta-title').text.strip()
            else:
                song_title = ''

            if song.find(class_='song-meta-artist'):
                artist = song.find(class_='song-meta-artist').text.strip()
            else:
                artist = ''

            if song_title and artist:
                song_dict = {
                    'song_title': song_title,
                    'artist': artist,
                    'order': songs.index(song),
                    'program': show_title,
                    'date': show_date
                }
                song_list.append(song_dict)

        logger.info("{} songs in song_list".format(len(song_list)))
        return song_list

    else:
        logger.info("Status code {} for url {}".format(r.status_code, url))


def crawl_for_song_lists(url_list, program):
    song_list = []
    for url in url_list:
        logger.info("starting {}".format(url))
        song_list.extend(get_songs_from_programs_page(url=url, program=program))
        logger.info("finished {}".format(url))

    return song_list
