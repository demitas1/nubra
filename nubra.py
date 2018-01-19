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
    ita = util2ch.Ita('', ita_title, ita_url)
    ita.update()
    data = []
    for sure_info in ita.sure_list:
        s = {
            "title": sure_info.title,
            "n_resu": sure_info.n_resu,
            "url_dat": sure_info.url_dat(),
            }
        data.append(s)
    return json.dumps(data)


@app.route('/sure', methods=['GET'])
def sure_view():
    url = request.args.get("url")
    j = {"url": url}
    return json.dumps(j)


if __name__ == '__main__':
    import webbrowser
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run(port=5000)
