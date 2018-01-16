# -*- coding: utf-8 -*-

import util2ch
import random
import os.path
import codecs


default_bbs = {
    "bbs_name": "おーぷん2ch",
    "url_bbs": "http://open2ch.net",
    "url_bbsmenu": "http://menu.open2ch.net/bbsmenu.html",
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

    # get latest dat file from the server
    if sure_info.exists_newer():
        print("get form server...")
        dat_content = sure_info.get_from_server()
        # save dat file
        sure_info.save_to_local()
    else:
        print("get form local file...")
        dat_content = sure_info.load_from_local()

    # show last 3 resu of the sure
    sure = util2ch.Sure(parent=ita)
    sure.read_from_text(dat_content)
    for r in sure[-3:]:
        if len(r.info_id) >= 3:
            print("{}: {}[{}] {} ID:{}".format(
                r.resu_number,
                r.user_name,
                r.email,
                r.info_datetime,
                r.info_id))
        else:
            print("{}: {}[{}] {}".format(
                r.resu_number,
                r.user_name,
                r.email,
                r.info_datetime))
        print(r.content_html)
