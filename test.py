# -*- coding: utf-8 -*-

import util2ch
import random
import os.path
import codecs


default_bbs = {
    "bbs_name" : "おーぷん2ch",
    "url_bbs" : "http://open2ch.net",
    "url_bbsmenu" : "http://menu.open2ch.net/bbsmenu.html",
    }


if __name__ == '__main__':
    # create BBS instance for open2ch.net
    bbs = util2ch.BBS(default_bbs)
    bbs.make_dat_root()
    bbs.update()

    # choose ita randomly
    ita = random.choice(bbs.ita_list)
    print("ita:{}".format(str(ita)))

    # generate url for subject.txt of the ita
    print("subject url:[{}]".format(ita.url_subject()))
    print("ita local dir:[{}]".format(ita.dat_root()))
    ita.update()

    # output top-5 sure for test
    for sure_info in ita.sure_list[:5]:
        print("{} ({})".format(sure_info.title, sure_info.n_resu))

    # generate dat url/local path for the top sure
    sure_info = ita.sure_list[0]
    print("dat local path:[{}]".format(sure_info.path_dat()))
    print("dat url:[{}]".format(sure_info.url_dat()))

    # compare local dat file to check newer resu
    if os.path.exists(sure_info.path_dat()):
        with open(sure_info.path_dat(), 'r') as f:
            dat_content = f.readlines()
            n_resu_dat_local = len(dat_content)
    else:
        n_resu_dat_local = 0
    n_resu_dat_server = sure_info.n_resu
    print("server[{}]:local[{}]".format(n_resu_dat_server, n_resu_dat_local))
    exists_newer_dat = n_resu_dat_server > n_resu_dat_local
    if exists_newer_dat:
        print("get from server...")
    else:
        print("read local file...")

    # get latest dat file from the server
    if exists_newer_dat:
        dat_content = util2ch.get_from_server(sure_info.url_dat())
        # save dat file
        with codecs.open(sure_info.path_dat(), 'w', 'utf-8') as f:
            f.write(dat_content)

    # show last 3 resu of the sure
    dat_lines = dat_content.split('\n')
    for l in dat_lines[-3:]:
        print(l)
