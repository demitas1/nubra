# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import codecs
import chardet
import lxml.html
import re


default_ua = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36' }

url_bbsmenu = 'http://menu.open2ch.net/bbsmenu.html'

if __name__ == '__main__':
    # get html from url
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

    # decode html content text
    data_bytes = response.read()
    char_guessed = chardet.detect(data_bytes) 
    content = data_bytes.decode(char_guessed['encoding']) 

    # extract ita url and titles
    dom = lxml.html.fromstring(content)
    body = dom.find('body')
    ita_category = '(no category)'
    ita_list = []
    for e in body.iter():
        if e.tag == 'b' and e.text and len(e.text) > 0:
            ita_category = e.text
        elif e.tag == 'a' and 'href' in e.attrib:
            ita_url = e.attrib['href']
            ita_title = e.text
            if re.match(r'http://', ita_url, re.I):
                ita_list.append((ita_category, ita_title, ita_url))

    # save to a file
    with codecs.open('ita_list.txt', 'w', 'utf-8') as f:
        for ita in ita_list:
            f.write('\t'.join(ita))
            f.write('\n')
