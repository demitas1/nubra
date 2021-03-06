# nubra


"nubra" is an experimental python/flask project to create a new browser for open2ch.net.



## 概要

nubraは、おーぷん2ch用のブラウザを作ってみるプロジェクトです。
今のところ、Flaskを使ってp2ブラウザっぽいものを作るのことを想定しています。

## これまで出来たもの

### ブラウザの起動 (nubra)

- Flaskをコマンドラインから起動してブラウザを開く

```
$ ./nubra
```

- 板一覧の表示
- スレ一覧の表示


### 基礎部分 (util2ch.py)

- クラスの作成
- BBS, Ita, SureInfo, Sure, Resu
- Resu(レス)内容のHTML化

### CUIベースのサンプルプログラム (test.py)

- open2ch.netの板一覧を取ってくる
- ランダムに板を選んでトップ10のスレタイトルとdatファイル名を取る
- 板ごとのdatファイル置き場をつくって、スレ一覧を保存する
- トップにあるスレのdatの最後の3レスを表示する

```
$ python test.py
$ cat dat/open2ch.net/ita_list.txt
```

### Known issues

- たまに、文字コードエラーがでる

### ローカルdatディレクトリの構造

`dat`ディレクトリの下にBBSディレクトリ、サーバーディレクトリ、板ディレクトリが階層構造をともなって作成されます。ここに板ごとのdatファイルがセーブされる予定。

例：

```
$ tree ./dat
./dat
└── open2ch.net
    ├── awabi.open2ch.net
    │   └── camera
    │       └── sure_list.txt
    ├── ikura.open2ch.net
    │   ├── material
    │   │   └── sure_list.txt
    │   └── news5
    │       └── sure_list.txt
    └── ita_list.txt
```


### ライセンス

MIT License

----

以下、自分用メモ

### 開発環境セットアップ

- http接続、datのテキスト処理関係の基本部分

```
$ conda create --name nubra python=3
$ source activate nubra
$ pip install urllib3 lxml requests chardet python-dateutil
```

なんとなく必要そうなものを入れているが、必須でないものも多分ある

- Flaskのインストール

```
$ source activate nubra
$ pip install Flask
```

### environ memo

```
$ pip list

certifi (2017.11.5)
chardet (3.0.4)
click (6.7)
Flask (0.12.2)
idna (2.6)
itsdangerous (0.24)
Jinja2 (2.10)
lxml (4.1.1)
MarkupSafe (1.0)
pip (9.0.1)
python-dateutil (2.6.1)
requests (2.18.4)
setuptools (38.4.0)
six (1.11.0)
urllib3 (1.22)
Werkzeug (0.14.1)
wheel (0.30.0)

$ conda list

ca-certificates           2017.11.5                     0    conda-forge
certifi                   2017.11.5                py36_0    conda-forge
chardet                   3.0.4                     <pip>
click                     6.7                       <pip>
Flask                     0.12.2                    <pip>
idna                      2.6                       <pip>
itsdangerous              0.24                      <pip>
Jinja2                    2.10                      <pip>
lxml                      4.1.1                     <pip>
MarkupSafe                1.0                       <pip>
ncurses                   5.9                          10    conda-forge
openssl                   1.0.2n                        0    conda-forge
pip                       9.0.1                    py36_1    conda-forge
python                    3.6.4                         0    conda-forge
python-dateutil           2.6.1                     <pip>
readline                  7.0                           0    conda-forge
requests                  2.18.4                    <pip>
setuptools                38.4.0                   py36_0    conda-forge
six                       1.11.0                    <pip>
sqlite                    3.20.1                        2    conda-forge
tk                        8.6.7                         0    conda-forge
urllib3                   1.22                      <pip>
Werkzeug                  0.14.1                    <pip>
wheel                     0.30.0                   py36_2    conda-forge
xz                        5.2.3                         0    conda-forge
zlib                      1.2.11                        0    conda-forge
```
