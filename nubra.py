from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    ita_list = [
        { 'title': 'ita 1', 'url': 'url1'},
        { 'title': 'ita 2', 'url': 'url2'},
        { 'title': 'ita 3', 'url': 'url3'},
        { 'title': 'ita 4', 'url': 'url4'},
        { 'title': 'ita 5', 'url': 'url5'},
    ]
    return render_template('index.html', ita_list=ita_list)


@app.route('/hello')
def hello_world():
    return 'Hello, World! (by nubra)'


if __name__ == '__main__':
    import webbrowser
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run(port=5000)
