import os
import re
import pytesseract
from PIL import Image as PILImage
from rich.console import Console


class ImgText:
    def __init__(self, filename):
        self.filename = filename
        self.tess_path = f"{os.getcwd()}\\tess\\tesseract.exe"
        self.pattern_str = r"\b(бул|вул|ква|наб|пл|пров|туп|уз|шос|пр-кт)\b"
        self.pattern_fl = r"кв\.?\s*\d+"

    def get_text(self):
        img = PILImage.open(self.filename)
        pytesseract.pytesseract.tesseract_cmd = self.tess_path
        text = pytesseract.image_to_string(img, lang="ukr")
        list_text = list(text.split("\n"))
        return list_text

    def get_box(self):
        fl = [item for item in self.get_text() if re.search(self.pattern_fl, item)]
        if fl != []:
            box = fl[0]
            b_index = box.find(".")
            nbox = box[b_index:].strip(".")
            return nbox
        else:
            return []

    def get_strtype(self):
        st = [item for item in self.get_text() if re.search(self.pattern_str, item)]
        if st != []:
            t_st = st[0]
            st_index = t_st.find(".")
            t_str = t_st[:st_index].strip(".")
            return t_str
        else:
            return []

    def get_strtype_id(self):
        if self.get_strtype() == "бул":
            return 8
        elif self.get_strtype() == "вул":
            return 1
        elif self.get_strtype() == "кв":
            return 9
        elif self.get_strtype() == "наб":
            return 10
        elif self.get_strtype() == "пл":
            return 4
        elif self.get_strtype() == "пров":
            return 2
        elif self.get_strtype() == "туп":
            return 7
        elif self.get_strtype() == "уз":
            return 6
        elif self.get_strtype() == "шос":
            return 11
        elif self.get_strtype() == "пр-кт":
            return 3
        elif self.get_strtype() == "проїзд":
            return 5
