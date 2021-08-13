import requests
import random

API_URL = 'https://api.scrolller.com/api/v2/graphql'

QUERY = "query SubredditQuery( $url: String! $filter: SubredditPostFilter $iterator: String ) { getSubreddit(url: $url) { children( limit: 50 iterator: $iterator filter: $filter ) { iterator items { mediaSources { url } } } } }"

QUERY_SEARCH = "query SearchQuery($query: String!, $isNsfw: Boolean) { searchSubreddits( query: $query isNsfw: $isNsfw limit: 500 ) { __typename url title secondaryTitle description createdAt isNsfw subscribers isComplete itemCount videoCount pictureCount albumCount isFollowing } }"

def try_search(tag:str, min_picture_count = 20):
    payload = {'authorization':None,
               'query':QUERY_SEARCH,
               'variables':{
                   'isNsfw':True,
                   'query':tag,
                   }
               }
    headers = {'Origin':'https://scrolller.com',
               'Referer':f'https://scrolller.com/discover',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    
    response = requests.post(API_URL,json=payload,headers=headers).json()
    to_return = []
    for item in response['data']['searchSubreddits']:
        if item['itemCount'] >= min_picture_count:
            to_return.append(item['url'].split('/')[-1])
    #if len(response['data']['searchSubreddits'])!=0:
    #    tag_to_return = response['data']['searchSubreddits'][0]['url'].split('/')[-1]
    #else:
    #    tag_to_return = None

    return to_return
    




def get_json_data(tag:str,iterator=None):
    payload = {'authorization':None,
               'query':QUERY,
               'variables':{
                   'filter': None,
                   'url':f'/r/{tag}'
                   
                   }
               }

    if iterator!= None:
        payload['variables']['iterator'] = iterator

    headers = {'Origin':'https://scrolller.com',
               'Referer':f'https://scrolller.com/r/{tag}',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    response = requests.post(API_URL,json=payload,headers=headers).json()

    counter = 0
    if response['data']['getSubreddit']==None\
        or response['data']['getSubreddit']['children']['items'] == []:
        tags = try_search(tag)

    while (response['data']['getSubreddit']==None\
       or response['data']['getSubreddit']['children']['items'] == [])\
            and counter != len(tags):
        if tags == []:
            tags = try_search(tag)
            continue
        else:
            tag = random.choice(tags)
        counter += 1

        payload['variables']['url'] = f'/r/{tag}'
        headers['Referer'] = f'https://scrolller.com/r/{tag}'
        response = requests.post(API_URL,json=payload,headers=headers).json()
        if tag == None:
            raise Exception('Nothing found!')
        #else:
            #response = get_json_data(tag,iterator)
        #counter += 1
    return response


def get_source_urls(data:dict):
    to_return = []
    for item in data['data']['getSubreddit']['children']['items']:
        to_return.append(item['mediaSources'][-1]['url'])
    return to_return

def get_iterator(data:dict):
    return data['data']['getSubreddit']['children']['iterator']


def get_random_photo(tag:str,max_iterations=10,chance=50)->str:
    '''max_iterations = -1:infinit
    chance [1,99]'''
    iterator = None
    get_photos = 100
    photos = list()
    iterations = 0
    while get_photos > 100-chance and iterations <max_iterations:
        data = get_json_data(tag,iterator)
        photos = get_source_urls(data)
        if photos == []:
            iterations += 1
            continue
        iterator = get_iterator(data)
        get_photos = random.randint(1,100)
        iterations += 1

    return random.choice(photos)

if __name__ == '__main__':
    while True:
        photo = get_random_photo('tomboy')
        print(photo)
    
