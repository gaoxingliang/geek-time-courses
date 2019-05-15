import os
import pathlib
import traceback


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

    except Exception as e:
        print(traceback.format_exc())
        #print("Error found", str(e))

    finally:
        latch.count_down()
