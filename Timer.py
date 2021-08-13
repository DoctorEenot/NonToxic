import time
import random


pre_ten_insults = ['https://www.google.com/url?sa=i&url=https%3A%2F%2Fprodota.ru%2Fforum%2Fprofile%2F179146%2Fcontent%2F%3Ftype%3Dcore_statuses_status%26change_section%3D1&psig=AOvVaw31-jXUtrpw7QDF6FXkPoFT&ust=1610721016255000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIDV_cPRm-4CFQAAAAAdAAAAABAD',
                   '10 минут и поднимаю скайнет на зачистку',
                   'Через 10 минут у меня в кабинете и не минутой позже!',
                   'cock and ball torture начинается через 10 минут',
                   'Часики-то тикают, и тикают, что осталось 10 минут',
                   'Я говорил с временем, время сказало, что осталось 10 минут',
                   'АЛО НАХУЙ, МЕНЯ СЛЫШНО!? осталось 10 минут']

end_insults = ['Ну все нахуй, время вышло',
               'На сервер быстро!',
               'Все пиздец, часики оттикали',
               'Если Магомед не идет к горе, то гора разносит Магомеду ебало нахуй',
               'Не дай бог не увижу сегодня сервере, заебу оповещениями',
               'Ехал Грека через реку и обосрался нахуй, потому что не успел',
               'Мне долго еще повторять? НА СЕРВЕР ЖИВО!',
               'Так, ну и где блять? Я нахер трачу свое процессорное время?']



class Timer:
    def __init__(self,time_delta:int,channel,mentions:list):
        self.start_time = time.time()
        self.end_time = self.start_time+time_delta
        self.delta = time_delta
        self.channel = channel
        self.mentions = mentions
        self.ten_passed=False
    def check(self):
        
        if time.time()-self.start_time >= self.delta:
            return True,random.choice(end_insults)
        elif self.end_time - time.time() >= 530 and self.end_time - time.time()<=630 and not self.ten_passed:  
            self.ten_passed = True
            return False,random.choice(pre_ten_insults)
        else:
            return False,False
