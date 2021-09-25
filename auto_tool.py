import requests
import os
from dotenv import load_dotenv
from dateutil import parser
import pytz
from datetime import datetime as dt, timedelta, date
import time
import traceback
import sys
import datetime


from fb import post_fb, login_fb
from discord_bot import send_message
from error_fb import map_code_error, log_error


class AutoTool:
    def __init__(self):
        self.start_time = ""
        self.end_time = ""
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
        """
        Crawl 5 posts of group "Biet the deo di lam"
        """

        url = f"{self.default_fb}/{self.group_id}?fields=feed.limit({self.number_post})&access_token={self.access_token}"

        group_posts = requests.get(url).json()

        log_error(map_code_error, group_posts)

        if len(group_posts["feed"]["data"]) == 0:
            raise ValueError("Not found posts")

        self.crawl_datas = group_posts["feed"]["data"]

    def get_start_and_end(self):

        VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")
        ago = dt.now(VN_TZ) - timedelta(1)
        self.start_time = ago.replace(hour=0, minute=0, second=0, microsecond=0)
        self.end_time = self.start_time + timedelta(1)

    def filter_posts(self):
        """
        filter matching posts
        """

        VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")

        for data in self.crawl_datas:
            created_time = parser.parse(
                parser.parse(data["created_time"]).astimezone(VN_TZ).isoformat()
            )

            if created_time > self.start_time and created_time < self.end_time:
                self.filter_datas.append(data)

        if len(self.filter_datas) == 0:
            raise ValueError("Not found valid posts")

    def get_datas(self):
        """
        get message and 1 image of posts
        """

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

        """
        post datas to group "Com ao gao tien - kiep lam nhan vien
        """

        # for data in self.datas:
        params = {
            "url": "https://i.ytimg.com/vi/lCxDAprbFx8/hqdefault.jpg",
            "message": "dich nay chan qua",
            "access_token": self.access_token,
        }
        url = f"{self.default_fb}/{self.my_group_id}/photos"
        response = requests.post(url, params=params).json()
        log_error(map_code_error, response)


def main():
    try:
        account = {
            "gmail": "dkingsama2000@gmail.com",
            "password": "skjfieurndasfier234@",
        }

        driver = login_fb(account)

        crawl = AutoTool()
        crawl.load_env()

        while True:
            crawl.crawl_posts()
            crawl.get_start_and_end()
            crawl.filter_posts()
            crawl.get_datas()

            post_fb(driver, crawl.datas)

            if len(sys.argv) > 1:
                send_message("Post status successfully")

            else:
                print("Post status successfully")

            time.sleep(86400)

    except Exception as e:
        if len(sys.argv) > 1:
            send_message(
                f"<@861984704084181012> error: {e} \n Traceback: {traceback.format_exc()}"
            )
        else:
            print(f"error: {e} \n Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
