import js2py

def get_cookie(script:str):
    file = open('file.html','w',encoding='utf-8')
    file.write(script)
    file.close()
    script = script.replace('<html><head><script type="text/javascript"><!--','')
    end = script.find('<body onload="go()">')
    cookies_string = script.find('document.cookie=')
    reload_string = script.find('document.location.reload(true);',cookies_string+len('document.cookie='))
    new_script = script[:cookies_string]+' return '+script[cookies_string+len('document.cookie='):reload_string]+script[reload_string+len('document.location.reload(true);'):end]
    try:
        res = js2py.eval_js(script)
    except:
        return None
    print(res)






