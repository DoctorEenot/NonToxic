from PIL import Image, ExifTags
from discord import File
from PIL import ImageFont
from PIL import ImageDraw 
import io
import random



def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode,
                      (new_width, new_height),
                        color)
    result.paste(pil_img, (left, top))
    return result

PHRASES = (u'Ультра хохол', u'Вообще псих',u"Ну что за гондон",
           u"Пидоры повсюду", u"Ну пиздец",u"Навернул пельменей",
           u"Перднул с подливой",u"Че делаешь?",u"Блять.",
           u"Бывает же",u"Убил маму",u"Героям слава!",
           u"Невменяемый хуй",u"навернул говна",u"Ебучая тушенка",
           u"Свердловсая область",u"Герой Украины",u"Путин пидор",
           u"Мать жива?",u"Не шути так",u"Еблан.",u"Пидорасы",
           u"Консерва",u"Рыбный фарш",u"Мать казнить",
           u"Убийца жизни",u"ПОСОСИ",u"Ты ебанутый?",
           u"Подмосковье",u"Запорожье",u"Киев",u"Сучара",
           u"Четкий поц",u"Коклошвайн",u"Гаврил.",u"Герой страны",
           u"Продал мать",u"Купил мать",u"Продавец говна",
           u"Запомните пидораса","Забыл умереть","Оформил вкид",
           "2 дня в качалке","Убил жену","Ебучий швед",
           "Бельгийцы...","Бешеный хуила","Заводной мудила",
           "И такое бывает","Хохол ебучий","Хохол опасный",
           "Куда сосать?","Платно","Бесплатно",
           "Шайба","Ну ахуеть","Че он творит",
           "Сралин","Вкинул знатно","На страже вкида",
           "Воскресил маму","Вкинул пак","Российский Иван",
           "Тян не нужны","Похоронил маму","Вообще похуй",
           "где блять?","Покупатель говна")

LAST_5_PHRASES = []


def generate_prikol(original:bytes):
    image = Image.open(io.BytesIO(original))

    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break

    try:
        exif=dict(image._getexif().items())

        if exif[orientation] == 3: 
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6: 
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8: 
            image=image.rotate(90, expand=True)
    except:
        pass

    image.thumbnail((450,450), Image.ANTIALIAS)
    image = add_margin(image,30,80,120,80,(0,0,0))
    width, height = image.size

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("DejaVuSans.ttf", 30)
    
    text = random.choice(PHRASES)
    while text in LAST_5_PHRASES:
        text = random.choice(PHRASES)

    if len(LAST_5_PHRASES)<5:
        LAST_5_PHRASES.append(text)
    else:
        LAST_5_PHRASES.pop(0)
        LAST_5_PHRASES.append(text)

    #w, h = draw.textsize(text)

    draw.text(((width-(len(text)*15))/2, height-(120-24)),text,(255,255,255),font=font)

    to_return = io.BytesIO()
    image.save(to_return,format='PNG')
    to_return.seek(0)
    return File(to_return,'smeisya_padla.png')
    #image.show()


