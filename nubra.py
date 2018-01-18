from flask import Flask
from flask import render_template

import util2ch

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


@app.route('/hello')
def hello_world():
    return 'Hello, World! (by nubra)'


if __name__ == '__main__':
    import webbrowser
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run(port=5000)
