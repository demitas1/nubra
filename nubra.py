# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template

import util2ch
import json

app = Flask(__name__, static_folder='static')

# initialize
default_bbs = {
    "bbs_name": "おーぷん2ch",
    "url_bbs": "http://open2ch.net",
    "url_bbsmenu": "http://menu.open2ch.net/bbsmenu.html",
    }


def bbs_init():
    # create BBS instance for open2ch.net
    global bbs
    bbs = util2ch.BBS(default_bbs)
    bbs.make_dat_root()
    if not bbs.load_ita_list():
        bbs.update()
    return bbs


@app.route('/')
def index():
    bbs = bbs_init()
    return render_template('index.html', ita_list=bbs.ita_list)


@app.route('/ita', methods=['GET'])
def hello():
    return 'Hello, World! args=[{}]'.format(request.args)


@app.route('/subjects', methods=['GET'])
def sure_subjects():
    ita_title = request.args.get("title")
    ita_url = request.args.get("url")
    if not ita_url:
        return "invalid sure url."
    ita = util2ch.Ita('', ita_title, ita_url, parent=bbs)
    ita.update()
    print("Ita dat root:[{}]".format(ita.dat_root()))
    data = []
    for sure_info in ita.sure_list:
        s = {
            "title": sure_info.title,
            "n_resu": sure_info.n_resu,
            "url_dat": sure_info.url_dat(),
            "path_dat": sure_info.path_dat(),
            }
        data.append(s)
    return json.dumps(data)


@app.route('/sure', methods=['GET'])
def sure_view():
    url = request.args.get("url")
    path = request.args.get("path")
    n_resu = request.args.get("n_resu")
    sure_info = util2ch.SureInfo(base_url=url, base_path=path, n_resu=n_resu)

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
    sure = util2ch.Sure()
    sure.read_from_text(dat_content)
    j_sure = []
    for r in sure[-3:]:
        if len(r.info_id) >= 3:
            j_resu = {
                "number": r.resu_number,
                "user_name": r.user_name,
                "email": r.email,
                "datetime": r.info_datetime,
                "user_id": r.info_id,
                }
        else:
            j_resu = {
                "number": r.resu_number,
                "user_name": r.user_name,
                "email": r.email,
                "datetime": r.info_datetime,
                "user_id": "",
                }
        j_sure.append(j_resu)

    return json.dumps(j_sure)


if __name__ == '__main__':
    import webbrowser
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run(port=5000)
