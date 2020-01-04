# -*- coding:utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup

import os
import asyncio
import requests
from selenium import webdriver
Chrome_Driver_Dir = "C:/chromedriver.exe"
now_dirname = os.path.dirname(os.path.abspath(__file__))

def init():
    options = webdriver.ChromeOptions()

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('window-size=1920x1080')
    options.add_argument('headless')

    options.add_argument("disable-gpu")  # 가속 사용 x
    options.add_argument("lang=ko-KR")  # 가짜 플러그인 탑재
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
    driver = webdriver.Chrome(Chrome_Driver_Dir, chrome_options=options)
    return driver

def crawler(req, dir, DownloadDate):
    Fail_Image = 0
    soup = BeautifulSoup(req, 'html.parser')
    Title = soup.find("meta", property="og:title")['content'].strip()
    if(soup.find("div",{"class":"flick-container"})):
        print(str(Title) + " Cannot Download, " , end=" ")
        return Title, "", -1
    if(DownloadDate): Date = soup.find("span",{'class':'se_publishDate'}).text.split(" ")[0]
    else: Date = ""
    SecDiv = soup.find("div", {'class': 'se_component_wrap sect_dsc __se_component_area'})
    Piclist = SecDiv.find_all("img")

    # Remove Pics that Doesn't need
    for i in range(0,len(Piclist)):
        # Remove Sticker image
        try:
            if Piclist[i]['alt'] == '스티커 이미지':
                del Piclist[i]
        except:
            break

    # Make Directory To Save Pics
    RepTxt_Bef = ["/", "\\", ":", "*", "?", "<", ">", "|",'"']
    RepTxt_Aft = ["／", "￦", "：", "＊", "？", "＜", "＞", "｜",'＂']
    for i in range(0,len(RepTxt_Bef)):
        Title = Title.replace(RepTxt_Bef[i], RepTxt_Aft[i])

    MakeDir = str(dir) + "/" + str(Date) + str(Title) + "/"
    print(str(Title) + " Start Download, ", end=" ")
    try:
        os.makedirs(MakeDir)
    except OSError:
        pass

    global loop
    loop = asyncio.get_event_loop()
    Fail_Image = sum(loop.run_until_complete(download_image_host(Piclist, MakeDir)))
    loop.close
    return Title, MakeDir, Fail_Image

# Get Titles Link
def get_titles(driver):
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

        # Click Button "더보기"
        MorebtnElem = driver.find_element_by_id("more_btn")
        GetStyle = MorebtnElem.get_attribute("style")
        if (GetStyle == 'display: none;'):  # if End
            break
        else:
            MorebtnElem.click()

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    group = soup.find_all('ul', {'class': 'lst_feed'})
    return group

# Download Image, with async
async def download_image_host(Piclist, MakeDir):
    Fail_Image = 0
    fts = [asyncio.ensure_future(downImage(Piclist[j], MakeDir, j)) for j in range(0, len(Piclist))]
    Fail_Image = await asyncio.gather(*fts)
    return Fail_Image


# Sub coroutine, download a single image
async def downImage(src, MakeDir, j):
    ErrorLevel = 0
    Fail_Tmp_Image = 0
    SaveDir = MakeDir + str(j) + ".png"
    while True:
        try:
            src = src.get('src')
            request = await loop.run_in_executor(None,requests.get,src)
            with open(SaveDir, 'wb') as file:
                file.write(request.content)
            break
        except:
            print(str(j) + ": Download Fail!")
            ErrorLevel += 1
            sleep(1)
            if (ErrorLevel >= 30):
                Fail_Tmp_Image = 1
                print(str(j) + ": Download Fail, Skip Image")
                break
    return Fail_Tmp_Image



