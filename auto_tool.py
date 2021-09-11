import requests
import os
from dotenv import load_dotenv
from dateutil import parser
import pytz
from datetime import datetime as dt
import traceback
import sys
import datetime
from fb import post_fb
from error_fb import map_code_error, log_error


class AutoTool:
    def __init__(self):
        self.number_post = ""
        self.group_id = ""
        self.access_token = ""
        self.page_token = ""
        self.my_group_id = ""
        self.crawl_datas = []
        self.filter_datas = []
        self.datas = []
        self.default_fb = "https://graph.facebook.com"

    def load_env(self):

        load_dotenv()
        self.access_token = os.getenv("access_token")
        self.group_id = os.getenv("group_id")
        self.my_group_id = os.getenv("my_group_id")
        self.number_post = os.getenv("number_post")

        if self.access_token == "" or self.group_id == "":
            raise ValueError("Error when load env file")

    def crawl_posts(self):
        '''
            Crawl 5 posts of group "Biet the deo di lam"
        '''

        url = f"{self.default_fb}/{self.group_id}?fields=feed.limit({self.number_post})&access_token={self.access_token}"

        group_posts = requests.get(url).json()

        log_error(map_code_error, group_posts)

        if len(group_posts["feed"]["data"]) == 0:
            raise ValueError("Not found posts")

        self.crawl_datas = group_posts["feed"]["data"]

    def filter_posts(self):
        '''
            filter matching posts 
        '''

        VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")

        # get today's date
        time_now = dt.now(VN_TZ)
        time_ago = dt.now(VN_TZ) - datetime.timedelta(minutes=360)

        for data in self.crawl_datas:
            created_time = parser.parse(
                parser.parse(data["updated_time"]).astimezone(VN_TZ).isoformat()
            )

            if created_time >= time_ago and created_time <= time_now:
                self.filter_datas.append(data)

        if len(self.filter_datas) == 0:
            raise ValueError("Not found valid posts")

    def get_datas(self):
        '''
            get message and 1 image of posts 
        '''

        option = "fields=message,full_picture"

        for data in self.filter_datas:

            # if "picture" in data:
            url = f"{self.default_fb}/{data['id']}?{option}&access_token={self.access_token}"

            post = requests.get(url).json()

            log_error(map_code_error, post)

            self.datas.append(post)

        if len(self.datas) == 0:
            raise ValueError("Not found posts with image")

    def post_group(self):

        '''
            post datas to group "Com ao gao tien - kiep lam nhan vien
        '''
        
        # for data in self.datas:
        params = {
            "url": "https://i.ytimg.com/vi/lCxDAprbFx8/hqdefault.jpg",
            "message": "dich nay chan qua",
            "access_token": self.access_token,
        }
        url = f"{self.default_fb}/{self.my_group_id}/photos"
        response = requests.post(url, params=params).json()
        log_error(map_code_error, response)

try:
    account = {"gmail": "taolasieunhansylas@gmail.com", "password": "asdfjkieurnakf934@"}
    crawl = AutoTool()
    crawl.load_env()
    crawl.crawl_posts()
    crawl.filter_posts()
    crawl.get_datas()
    for content in crawl.datas:
        post_fb(account, content)

except Exception as e:
    print(f"Traceback: {traceback.format_exc()}")