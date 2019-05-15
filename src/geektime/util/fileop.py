import os
import pathlib
import traceback
from src.geektime.util.CountDownLatch import  CountDownLatch
import _thread
import shutil

def downloadfile(session, url, targetfilename, latch):
    # targetfilename is an absolutepath
    try:
        all_content = session.get(url).text
        file_line = all_content.split("\n")
        if file_line[0] != "#EXTM3U":
            print("Not a ext file", file_line[0])
            latch.count_down()
        else:
            # this is a file
            path = pathlib.Path(targetfilename)
            if path.exists() and path.is_file():
                os.remove(targetfilename)

            # make a tempdir
            tempdir = targetfilename + "_temp"
            if not os.path.exists(tempdir):
                os.makedirs(tempdir)

            partfiles = []
            for index, line in enumerate(file_line):
                if "EXTINF" in line:
                    # 拼出ts片段的URL
                    pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]
                    print("\t downloading - ", pd_url[-10:])
                    partfile = tempdir + "/part" + str(index)
                    partrecordfile = partfile + ".ok"
                    partfiles.append(partfile)
                    if os.path.exists(partrecordfile):
                        print("skipped partfile - ", partrecordfile)

                        continue
                    res = session.get(pd_url)
                    with open(partfile, 'ab') as f:
                        f.write(res.content)
                        f.flush()
                    open(partrecordfile, 'a').close()

            # all finished
            print("start combining...")
            with open(targetfilename, "ab") as f:
                for partfile in partfiles:
                    with open(partfile, "rb") as par:
                        f.write(par.read())
                        f.flush()
            open(targetfilename+".ok", "a").close()
            # change to mp4 file
            print("download finish - ", targetfilename)

            # if download finish let's remove the directory
            shutil.rmtree(tempdir)
    except Exception as e:
        print(traceback.format_exc())
        #print("Error found", str(e))

    finally:
        latch.count_down()

def compose_target_file(targetfolder, name, quality):
    return str(targetfolder) + os.sep + name + quality + ".mp4"

def compose_target_recordfile(targetfolder, name, quality):
    return compose_target_file(targetfolder, name, quality) + ".ok"


def multi_thread_download(session, courses, targetfolder, **kwargs):
    # download all courses into targetfolder
    path = pathlib.Path(targetfolder)
    if not path.exists() or  path.is_file():
        os.makedirs(targetfolder)
    print("Will download into ", targetfolder)
    videoQuality = kwargs.get("quality", "sd")

    # fetch all tasks
    names = []
    m3u8s = []
    for c in courses:
        if not c.accessok or c.video_map is None:
            continue
        if videoQuality not in c.video_map:
            print("The video not exists this quality, skip", c.name, " videos:", c.video_map)
            continue
        if os.path.exists(compose_target_recordfile(targetfolder, c.name, videoQuality)):
            print("The video is there ignore it", c.name)
            continue
        names.append(c.name)
        m3u8s.append(c.video_map[videoQuality]["url"])

    threadcount = int(kwargs.get("threads", 10))

    print("Will download total tasks:", len(names), " with threads ", threadcount)
    while len(names) > 0:
        count = min(len(names), threadcount)
        latch = CountDownLatch(count)
        for i in range(count):
            name = names.pop()
            m3u8 = m3u8s.pop()
            targetfilename = compose_target_file(targetfolder, name, videoQuality)
            print("\t\t start download ", name)
            _thread.start_new_thread(downloadfile, (session, m3u8, targetfilename, latch))
        latch.await()