# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import codecs
import chardet


default_ua = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36' }

url_bbsmenu = 'http://menu.open2ch.net/bbsmenu.html'

if __name__ == '__main__':
    try:
        req = Request(url_bbsmenu, headers=default_ua)
        response = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.:{}'.format(url))
        print('Error code: ', e.code)
        exit()
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        exit()

    data_bytes = response.read()
    char_guessed = chardet.detect(data_bytes) 
    content = data_bytes.decode(char_guessed['encoding']) 
    print(content)
