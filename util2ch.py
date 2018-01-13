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


default_ua = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36' }

bbs_name = 'おーぷん2ch'
url_bbs = 'http://open2ch.net'
url_bbsmenu = 'http://menu.open2ch.net/bbsmenu.html'

data_dir = './dat'
file_bbsmenu = 'ita_list.txt'


def get_from_server(url, charset=None):
    # wait 2sec to avoid server overload
    time.sleep(2)

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


if __name__ == '__main__':
    # get bbs menu
    content = get_from_server(url_bbsmenu)

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

    # make dat root dir for the bbs
    o = urlparse(url_bbs)
    dat_bbs_root = os.path.join(data_dir, o.netloc)
    print(dat_bbs_root)
    if not os.path.isdir(dat_bbs_root):
        os.makedirs(dat_bbs_root, exist_ok=True)

    # save ita list to a file
    path_bbsmenu = os.path.join(dat_bbs_root, file_bbsmenu)
    with codecs.open(path_bbsmenu, 'w', 'utf-8') as f:
        for ita in ita_list:
            f.write('\t'.join(ita))
            f.write('\n')

    # choose ita randomly
    import random
    ita_info = random.choice(ita_list)
    ita_category, ita_title, ita_url = ita_info
    print("{}:{}:{}".format(ita_category, ita_title, ita_url))

    # generate url for subject.txt of the ita
    o = urlparse(ita_url)
    p = o.path
    if p[-1] != '/':
        p += '/'
    subject_url = "http://" + o.netloc + p + "subject.txt"
    print("subject url:{}".format(subject_url))

    # generate local file path for subjects
    p = o.path
    if p[0] == '/':
        p = p[1:]
    dat_ita_root = os.path.join(dat_bbs_root, o.netloc, p)
    print("ita local dir:{}".format(dat_ita_root))

    # get subject.txt from the server
    subject_txt = get_from_server(subject_url)

    # parse subject.txt to make sure list
    sure_list = []
    subject_lines = subject_txt.split('\n')
    for s in subject_lines:
        m = re.match(r'(\d+?\.dat)<>(.*) \((\d+)\)$', s.rstrip())
        if m:
            dat_name = m.group(1)
            dat_title = m.group(2)
            dat_resu = m.group(3)
            sure_list.append((dat_name, dat_title, dat_resu))

    # format and save sure list to local file "sure_list.txt".
    if not os.path.isdir(dat_ita_root):
        os.makedirs(dat_ita_root, exist_ok=True)
    path_subjects = os.path.join(dat_ita_root, "sure_list.txt")
    with codecs.open(path_subjects, 'w', 'utf-8') as f:
        for s in sure_list:
            f.write('\t'.join(s))
            f.write('\n')

    # output top-10 sure for test
    for i in range(0, min(10, len(sure_list))):
        dat_name, dat_title, dat_resu = sure_list[i]
        print("{}:{} ({})".format(dat_name, dat_title, dat_resu))

    # generate dat url/local path for the top sure
    dat_name, dat_title, dat_resu = sure_list[0]
    dat_url = urljoin(ita_url, 'dat/' + dat_name)
    print("dat url:[{}]".format(dat_url))
    dat_local_path = os.path.join(dat_ita_root, dat_name)
    print("dat local path:[{}]".format(dat_local_path))

    # compare local dat file to check newer resu
    if os.path.exists(dat_local_path):
        with open(dat_local_path, 'r') as f:
            dat_content = f.readlines()
            n_resu_dat_local = len(dat_content)
    else:
        n_resu_dat_local = 0
    n_resu_dat_server = int(dat_resu)
    print("server[{}]:local[{}]".format(n_resu_dat_server, n_resu_dat_local))
    exists_newer_dat = n_resu_dat_server > n_resu_dat_local

    # get latest dat file from the server
    if exists_newer_dat:
        dat_content = get_from_server(dat_url)
        # save dat file
        with codecs.open(dat_local_path, 'w', 'utf-8') as f:
            f.write(dat_content)

    # show last 3 resu of the sure
    dat_lines = dat_content.split('\n')
    for l in dat_lines[-3:]:
        print(l)
