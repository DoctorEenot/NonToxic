
AMOUNT = 1000

OUTFILE = 'RUS_PHRASES.py'

to_write_data = '# coding=windows-1251\nwords = ['
#  # coding=windows-1251

file = open('russian.txt','r',encoding='windows-1251')

line = file.readline().rstrip('\n').replace("'",'')
to_write_data += "'"+line+"',"
counter = 0
while line and counter<AMOUNT:
    line = file.readline().rstrip('\n').replace("'",'')
    to_write_data += "'"+line+"',"
    counter += 1
    
to_write_data += ']'
file.close()
file = open(OUTFILE,'w',encoding='windows-1251')
file.write(to_write_data)
file.close()
