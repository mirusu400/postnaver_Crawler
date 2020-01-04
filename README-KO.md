# postnaver_Crawler

![preview](https://i.imgur.com/fxcJTus.gif)

post.naver.com 사이트의 유저ID를 이용해 이미지를 크롤링하는 프로그램입니다 .


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
* `MemberNo` 는 URL에서 맨 뒤의 ID부분을 찾으면 됩니다.. (Ex. https://post.naver.com/my.nhn?memberNo=2380229 => MemberNo = `2380229`)
* `-k KEYWORD [KEYWORD ...]` 는 검색 키워드 한개나, 여러개가 연속해서 올 수 있습니다.  (Ex.`KEYWORD1 KEYWORD2 KEYWORD3 ...`)
* `-d` 옵션을 선택하면 폴더를 만들 때 글이 써진 날짜까지 같이 기록됩니다.
* `-n NAME` 를 이용하면 저장되는 폴더의 이름을 설정합니다. 기본값은 `Naver_Post_Download` 입니다.


