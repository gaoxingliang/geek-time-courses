import requests
import json
import os
from .util.help import formatFileName, dumpResp
import pathlib
from .util.fileop import multi_thread_download


# change it to ld/sd/hd when choosing the video quality
videoQuality = "sd"

from .Course import Course


def getAllCourses(session, **kwargs):
    # after login get the page
    urlarticles = "https://time.geekbang.org/serv/v1/column/articles"
    courseid = kwargs["courseid"]
    articlesData = {"cid": courseid, "size": 500, "prev": 0, "order": "earliest", "sample": False}
    articlesHeaders = {
        "Referer": "https://time.geekbang.org/course/intro/" + courseid,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0)",
        "Content-Type": "application/json"
    }
    resp = session.post(urlarticles, json=articlesData, headers=articlesHeaders)
    dumpResp(resp)
    content = json.loads(resp.text)
    courses = []
    for obj in content["data"]["list"]:
        c = Course()
        courses.append(c)
        c.name = formatFileName(obj["article_title"])
        print("[course] ------------ ", c.name)
        if obj["article_could_preview"] == True:
            c.accessok = True
            if "video_media_map" in obj:
                c.video_map = obj["video_media_map"]
                for key in c.video_map.keys():
                    print("\t\t video ", key, " url:", c.video_map[key]["url"])
            else:
                print("\t\t No video for this course, it's maybe a page.")
        else:
            c.accessok = False
            print("\t\t !!!Not Accessible")
    return courses


def downloadAllCourses(session, courses, **kwargs):
    download_path = os.getcwd() + os.sep + "downloadDirHere_" + kwargs.get("courseid")
    path = pathlib.Path(download_path)
    if (not path.exists()) or path.is_file():
        os.makedirs(download_path)
    multi_thread_download(session, courses, path, **kwargs)


def login(**kwargs):
    s = requests.session()
    if "user" in kwargs and "pass" in kwargs:
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
    else:
        print("No user and pass is set (try with -U and -P options), not login")
    return s


def run(**kwargs):
    s = login(**kwargs)
    courses = getAllCourses(s, **kwargs)
    if kwargs.get("download", False):
        downloadAllCourses(s, courses=courses, **kwargs)
