def formatFileName(filename):
    return filename.replace("/", "", -1).replace("\\", "", -1)

def dumpResp(resp):
    print("resp text", resp.text, " resp status", resp.status_code, " headers:", resp.headers)
