# -*- coding:utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import argparse
from naver_adapter import *

from collections import deque

Keyword_List = []
Sub_Page_Lst = deque()
now_dirname = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloader for post.naver.com')

    parser.add_argument('MemberNo', help='Member ID shown in url. See readme.md if need.')
    parser.add_argument('-k', '--keyword', required=False, nargs='+',
                        help='Keyword to search and crawl. It can be single string or list. If not, will crawl all pages.')
    parser.add_argument('-d', '--date', required=False, action='store_true', help='Use it if you need download with date')
    parser.add_argument('-n', '--name', required=False, default="Naver_Post_Download",
                        help='Download specific folder. default: Naver_Post_Download')
    args = parser.parse_args()
    if args.keyword: [Keyword_List.append(i) for i in args.keyword]
    MemberNo = args.MemberNo
    DownloadDate = args.date
    Dir_Name = args.name

    # ----------- Args Parse Done ----------

    try:
        os.makedirs(now_dirname + "/log")
    except OSError:
        pass

    while True:
        driver = init()
        if (driver != -1):
            break
    if not Keyword_List:
        driver.get('https://post.naver.com/my.nhn?memberNo=' + MemberNo)
        driver.implicitly_wait(2)
        user_name = driver.find_element_by_class_name('name').text
        Keyword_List = [-1]
    else:
        driver.get('https://post.naver.com/search/authorPost.nhn?memberNo=' + MemberNo)
        driver.implicitly_wait(2)
        user_name = driver.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/h2/div/span[1]').text

    print("Download '%s' Posts" % user_name)

    for Keyword in Keyword_List:
        Download_Done = []
        Download_Done_Num = -1
        chklink = ""
        if Keyword != -1:
            driver.get('https://post.naver.com/search/authorPost.nhn?memberNo=' + MemberNo)
            driver.implicitly_wait(2)
            driver.find_element_by_id('inputSearchKeyword').send_keys(Keyword)
            driver.find_element_by_class_name('btn_search').click()
            CsvFile = now_dirname + "/log/" + str(user_name) + "_" + str(Keyword) + ".csv"
            FileDes = now_dirname + "/" + Dir_Name + "/" + user_name + "/" + Keyword
            print("Search %s Keyword" % (Keyword))
        else:
            driver.get('https://post.naver.com/my.nhn?memberNo=' + MemberNo)
            driver.implicitly_wait(2)
            CsvFile = now_dirname + "/" + "log/" + str(user_name) + ".csv"
            FileDes = now_dirname + "/" + Dir_Name + "/" + user_name + "/_All"

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'lst_feed'))
            )
        except Exception as ex:
            print(ex)
            exit()

        try:
            OpenFile = open(CsvFile, 'r', encoding='utf-8')
            rdr = csv.reader(OpenFile)
            for i in rdr:
                # Add already downloaded links to list
                if Download_Done_Num == -1:
                    Download_Done_Num = int(i[0])
                Download_Done.append(i[4])
        except FileNotFoundError:
            Download_Done_Num = 0
        group = get_titles(driver)

        for i in group:
            imggroup = i.find_all('div', {'class': "image_area"})
            for j in imggroup:
                link = j.find('a', {'class': "link_end"})['href']
                chklink = link.split("volumeNo=")[1].split("&")[0]
                if chklink not in Download_Done:
                    Sub_Page_Lst.append([link,chklink])
                else:
                    break

        Sub_Page_Num = len(Sub_Page_Lst)
        for i in range(1, Sub_Page_Num + 1):
            Link,chklink = Sub_Page_Lst.pop()
            driver.get("https://post.naver.com" + Link)
            driver.implicitly_wait(3)
            print(str(Sub_Page_Num) + " / " + str(i) + ": ", end="")

            Title, MakeDir, Fail_Image = crawler(driver.page_source, FileDes, DownloadDate)

            # Write original post link
            f = open(MakeDir + "link.txt", "w")
            f.write("https://post.naver.com" + Link)
            f.close()

            print("Done!")

            # Write csv which has downloaded
            f = open(CsvFile, 'a', encoding='utf-8', newline='')
            wr = csv.writer(f)
            wr.writerow([Download_Done_Num + i, Title, user_name, Keyword, chklink, MakeDir, Fail_Image])
            f.close()

