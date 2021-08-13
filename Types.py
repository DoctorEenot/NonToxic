import requests
from bs4 import BeautifulSoup
import json
import JSExecutor
import random
import time
import captcha

MAIN_URL = 'https://www.pornhub.com'
RECOMMENDED_PATH = '/recommended'

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}


class Thumbnails:
    def __init__(self,url_pattern:str):
        self.max_thumbnails = 0
        url_pattern = url_pattern.replace('\\','')
        left_offset = url_pattern.find('{')
        right_offset = url_pattern.find('}',left_offset)
        try:
            self.max_thumbnails =int(url_pattern[left_offset+1:right_offset])
        except:
            self.max_thumbnails = 0
        self.url_pattern = url_pattern[:left_offset+1]+url_pattern[right_offset:]
    def get_thumbnail(self,number:int):
        if number>self.max_thumbnails:
            number = self.max_thumbnails
        return self.url_pattern.format(number)


class Video:
    def __init__(self,url,title=''):
        self.url = url.replace('https://www.pornhub.com','')
        self.url = self.url.replace('https://rt.pornhub.com','')
        self.title = title
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        if self.title == '':
            self.get_title()
        self.id = self.url[self.url.find('=')+1:]
        self.thumb = ''
        self.thumbnails = None
        self.js = JSExecutor.Executor()
    def get_file_urls(self):       
        page = self.session.get(MAIN_URL+self.url)
        soup = BeautifulSoup(page.text,'html.parser')
        player = soup.find('div',{'id':'player'})
        if player == None:
            captcha.get_cookie(page.text)
            #file = open('ph_vid.html','w',encoding='utf-8')
            #file.write(page.text)
            #file.close()
        else:
            print('found player')
        #js = JSExecutor.Executor()
        self.js.clear()
        script = player.find('script').text
        self.js.execute(script)

        flashvars = ''
        for key in self.js.vars.keys():
            if 'flashvars_' in key:
                flashvars = key
                break

        self.thumb = self.js.vars[flashvars]['image_url'].replace('\\','')
        self.thumbnails = Thumbnails(self.js.vars[flashvars]['thumbs']['urlPattern'])

        video_url = ''
        for item in self.js.vars[flashvars]['mediaDefinitions']:
            if item['format'] == 'mp4':
                video_url = item['videoUrl']
        data = self.session.get(video_url)
        print(data)
        return data.json()
    def get_best_quality(self): 
        
        data = self.get_file_urls()
        return data[-1]['videoUrl']
    def get_title(self):
        page = self.session.get(MAIN_URL+self.url)
        soup = BeautifulSoup(page.text,'html.parser')
        video_wrapper = soup.find('div',{'class':'video-wrapper'})
        title  = video_wrapper.find('h1',{'class':'title'}).find('span').text
        self.title = title
        return self.title
