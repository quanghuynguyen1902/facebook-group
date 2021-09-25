import re
import requests
import os

text = "M.n nộp đơn xin việc ntn vậy ạ? Em là sinh viên mới ra trường mà nộp hồ sơ vô cty nào cũng toàn làm công nhân không à!😢😭\n\nỦa em chỉ muốn làm nhân viên văn phòng bình thường thôi, sao mấy anh chị châm biếm em dữ vậy? Em thấy cty thông báo tuyển thì em nộp đơn chứ em có biết tốt nghiệp làm công nhân đâu, thậm chí anh phỏng vấn cũng nói là vô sẽ có người sắp xếp công việc cho em nên em mới vô mà!! 🙏🏻"

import re


def remove_emojis(data):
    data = data.strip()
    data = data.replace("#BTDDL", "#CAGT-KLNV")
    emoj = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoj, "", data)


def download_image(name, url):
    response = requests.get(url)
    file = open("./image/" + name, "wb")
    file.write(response.content)
    file.close()
