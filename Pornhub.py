import requests
from bs4 import BeautifulSoup
import json
import base64
import random
import time
import captcha
from Types import Video

MAIN_URL = 'https://www.pornhub.com'
RECOMMENDED_PATH = '/recommended'

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}








class API:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    def videos(self,search,page=1,production='all',c=-1,min_duration=0,max_duration=0,hd=False):
        '''
        c - category(int)
        production - all/professional/homemade
        hd - True/False
        '''
        to_return = []
        url = MAIN_URL +f'/video/search?search={search}'
        if page>1:
            url += f'&page={page}'
        if production == 'professional' or production=='homemade':
            url += f'&p={production}'
        if c>=0:
            url += f'&c={c}'
        if min_duration>0:
            url += f'&min_duration={min_duration}'
        if max_duration>0:
            url += f'&max_duration={max_duration}'
        if hd:
            url += '&hd=1'

        page_html = self.session.get(url)
        if page_html.status_code!= 200:
            return None
       
        soup = BeautifulSoup(page_html.text,'html.parser')
        videos_block = soup.find('ul',{'id':'videoSearchResult'})
        if videos_block == None:
            nothing_found = soup.find('div',{'class':'noResultsWrapper'})
            if nothing_found != None:
                return None
            captcha.get_cookie(page_html.text)
            return None
        spans = videos_block.findChildren('span',{'class':'title'})
        for span in spans:
            a = span.find('a')
            to_return.append(Video(a['href'],a['title']))
        return to_return

    def get_random_video(self,search,max=25,production='all',c=-1,min_duration=0,max_duration=0,hd=False):
        random_page_number = random.randint(1,max)
        videos = self.videos(search,random_page_number,production,c,min_duration,max_duration,hd)
        while videos == None or max > 0:
            max = max//2
            if max <= 0:
                break
            random_page_number = random.randint(1,max)
            videos = self.videos(search,random_page_number,production,c,min_duration,max_duration,hd)
        #if videos == None:
        #    for i in range(random_page_number,0,-1):
        #        videos = self.videos(search,i,production,c,min_duration,max_duration,hd)
                
        #        if videos != None and videos != []:
        #            break
                #time.sleep(1)
        if videos == None or len(videos) == 0:
            return False
        return random.choice(videos)


if __name__ == '__main__':
    api = API()
    #videos = api.videos('cute',page=1)
    #url = videos[0].get_best_quality()
    while True:
        #video = api.get_random_video('cute tomboy')
        #url = video.get_best_quality()
        vid = Video('https://www.pornhub.com/view_video.php?viewkey=662397712')
        vid.get_best_quality()
        print(url)

