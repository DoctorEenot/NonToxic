import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0','Alt-Used':'rule34.xxx'}

def search(query:str,next=False):
    urls = []
    referer = None
    if not next:
        referer = f'https://rule34.xxx/index.php?page=post&s=list&tags={query}'
        page = requests.get(referer,headers=headers)
    else:
        referer = query
        page = requests.get(query,headers=headers)
    soup = BeautifulSoup(page.text,'html.parser')
    posts = soup.find_all('span',{'class':'thumb'})
    for post in posts:
        urls.append('https://rule34.xxx/'+post.find('a')['href'])

    next_url_tag = soup.find('a',{'alt':'next'})
    if next_url_tag == None:
        next_url = None
    else:
        next_url = 'https://rule34.xxx/index.php'+next_url_tag['href']
    return (urls,next_url,referer)



def get_content_url(page_url,referer:str):
    headers_request = headers.copy()
    headers_request['Referer'] = referer
    page = requests.get(page_url,headers=headers_request)
    soup = BeautifulSoup(page.text,'html.parser')
    content_url_tag = None
    
    content_url_tag = soup.find('img',{'id':'image'})

    if content_url_tag == None:
        content_url_tag = soup.find('source',{'type':'video/mp4'})
    if content_url_tag == None:
        print(page_url)
        return 'FUCK!'
    content_url = content_url_tag.attrs.get('src',None)

    return content_url







if __name__ == '__main__':
    data = search('tomboy')
    url = get_content_url(data[0][5],data[2])
    data = search(data[1],True)
    print(data)



