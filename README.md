# postnaver_Crawler

![preview](https://i.imgur.com/fxcJTus.gif)

Crawl image from post.naver.com with specific username / ID .

**[한글 README](README-KO.md)**

## Requirements
* Selenium
* Beautifulsoup4

## Dependencies
```
pip install -r requirements.txt
```

## Usage
```
usage: main.py [-h] [-k KEYWORD [KEYWORD ...]] [-d] [-n NAME] MemberNo

Downloader for post.naver.com

positional arguments:
  MemberNo              Member ID shown in url. See readme.md if need.

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD [KEYWORD ...], --keyword KEYWORD [KEYWORD ...]
                        Keyword to search and crawl. It can be single string
                        or list. If not, will crawl all pages.
  -d, --date            Use it if you need download with date
  -n NAME, --name NAME  Download specific folder. default: Naver_Post_Download
```
* You can find `MemberNo` by url. (Ex. https://post.naver.com/my.nhn?memberNo=2380229 => MemberNo = `2380229`)
* `-k KEYWORD [KEYWORD ...]` should be single keyword or list of keywords, such as `KEYWORD1 KEYWORD2 KEYWORD3 ...`
* `-d` option will makes sub directories with dates which post was written.
* `-n NAME` sets your download folder name. default is `Naver_Post_Download`


## TODO
* Support  crawl images with specific form `se_card_container`  (Ex. https://post.naver.com/viewer/postView.nhn?volumeNo=27198154&memberNo=43521146)