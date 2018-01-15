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
    "data_dir": "./dat",
    "file_bbsmenu": "ita_list.txt",
    "wait_get": 2,
    }

default_ua = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
    }


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
                    ita = Ita(ita_category, ita_title, ita_url, parent=self)
                    self.ita_list.append(ita)

    def save_ita_list(self):
        # save ita list to a file
        path_bbsmenu = os.path.join(self.dat_bbs_root, config["file_bbsmenu"])
        with codecs.open(path_bbsmenu, 'w', 'utf-8') as f:
            for ita in self.ita_list:
                f.write(str(ita) + '\n')


class Ita(object):
    def __init__(self, category, title, url, parent=None):
        self.parent = parent
        self.category = category
        self.title = title
        self.url = url
        self._url_subject = None
        self._dat_root = None
        self.sure_list = []

    def __str__(self):
        return "{}\t{}\t{}".format(
            self.category,
            self.title,
            self.url)

    def url_subject(self):
        if self._url_subject is None:
            # generate url for subject.txt of the ita
            o = urlparse(self.url)
            p = o.path
            if p[-1] != '/':
                p += '/'
            self._url_subject = "http://" + o.netloc + p + "subject.txt"
        return self._url_subject

    def dat_root(self):
        if self._dat_root is None:
            if self.parent and self.parent.dat_bbs_root:
                # generate local file path for subjects
                o = urlparse(self.url)
                p = o.path
                if p[0] == '/':
                    p = p[1:]
                self._dat_root = os.path.join(
                    self.parent.dat_bbs_root,
                    o.netloc,
                    p)
        return self._dat_root

    def update(self):
        subject_txt = self.get_from_server()
        self.read_from_text(subject_txt)
        self.save_sure_list()

    def get_from_server(self):
        subject_txt = get_from_server(self.url_subject())
        return subject_txt

    def read_from_text(self, subject_txt):
        # parse subject.txt to make sure list
        self.sure_list = []
        subject_lines = subject_txt.split('\n')
        for s in subject_lines:
            sure_info = SureInfo(self)
            if sure_info.read_from_text(s):
                self.sure_list.append(sure_info)

    def save_sure_list(self):
        dat_ita_root = self.dat_root()
        if not dat_ita_root:
            return

        # format and save sure list to local file "sure_list.txt".
        if not os.path.isdir(dat_ita_root):
            os.makedirs(dat_ita_root, exist_ok=True)
        path_subjects = os.path.join(dat_ita_root, "sure_list.txt")
        with codecs.open(path_subjects, 'w', 'utf-8') as f:
            for s in self.sure_list:
                f.write(str(s) + '\n')


class SureInfo(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.dat_name = None
        self.title = None
        self.n_resu = None
        self._path_dat = None
        self._url_dat = None
        self.dat_content = None
        self._exists_newer = None

    def __str__(self):
        return '{}\t{}\t{}'.format(
            self.dat_name,
            self.title,
            self.n_resu)

    def read_from_text(self, s):
        m = re.match(r'(\d+?\.dat)<>(.*) \((\d+)\)$', s.rstrip())
        if m:
            self.dat_name = m.group(1)
            self.title = m.group(2)
            self.n_resu = int(m.group(3))
            return True
        else:
            return False

    def url_dat(self):
        if not self._url_dat:
            if not self.dat_name:
                return None
            if not self.parent:
                return None
            if not self.parent.url:
                return None
            self._url_dat = urljoin(self.parent.url, 'dat/' + self.dat_name)
        return self._url_dat

    def path_dat(self):
        if not self._path_dat:
            if not self.dat_name:
                return None
            if not self.parent:
                return None
            dat_ita_root = self.parent.dat_root()
            if not dat_ita_root:
                return None
            self._path_dat = os.path.join(dat_ita_root, self.dat_name)
        return self._path_dat

    def exists_newer(self):
        if self.n_resu is None:
            pass  # todo: throw exception
        if self.path_dat() is None:
            pass  # todo: throw exception

        if self._exists_newer is None:
            # compare local dat file to check newer resu
            if os.path.exists(self.path_dat()):
                self.load_from_local()
                n_resu_dat_local = len(self.dat_content)
            else:
                n_resu_dat_local = 0
            n_resu_dat_server = self.n_resu
            self._exists_newer = n_resu_dat_server > n_resu_dat_local
        return self._exists_newer

    def load_from_local(self):
        if self.path_dat() is None:
            pass  # todo: throw exception

        if self.dat_content is None:
            with open(self.path_dat(), 'r') as f:
                self.dat_content = f.readlines()
        return self.dat_content

    def save_to_local(self):
        if self.path_dat() is None:
            pass  # todo: throw exception
        if self.dat_content is None:
            pass  # todo: throw exception

        with codecs.open(self.path_dat(), 'w', 'utf-8') as f:
            f.write(self.dat_content)

    def get_from_server(self):
        if self.url_dat() is None:
            pass  # todo: throw exception
        self.dat_content = get_from_server(self.url_dat())
        return self.dat_content


class Sure(object):
    def __init__(self):
        self.resu = []

    def __len__(self):
        return len(self.resu)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self.resu[i] for i in range(key.start, key.stop)]
        elif key < len(self.resu):
            return self.resu[key]
        else:
            return None

    def __iter__(self):
        return iter(self.resu)

    def length(self):
        return len(self.resu)

    def append(self, new_resu):
        self.resu.append(new_resu)


class Resu(object):
    def __init__(self):
        self.raw_text = None
