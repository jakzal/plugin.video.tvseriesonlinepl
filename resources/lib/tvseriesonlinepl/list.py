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
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def url(self):
        return self.url

    def name(self):
        return self.name


class PlayerSites:
    def __init__(self, name, image):
        self.name = name
        self.list = []
        self.image = image

    def add(self, stream):
        self.list.append(stream)

    def all(self):
        return self.list

    def image(self):
        return self.image


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
    headers = soup.body.find('article').findAll('h4')
    title = soup.body.find('article').find('h2').text
    image = soup.body.find('article').find('img').get('src')

    episode_list = Episodes(title.encode('utf-8'), image.encode('utf-8'))
    for header in headers:
        for link in header.findAll('a'):
            episode_list.add(Episode(link.text.encode('utf-8'), link.get("href").encode('utf-8')))

    return episode_list


def player_sites(episode_url):
    page = requests.get(episode_url)
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    links = soup.body.find('div', {"class": re.compile(r".*\bvideo-links\b.*")}).findAll('a')
    image = soup.body.find('div', {"class": "catImage"}).find('img').get('src')

    sites = PlayerSites("All", image)

    for link in links:
        url = link.get('href').encode('utf-8')
        group = link.findPrevious('h5').text.strip(':').encode('utf-8')
        name = re.sub(r".*?://([^/]*)/.*", r"\1", url)+" ("+group+")"
        sites.add(PlayerSite(url, name))

    return sites
