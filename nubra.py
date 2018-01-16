from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! (by nubra)'

if __name__ == '__main__':
    import webbrowser
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run()
