# -*- coding: utf-8 -*-

import util2ch


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
    import random
    ita = random.choice(bbs.ita_list)
    print("ita:{}".format(str(ita)))

    # generate url for subject.txt of the ita
    print("subject url:[{}]".format(ita.url_subject()))
    print("ita local dir:[{}]".format(ita.dat_root()))
    ita.update()

    exit()

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
