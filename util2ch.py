# -*- coding: utf-8 -*-

from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import codecs
import chardet
import lxml.html
import re
import time
import os
import os.path


config = {
    "data_dir" : "./dat",
    "file_bbsmenu" : "ita_list.txt",
    "wait_get" : 2,
    }

default_ua = { "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36" }


def get_from_server(url, charset=None):
    # wait 2sec to avoid server overload
    time.sleep(config["wait_get"])

    # get html from url
    try:
        req = Request(url, headers=default_ua)
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
    if charset is None:
        char_guessed = chardet.detect(data_bytes)
        content = data_bytes.decode(char_guessed['encoding'])
    else:
        content = data_bytes.decode(charset)
    return content


class BBS(object):
    def __init__(self, bbs_property):
        self.bbs_name = bbs_property["bbs_name"]
        self.url_bbs = bbs_property["url_bbs"]
        self.url_bbsmenu = bbs_property["url_bbsmenu"]
        self.ita_list = []


    def make_dat_root(self):
        # make dat root dir for the bbs
        o = urlparse(self.url_bbs)
        self.dat_bbs_root = os.path.join(config["data_dir"], o.netloc)
        if not os.path.isdir(self.dat_bbs_root):
            os.makedirs(self.dat_bbs_root, exist_ok=True)


    def update(self):
        content = self.get_menu_from_server()
        self.update_ita_list(content)
        self.save_ita_list()

    def get_menu_from_server(self):
        return get_from_server(self.url_bbsmenu)

    def update_ita_list(self, content_bbs_menu):
        dom = lxml.html.fromstring(content_bbs_menu)
        body = dom.find('body')
        ita_category = '(no category)'
        for e in body.iter():
            if e.tag == 'b' and e.text and len(e.text) > 0:
                ita_category = e.text
            elif e.tag == 'a' and 'href' in e.attrib:
                ita_url = e.attrib['href']
                ita_title = e.text
                if re.match(r'http://', ita_url, re.I):
                    ita = Ita(ita_category, ita_title, ita_url)
                    self.ita_list.append(ita)

    def save_ita_list(self):
        # save ita list to a file
        path_bbsmenu = os.path.join(self.dat_bbs_root, config["file_bbsmenu"])
        with codecs.open(path_bbsmenu, 'w', 'utf-8') as f:
            for ita in self.ita_list:
                f.write(str(ita))
                f.write('\n')


class Ita(object):
    def __init__(self, category, title, url):
        self.category = category
        self.title = title
        self.url = url

    def __str__(self):
        return "{}\t{}\t{}".format(
            self.category,
            self.title,
            self.url)
