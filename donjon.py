import requests
from bs4 import BeautifulSoup


DUNGEON_GEN_URL = 'https://donjon.bin.sh/d20/dungeon/index.cgi'
DUNGEON_GEN_HEADERS = {'Origin':'https://donjon.bin.sh',
                       'Referer':'https://donjon.bin.sh/d20/dungeon',
                       'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
                       }

HELP_TYPES = {'level':('1-20'),
              'motif':("None","Abandoned","Aberrant","Giant","Undead","Vermin","Aquatic","Desert","Underdark","Arcane","Fire","Cold","Abyssal","Infernal"),
              'seed':('number'),
              'map_style':("Standart","Classic","Crosshatch","GraphPaper","Parchment","Marble","Sandstone","Stale","Aquatic","Infernal","Glacial","Wooden","Asylum","Steampunk","Gamma"),
              'grid':("None","Square","hex","VertHex"),
              'dungeon_layout':("Square","Rectangle","Box","Cross","Dagger","Saltire","Keep","Hexagon","Round","Cavernous"),
              'dungeon_size':("Fine","Diminiutive","Tiny","Small","Medium","Large","Huge","Gargantuan","Colossal","Custom"),
              'colsxrows':("If dungeon_size is Custom"),
              'peripheral_egress':('No','Yes','Many','Tiling'),
              'add_stairs':('No','Yes','Many'),
              'room_layout':('Sparse','Scattered','Dense','Symmetric','Complex'),
              'room_size':("Small","Medium","Large","Huge","Gargantuan","Colossal"),
              'door_set':('None','Basic','Secure','Standart','Deathtrap'),
              'corridor_layout':('Labyrinth','Errant','Straight'),
              'remove_deadends':('None','Some','All')
                }


class Dungeon:
    def __init__(self,name='Dungeon',level='1',motif='',seed=182894729,map_style='Standart',grid='None',dungeon_layout='Square',dungeon_size='Medium',cols=0,rows=0,peripheral_egress='Tiling',add_stairs='Yes',room_layout='Complex',room_size='Huge',door_set='Secure',corridor_layout='Labyrinth',remove_deadends=''):
        self.name = name
        self.level = str(level)
        self.motif = motif
        self.seed = int(seed)
        self.map_style = map_style
        self.grid = grid
        self.dungeon_layout = dungeon_layout
        self.dungeon_size = dungeon_size
        self.cols = cols
        self.rows = rows
        self.peripheral_egress = peripheral_egress
        self.add_stairs = add_stairs
        self.room_layout = room_layout
        self.room_size = room_size
        self.door_set = door_set
        self.corridor_layout = corridor_layout
        self.remove_deadends = remove_deadends
        self.construct = "Construct"
        self.id = None
    def generate(self):
        data = {'name':self.name,
                'level':str(self.level),
                'motif':self.motif,
                'seed':self.seed,
                'map_style':self.map_style,
                'grid':self.grid,
                'dungeon_layout':self.dungeon_layout,
                'dungeon_size':self.dungeon_size,
                'peripheral_egress':self.peripheral_egress,
                'add_stairs':self.add_stairs,
                'room_layout':self.room_layout,
                'room_size':self.room_size,
                'door_set':self.door_set,
                'corridor:layout':self.corridor_layout,
                'remove_deadends':self.remove_deadends,
                'construct':self.construct
                }
        if self.dungeon_size == 'Custom':
            data['map_cols'] = self.cols
            data['map_rows'] = self.rows
        answer = requests.post(DUNGEON_GEN_URL,data=data,headers=DUNGEON_GEN_HEADERS)
        soup = BeautifulSoup(answer.text,'html.parser')

        img_link = 'https://donjon.bin.sh'+soup.find('img',{'id':'map_img'})['src']

        self.id = (img_link.split('/')[-1]).replace('.png','')
        
        return img_link

    def get_html(self):
        headers = {'Referer':'https://donjon.bin.sh/d20/dungeon/index.cgi',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
                       }
        data = requests.post(f'https://donjon.bin.sh/fantasy/dungeon/lib/html.cgi',data = {'cache_id':self.id},headers=DUNGEON_GEN_HEADERS) 
        return 'https://donjon.bin.sh'+data.json()['uri']
    def get_player_map(self):
        headers = {'Referer':'https://donjon.bin.sh/d20/dungeon/index.cgi',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
                       }
        data = requests.post(f'https://donjon.bin.sh/fantasy/dungeon/lib/player.cgi',data = {'cache_id':self.id},headers=DUNGEON_GEN_HEADERS)
        return 'https://donjon.bin.sh'+data.json()['uri']
    def get_print_map(self):
        headers = {'Referer':'https://donjon.bin.sh/d20/dungeon/index.cgi',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
                       }
        data = requests.post(f'https://donjon.bin.sh/fantasy/dungeon/lib/print.cgi',data = {'cache_id':self.id},headers=DUNGEON_GEN_HEADERS)
        return 'https://donjon.bin.sh'+data.json()['uri']
    def get_text_map(self):
        headers = {'Referer':'https://donjon.bin.sh/d20/dungeon/index.cgi',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
                       }
        data = requests.post(f'https://donjon.bin.sh/fantasy/dungeon/lib/text.cgi',data = {'cache_id':self.id},headers=DUNGEON_GEN_HEADERS)
        return 'https://donjon.bin.sh'+data.json()['uri']
    








if __name__ == '__main__':
    #map = Dungeon()
    #data = map.generate()
    #url = map.get_html()
    #data = map.get_player_map()
    #data = map.get_print_map()
    #data = map.get_text_map()
    print()
