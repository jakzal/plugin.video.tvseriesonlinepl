# -*- coding: utf-8 -*-
# Module: default
# Author: Jakub Zalas
# Created on: 09.01.2015
# License: MIT https://opensource.org/licenses/MIT

import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
from urlparse import parse_qsl
from tvseriesonlinepl import list
import urllib
import xbmcgui
import xbmcplugin

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
    for episode in list.episodes(show_url).all():
        url = build_url({'action': 'list_players', 'episode_name': episode.name, 'episode_url': episode.url})
        li = xbmcgui.ListItem(episode.name, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)


def list_players(episode_url):
    for player_site in list.player_sites(episode_url).all():
        url = build_url({'action': 'play', 'player_site_name': player_site.name, 'player_site_url': player_site.url})
        li = xbmcgui.ListItem(player_site.name, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)


def play(player_site_url):
    xbmcgui.Dialog().ok("Play", player_site_url)


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
