import requests
import json
import os
import _thread
from .util.help import formatFileName, dumpResp
import traceback
import pathlib

import threading


# change it to ld/sd/hd when choosing the video quality
videoQuality = "sd"


from .Course import Course
def getAllCourses(session, **kwargs):
    # after login get the page
    urlarticles = "https://time.geekbang.org/serv/v1/column/articles"
    articlesData = {"cid": kwargs["courseid"], "size": 200, "prev": 0, "order": "earliest", "sample": "true"}
    articlesheaders = {
        "Referer": "https://time.geekbang.org/course/detail/177-94080",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0)"
    }
    resp = session.post(urlarticles, json=articlesData, headers=articlesheaders)
    dumpResp(resp)
    content = json.loads(resp.text)
    courses = []
    for obj in content["data"]["list"]:
        c = Course()
        c.name = formatFileName(obj["article_title"])
        print("course ------------ ", c.name)
        if obj["article_could_preview"] == True:
            c.accessok = True
            c.video_map = obj["video_media_map"]
            for key in c.video_map.keys():
                print("\t\t video ", key, " url:", c.video_map[key]["url"])
        else:
            c.accessok = False
            print("\t\t !!!Not Accessible")

def downloadAllCourses(session, courses, **kwargs):
    download_path = os.getcwd() + os.sep + "downloadDirHere"
    path = pathlib.Path(download_path)
    if (not path.exists()) or path.is_file():
        os.mkdir(download_path)
    videoQuality = kwargs.get("quality", "sd")
    for c in courses:
        targetfile = download_path + os.sep + c.name + videoQuality + ".mp4"
        if os.path.exists(targetfile):
            print("file already exists, ignore and continue", targetfile)
            continue





def login(**kwargs):
    s = requests.session()
    url = "https://account.geekbang.org/account/ticket/login"
    data = {
        "country": 86,
        "cellphone": kwargs["user"],
        "password": kwargs["pass"],
        "captcha": "",
        "remember": 1,
        "platform": 2,
        "appid": 1
    }
    headers = {"Host": "account.geekbang.org",
               "Referer": "https://account.geekbang.org/login",
               "Connection": "keep-alive"
               }
    resp = s.post(url=url, json=data, headers=headers)
    print("resp login", resp.text, " code", resp.status_code)
    return s


def run(**kwargs):
    s = login(**kwargs)
    courses = getAllCourses(s, **kwargs)
    if kwargs["download"] == True:
        downloadAllCourses(s, courses=courses, **kwargs)

def parse_to_m3u8_links():
    pass

