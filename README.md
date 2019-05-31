# geek-time-courses
Geektime courses/极客时间  https://time.geekbang.org/ sharing course repo<br>
Username or passwords will <font color="red"><b>NOT</b></font> be collected.<br>

The below functions are provided:
1. sharing some courses videos and pdfs.
2. provide a tool to parse and download videos.

Now provided:

 1. [QCon 2019 beijing video and ppt](courses/QCon2019Beijing/README.md) <br>
 2. [nginx核心知识100讲](courses/nginx/README.md)

# how to download geektime videos
clone this repo and run with:
```
python3 geektime.py https://time.geekbang.org/course/intro/181
```

Download videos for a course:
```
python3 -d geektime.py https://time.geekbang.org/course/intro/181
# run this when you have bought a class to see ALL courses:
python3 -U yourCellphone -P yourPassword -d geektime.py https://time.geekbang.org/course/intro/181
```

Only get download urls for a course:
```
python3 -p geektime.py https://time.geekbang.org/course/intro/181
```
other helps just run:
```
python3 geektime.py
```

# How to contribute to share more courses
If you have ever bought/subscribed an video course: <br>
run below code to share the m3u8 files and you can download it and share it by a PULL request or an issue :
```
python3 -U yourCellphone -P yourPassword -d geektime.py https://time.geekbang.org/course/intro/181
```
or not downloading and just providing the urls:
```
python3 -U yourCellphone -P yourPassword -p geektime.py https://time.geekbang.org/course/intro/181
```
Note: NO passwords will be collected. check our source code.  Thanks for your SHARING.

