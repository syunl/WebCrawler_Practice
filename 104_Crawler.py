import requests
from bs4 import BeautifulSoup
import csv
import random,time
import json
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
}
page=0  
url=f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=python&area=6001001000%2C6001002000&order=15&asc=0&page={page}&mode=s&jobsource=2018indexpoc'

all_job_links=[]
for page in range(1,5):
    htmlFile = requests.get(url, headers=headers)
    ObjSoup=BeautifulSoup(htmlFile.text,'lxml')
    jobs = ObjSoup.find_all('article',class_='js-job-item')                 #搜尋所有職缺  
    # time.sleep(random.randint(1,3))
    for job in jobs:
        job_url=job.find('a').get('href')                                   #網址
        job_url1 = job_url.split('?')[0]
        job_url2 = job_url1. split('/')[-1]
        all_job_links.append(job_url2)
firmList = list()
jobVacancy = list()
jobDescList = list()
pythonList = list()
MySQLList = list()
LinuxList =list()
JavaList=list()
JavaScriptList=list()
for i in all_job_links:
    url = f'https://www.104.com.tw/job/ajax/content/{i}'
    urlReferer = f'https://www.104.com.tw/job/{i}?jobsource=2018indexpoc'
    headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
        'Referer':urlReferer
    }
    res = requests.get(url, headers=headers)
    jsonData = json.loads(res.text)  
    
    firm = jsonData['data']['header']['custName']
    firmList.append(firm)
    jv = jsonData['data']['header']['jobName']
    jobVacancy.append(jv)    
    jobDesc = jsonData['data']['jobDetail']['jobDescription']
    jobDescList.append(jobDesc)
    skillList=list()
    for skillSet in jsonData['data']['condition']['specialty']:
        skill = skillSet['description']
        skillList.append(skill)

    if 'Python' in skillList:
        pythonList.append('1')
    else :
        pythonList.append('0')

    if 'MySQL' in skillList:
        MySQLList.append('1')
    else :
        MySQLList.append('0')

    if 'Linux' in skillList:
        LinuxList.append('1')
    else :
        LinuxList.append('0') 

    if 'Java' in skillList:
        JavaList.append('1')
    else :
        JavaList.append('0')      
    if 'JavaScript' in skillList:
        JavaScriptList.append('1')
    else :
        JavaScriptList.append('0')         
    jobData=pd.DataFrame({
        "公司名":firmList,
        "職缺名":jobVacancy,
        "工作內容":jobDescList,
        "python":pythonList,
        "MySQL":MySQLList,
        "Linux":LinuxList,
        "Java":JavaList,
        "JavaScript":JavaScriptList
    })

    jobData.to_csv('./104_JobVacancy.csv', index=False, encoding='utf-8-sig')