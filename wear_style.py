import requests
from bs4 import BeautifulSoup
import csv
import random,time
import json
import pandas as pd
import os

def style_pic(styleName,tag_ids):
    if os.path.exists('./wear') == False:
        os.mkdir('./wear')
    if os.path.exists('./wear/training_set') == False:
        os.mkdir('./wear/training_set')
    if os.path.exists('./wear/test_set') == False:
        os.mkdir('./wear/test_set')
    if os.path.exists(f'./wear/training_set/{styleName}') == False:
        os.mkdir(f'./wear/training_set/{styleName}')
    if os.path.exists(f'./wear/test_set/{styleName}') == False:
        os.mkdir(f'./wear/test_set/{styleName}')
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    'Referer': 'https://wear.tw/ranking/user/'
    }
    for page in range(1,97):
        url = f'https://wear.jp/women-coordinate/?tag_ids={tag_ids}&suggest_flag=1&pageno={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        like_mark = soup.find_all('li', class_='like_mark')
        for w in like_mark:
            imgUrl = 'https:' + w.find('img').get('data-originalretina')
            print(imgUrl)
            imgPath = f'./wear/training_set/{styleName}/' + imgUrl.split('/')[-1]
            try:
                resImg = requests.get(imgUrl, headers=headers)
                with open(imgPath, 'wb') as f:
                    f.write(resImg.content)
                print('done')
            except:
                print('error')    

    for page in range(97,121):
        url = f'https://wear.jp/women-coordinate/?tag_ids={tag_ids}&suggest_flag=1&pageno={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        like_mark = soup.find_all('li', class_='like_mark')
        for w in like_mark:
            imgUrl = 'https:' + w.find('img').get('data-originalretina')
            print(imgUrl)
            imgPath = f'./wear/test_set/{styleName}/' + imgUrl.split('/')[-1]
            try:
                resImg = requests.get(imgUrl, headers=headers)
                with open(imgPath, 'wb') as f:
                    f.write(resImg.content)
                print('done')
            except:
                print('error')    


style_pic('feminine','4047')