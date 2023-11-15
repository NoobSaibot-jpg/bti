import shutil
import re
import pytesseract
from PIL import Image, ImageEnhance
import os


dir = os.getcwd()



tess_path = f'{dir}\\tess\\tesseract.exe'



pattern_fl = r"кв\.?\s*\d+"

pattern_str = r'\b(бул|вул|ква|наб|площ|про|туп|уз|шос)\b'



def read_img(file_name):
    img= Image.open(file_name)
    # enhancer = ImageEnhance.Contrast(img)
    # enhanced_image = enhancer.enhance(2.0)  # Увеличьте контрастность в 2 раза
    # # Сохраните улучшенное изображение
    # enhanced_image.save("enhanced_image.jpg")
    pytesseract.pytesseract.tesseract_cmd = tess_path 
    text= pytesseract.image_to_string(img, lang='ukr')
    list_text=list(text.split('\n'))
    fl = [item for item in list_text if re.search(pattern_fl, item)]
    st = [item for item in list_text if re.search(pattern_str, item)]
    # # return list_text
    return fl, st



print (read_img("photo_1.jpg"))