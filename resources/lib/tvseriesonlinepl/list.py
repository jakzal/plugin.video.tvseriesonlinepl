import requests
import re
from BeautifulSoup import BeautifulSoup

class Show:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def name(self):
        return self.name

    def url(self):
        return self.name


class Shows:
    def __init__(self, name):
        self.name = name
        self.list = []

    def add(self, show):
        self.list.append(show)

    def all(self):
        return self.list


class Episode:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def name(self):
        return self.name

    def url(self):
        return self.name


class Episodes:
    def __init__(self, name, image):
        self.name = name
        self.list = []
        self.image = image

    def add(self, episode):
        self.list.append(episode)

    def all(self):
        return self.list

    def image(self):
        return self.image

class PlayerSite:
    def __init__(self, url):
        self.url = url
        self.name = re.sub(r".*?://([^/]*)/.*", r"\1", url)

    def url(self):
        return self.url

    def name(self):
        return self.name


class PlayerSites:
    def __init__(self, name):
        self.name = name
        self.list = []

    def add(self, stream):
        self.list.append(stream)

    def all(self):
        return self.list


def shows():
    page = requests.get('http://www.tvseriesonline.pl')
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    links = soup.body.find('ul', {"id": "categories"}).findAll('a')

    show_list = Shows("All")
    for link in links:
        show_list.add(Show(link.text.encode('utf-8'), link.get("href").encode('utf-8')))

    return show_list


def episodes(show_url):
    page = requests.get(show_url)
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    headers = soup.body.find('div', {"id": "contentwrap2"}).findAll('h3')
    title = soup.body.find('div', {"class": "catdesc"}).find('h2').text
    image = soup.body.find('div', {"class": "catdesc"}).find('div', {"class": "catImage"}).find('img').get('src')

    episode_list = Episodes(title.encode('utf-8'), image.encode('utf-8'))
    for header in headers:
        for link in header.findAll('a'):
            episode_list.add(Episode(link.text.encode('utf-8'), link.get("href").encode('utf-8')))

    return episode_list


def player_sites(episode_url):
    sites = PlayerSites("All")

    page = requests.get(episode_url)
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    main_link = soup.body.find('div', {"class": "seriale"}).findNextSibling('a').get('href')
    other_links = soup.body.find('div', {"class": "seriale"}).findAll('li')

    page = requests.get(main_link)
    link = re.search('.*window.location.href=\'(.*)\'.*', page.content).group(1)
    sites.add(PlayerSite(link))

    for link in other_links:
        for a in link.findAll('a'):
            sites.add(PlayerSite(a.get('href').encode('utf-8')))

    return sites


#for show in shows().all():
#    print show.name+" "+show.url

# for episode in episodes("http://www.tvseriesonline.pl/elementary/").all():
#     print episode.name+" "+episode.url

# for stream in player_sites("http://www.tvseriesonline.pl/elementary/1x01-pilot-23/").all():
#    print stream.name+" "+stream.url