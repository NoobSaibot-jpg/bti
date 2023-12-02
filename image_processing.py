import PIL.Image
import pytesseract
import re
import os

dir = os.getcwd()
def str_type(str):
    if str == 'бул':
        return 8
    elif str == 'вул':
        return 1
    elif str == 'кв':
        return 9
    elif str == 'наб':
        return 10
    elif str == 'пл':
        return 4
    elif str == 'пров':
        return 2
    elif str == 'туп':
        return 7
    elif str == 'уз':
        return 6
    elif str == 'шос':
        return 11
    elif str == 'пр-кт':
        return 3
    elif str == 'проїзд':
        return 5


def read_img(file_name):
    pattern_fl = r"кв\.?\s*\d+"
    pattern_str = r'\b(бул|вул|кв|наб|пл|пров|туп|уз|шос|пр-кт)\b'
    img = PIL.Image.open(file_name)
    pytesseract.pytesseract.tesseract_cmd = f'{dir}\\tess\\tesseract.exe'
    text = pytesseract.image_to_string(img, lang='ukr')
    list_text = list(text.split('\n'))
    fl = [item for item in list_text if re.search(pattern_fl, item)]
    st = [item for item in list_text if re.search(pattern_str, item)]
    if len(st) == 0 or len(st) > 8 or len(fl) == 0:  # Проверяем наличие значений
        return None, None  # Возвращаем None, если данных для распаковки недостаточно
    else:
        box = str(fl[0])  # Берем первый элемент списка fl
        b_index = box.find('.')
        cut_box = box[b_index:-2].strip('.')
        st_text = str(st[0])  # Берем первый элемент списка st
        st_index = st_text.find('.')
        cut_str = str_type(st_text[2:st_index:].strip('.'))
        return cut_box, str_type(cut_str)
    

