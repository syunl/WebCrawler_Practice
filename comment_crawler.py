import pymongo 
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymysql
import re


def filter_emoji(desstr,restr=''):    
    try:  
        co = re.compile(u'[\U00010000-\U0010ffff]')  
    except re.error:  
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')  
    return co.sub(restr, desstr)  

#get deta from mongodb
cluster = MongoClient('mongodb+srv://crawler:!QAZ2wsx@cluster0.k1oua.mongodb.net/wear?retryWrites=true&w=majority')
db = cluster['wear']
collection = db['Mondel_W']
results = collection.find({'Mondel_Rank': '16'}) #62,88
feature = []

for result in results: 
    for sets in result['SET']:
        feature.append(sets["Set_Url"])

# web crwaler
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
'Referer': 'https://wear.tw/ranking/user/'
}

commentInsert = []
for outfiturl in feature:
    url = outfiturl
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    Nocomment = soup.find('p', class_='no_comment')
    historyComment = soup.find('p', id = 'history_comment')
    if Nocomment != None:
        commentInsert.append([outfiturl.split('/')[-3] + "_" + outfiturl.split('/')[-2],'NO COMMENT','NO COMMENT'])
    elif historyComment == None:
        commentContainer = soup.find('div', class_ = 'comment_container')
        comment = commentContainer.find_all('p',class_ = 'txt')
        userId = commentContainer.find_all('span',class_ = 'userid')
        for c, u in zip(comment,userId):
            commentInsert.append([outfiturl.split('/')[-3] + "_" + outfiturl.split('/')[-2], filter_emoji(c.text), u.text.split('@')[-1]])
        
    else:
        driverPath = 'C:\geckodriver\geckodriver.exe'
        browser = webdriver.Firefox(executable_path=driverPath)
        browser.get(url)
        eleLink = browser.find_element_by_id('history_comment')
        eleLink.click()
        # time.sleep(2)
        commentContainer = browser.find_element_by_class_name('comment_container')
        comment = commentContainer.find_elements_by_class_name('txt')
        userId = commentContainer.find_elements_by_class_name('userid') 
        for c, u in zip(comment,userId):
            commentInsert.append([outfiturl.split('/')[-3] + "_" + outfiturl.split('/')[-2], filter_emoji(c.text), u.text.split('@')[-1]])
  
#Insert to MySQL
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "wear",
    "charset": "utf8"
}

command = ''
try:
# 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        for c in commentInsert:
            try:
                command = f'INSERT INTO usercomment(OutfitId, UserComment, UserCommentId)VALUES("{c[0]}", "{c[1]}", "{c[2]}");'
                cursor.execute(command)
            except Exception as ex:
                print(ex)
                print(command)
            print('down')
    
        # 儲存變更
        conn.commit()
    
except Exception as ex:
    print(ex)
    print(command)