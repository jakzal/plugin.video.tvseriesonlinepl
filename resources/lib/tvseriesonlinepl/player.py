from lxml import html
import requests
import re

def find_stream_anyfiles(url):
    base_url = re.sub(r"^([^:]*://[^/]*)/.*", r"\1", url)

    page = requests.get(url)
    tree = html.fromstring(page.content)
    iframe = tree.xpath('//div[@id="VideoInfoLoadDiv"]/preceding-sibling::iframe[1]')[0]
    iframe_src = base_url+iframe.get('src');

    page = requests.get(iframe_src, headers={'referer': url})
    tree = html.fromstring(page.content)
    script = tree.xpath('//script[contains(@src, "/pcs?")][1]')[0]
    script_src = base_url+script.get('src')

    page = requests.get(script_src, {'referer': iframe_src, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'})
    print iframe_src
    print script_src
    print page.content


    return iframe_src

def find_stream(player_site):
    if "video.anyfiles.pl" in player_site:
        return find_stream_anyfiles(player_site)

    return ""

print find_stream("http://video.anyfiles.pl/Elementary+S01E01+PL/Kino+i+TV/video/40326")