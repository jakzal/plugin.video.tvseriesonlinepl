# Author: Jakub Zalas
# License: MIT https://opensource.org/licenses/MIT

import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
from urlparse import parse_qsl
from tvseriesonlinepl import list
from threading import Thread
import urllib
import xbmcgui
import xbmcplugin
import urlresolver

_url = sys.argv[0]
_handle = int(sys.argv[1])


def build_url(query):
    return _url + '?' + urllib.urlencode(query)


def list_shows():
    for show in list.shows().all():
        url = build_url({'action': 'list_episodes', 'show_name': show.name, 'show_url': show.url})
        li = xbmcgui.ListItem(show.name, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)


def list_episodes(show_url):
    episodes = list.episodes(show_url)
    for episode in episodes.all():
        url = build_url({'action': 'list_players', 'episode_name': episode.name, 'episode_url': episode.url})
        li = xbmcgui.ListItem(episode.name, iconImage=episodes.image)
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)


def list_players(episode_url):
    sites = list.player_sites(episode_url)
    threads = []
    for player_site in sites.all():
        thread = Thread(target=resolve_media_url, args=(player_site, sites))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    xbmcplugin.endOfDirectory(_handle)


def resolve_media_url(player_site, sites):
    media_url = urlresolver.resolve(player_site.url)
    item_name = player_site.name
    if not media_url:
        item_name = ':( ' + item_name
    url = build_url({'action': 'play', 'player_site_name': player_site.name, 'player_site_url': media_url})
    li = xbmcgui.ListItem(item_name, iconImage=sites.image)
    if media_url:
        li.setInfo(type='Video', infoLabels={"Title": item_name})
        li.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=False)


def play(media_url):
    play_item = xbmcgui.ListItem(path=media_url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'list_episodes':
            list_episodes(params['show_url'])
        if params['action'] == 'list_players':
            list_players(params['episode_url'])
        if params['action'] == 'play':
            play(params['player_site_url'])
    else:
        list_shows()


if __name__ == '__main__':
    router(sys.argv[2][1:])
