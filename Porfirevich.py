import requests
import random
import RUS_PHRASES

phrases = []

def populate_phrases(n=200):
    for i in range(n):
        string_to_append = ''
        for a in range(2):
            string_to_append += random.choice(RUS_PHRASES.words)+' '
        phrases.append(string_to_append)
populate_phrases()
            
async def get_reply(prompt=None, rec=3):
    if prompt == None:
        prompt = random.choice(phrases)
    data = requests.post('https://pelevin.gpt.dobro.ai/generate/',
                            json={'length':60,'prompt':prompt})
    if rec == 0:
        return prompt + random.choice(data.json()['replies'])
    else:
        return await get_reply(prompt + random.choice(data.json()['replies']),rec-1)
    
    
    
    
if __name__ == '__main__':
    reply = get_reply()
    print(reply)
    input()