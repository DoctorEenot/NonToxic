
SPEC_SUMBOLS = ',[]{};+'


def string_parse(script:str,start:int):
    if script[start] == '"':
        starting_offset = start
        while True:
            end = script.find('"',starting_offset+1)
            if script[end-1] != '\\' or (script[end-1] == '\\' and script[end-2] == '\\'):
                break
            else:
                starting_offset = end
    elif script[start] == '\'':
        starting_offset = start
        while True:
            end = script.find("'",starting_offset+1)
            if script[end-1] != '\\' or (script[end-1] == '\\' and script[end-2] == '\\'):
                break
            else:
                starting_offset = end
    return script[start+1:end],end+1

def number_parse(script:str,start:int):
    number = ''
    while True:
        if script[start] not in '0123456789.':
            break
        number += script[start]
        start += 1
    return float(number),start

def parse_boolean(script:str,start:int):
    if script[start] == 'f':
        if script[start:start+5] == 'false' and (script[start+5] in SPEC_SUMBOLS):
            return False, start+5
    elif script[start] == 't':
        if script[start:start+4] == 'true' and (script[start+4] in SPEC_SUMBOLS):
            return False,start+4
    return None

def list_parse(script:str,start:int):
    to_return = []
    start += 1
    while script[start] != ']':
        while script[start] == ' ' or script[start] == '\n' or script[start] == '\t':
            start += 1
        in_var = var_parse(script,start)
        if in_var[1]=='':
            start = in_var[0]
            continue
        to_return.append(in_var[0])
        start = in_var[1]
        while script[start] == ' ' or script[start] == '\n' or script[start] == '\t':
            start += 1
        if script[start] == ',':
            start += 1
    start += 1
    return to_return,start

def dict_parse(script:str,start:str):
    to_return = {}
    start += 1
    while script[start] != '}':
        while script[start] == ' ' or script[start] == '\n' or script[start] == '\t':
            start += 1
        key = string_parse(script,start)
        #to_return[key[0]] = None
        start = key[1]
        while script[start] == ' ' or script[start] == '\n' or script[start] == '\t':
            start += 1
        if script[start] == ':':
            start += 1
        while script[start] == ' ' or script[start] == '\n' or script[start] == '\t':
            start += 1
        data = var_parse(script,start)
        if data[1]=='':
            start = data[0]
            continue
        to_return[key[0]] = data[0]
        start = data[1]
        while script[start] == ' ' or script[start] == '\n' or script[start] == '\t':
            start += 1
        if script[start] == ',':
            start += 1
    start += 1
    return to_return,start

def null_parse(script:str,start:int):
    if script[start] == 'n':
        if script[start:start+4] == 'null' and (script[start+4] in SPEC_SUMBOLS):
            return None,start+4
    return False

def var_parse(script:str,start:int):
    to_return = None
    if script[start] == '[':
        to_return = list_parse(script,start)
    elif script[start] in '0123456789':
        to_return = number_parse(script,start)
    elif script[start] in '\'"':
        to_return = string_parse(script,start)
    elif script[start] == '{':
        to_return = dict_parse(script,start)
    elif script[start] in 'ft':
        to_return = parse_boolean(script,start)
        if to_return == None:
            return None
    elif script[start] == 'n':
        to_return = null_parse(script,start)
        if to_return == False:
            return None
    elif script[start]=='/':
        if script[start+1]=='*':
            start = script.find('*/',start)+2
            to_return=start,''


    return to_return
    
class Executor:
    def __init__(self):
        self.vars = {}
    def get_variable_raw(self,data:str):
        root=''
        query=[]
        start = 0
        while start<len(data):
            if data[start] == '[':
                start+=1
                while data[start] == ' ' or data[start] == '\n' or data[start] == '\t':
                    start += 1
                ret = var_parse(data,start)
                if ret != None:
                    query.append(ret[0])
                    start = ret[1]
            elif data[start] == ']':
                start += 1
            elif data[start] == ' ':
                start+=1
            else:
                root += data[start]
                start += 1
        to_return = self.vars[root]
        for key in query:
            to_return = to_return[key]
        return to_return

    def set_variable_raw(self,data:str,value,plus = False):
        root=''
        query=[]
        start = 0
        while start<len(data):
            if data[start] == '[':
                start+=1
                while data[start] == ' ' or data[start] == '\n' or data[start] == '\t':
                    start += 1
                ret = var_parse(data,start)
                if ret != None:
                    query.append(ret[0])
                    start = ret[1]
            elif data[start] == ']':
                start += 1
            elif data[start] == ' ':
                start+=1
            else:
                root += data[start]
                start += 1
        if len(query) == 0:
            if not plus:
                self.vars[root] = value
            else:
                self.vars[root] += value
            return
        dict_data = self.vars[root]
        lastkey = query[-1]
        for k in query[:-1]:
            if isinstance(k,float):
                dict_data = dict_data[int(k)]
            else:
                dict_data = dict_data[k]
        if not plus:
            dict_data[lastkey] = value
        else:
            dict_data[lastkey] += value
        

    def var(self,script,start,var_name_in=''):
        var_name = var_name_in
        if var_name == '':
            while True:
                if script[start] == ' ':
                    start+=1
                    continue
                elif script[start] == '=' or script[start] == ';':
                    break
                var_name += script[start]
                start += 1
        #self.vars[var_name] = None
        
        to_repeat = False
        if script[start] == '=':
            #if script[start] == '=':
            #    prev = '='
            start += 1
            while True:
                while script[start] == ' ':
                    start += 1
                data = var_parse(script,start)
                if data == None:
                    data = ''
                    while True:
                        if script[start] == ' ':
                            start+=1
                            continue
                        elif script[start] == ';' or script[start] == '+':
                            break
                        data += script[start]
                        start += 1
                    self.set_variable_raw(var_name,self.get_variable_raw(data))
                    break
                    #self.vars[var_name] = self.vars[data]
                elif data[1] == '':
                    start = data[0]
                    #to_repeat = True
                else:
                    self.set_variable_raw(var_name,data[0])
                    start = data[1]
                    break
        elif script[start] == '+':
            start += 1
            while True:
                while script[start] == ' ':
                    start += 1
                data = var_parse(script,start)
                if data == None:
                    data = ''
                    while True:
                        if script[start] == ' ':
                            start+=1
                            continue
                        elif script[start] == ';' or script[start] == '+':
                            break
                        data += script[start]
                        start += 1
                    self.set_variable_raw(var_name,self.get_variable_raw(data),True)
                    break
                    #self.vars[var_name] += self.vars[data]
                elif data[1] == '':
                    start = data[0]
                
                else:
                    self.set_variable_raw(var_name,data[0],True)
                    start = data[1]
                    break
        while True:
            if script[start] == ' ':
                start+=1                
            else:
                break
            
        if script[start] == '+':
            start = self.var(script,start,var_name)
        #elif to_repeat:
        #    start = self.var(script,start,var_name,prev)
        elif script[start] == ';':
            start += 1
        return start

            
    def execute(self,script:str):       
        start = 0
        command = ''
        while start<len(script):
            if script[start] == ' ' or script[start] == '=':
                start += 1
                if command == 'var':
                    start = self.var(script,start)
                    command = ''
                elif command != '':
                    start = self.var(script,start,command)
                    command = ''
                else:
                    start += 1
            elif script[start]=='/' and script[start+1]=='/':
                start = script.find('\n',start)+1
                command = ''
            elif script[start] == '\n' or script[start] == '\t':
                start += 1
                continue
            else:
                command += script[start]
                start += 1
    def clear(self):
        self.vars = {}




