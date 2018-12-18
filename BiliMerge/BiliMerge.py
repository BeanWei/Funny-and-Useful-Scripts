# -*- coding:gbk -*-

import os
import shutil
import json
import time
import threading


title = None
targetDir = None

def main():
    target_path = raw_input("Please input the Target Path: ")
    output_path = raw_input("Please input the Output Path: ")
    items = os.listdir(target_path)
    for i in items:
        t = threading.Thread(target=handleSingle, args=(os.path.join(target_path, i), target_path, output_path))
        t.start()

def handleSingle(path, basepath, outputpath):
    global title
    global targetDir
    with open(os.path.join(path, "entry.json")) as fp:
        jsonEntry = json.load(fp)
        if not title:
            title = jsonEntry.get("title", "{}".format(time.time() * 1000))
            targetDir = os.path.join(outputpath, title)
            os.makedirs(targetDir.encode("gbk"))
        partname = jsonEntry["page_data"]["part"]
    getBlv(path, partname)

def getBlv(path, partname):
    mp4list = list()
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            blvpath = os.path.join(path, i)
            for b in os.listdir(os.path.join(path, i)):
                if b.endswith(".blv"):
                    newb = b.replace(".blv", ".mp4")
                    os.rename(os.path.join(path, i, b), os.path.join(path, i, newb))
                    mp4list.append(newb)
            filedtr = ""
            mp4list.sort()
            for m in mp4list:
                filedtr += "file " + m + "\n" 
            with open(os.path.join(blvpath, "filelist.txt"), "w") as f:                
                f.write(filedtr)
            partname = partname.replace(" ", "") + ".mp4"
            mergeBlv(blvpath, targetDir, partname)                   

def mergeBlv(shelldir, outputDir, partname):
    merge_cmd = "ffmpeg -f concat -i filelist.txt -c copy {}".format(partname.encode("gbk"))
    execDir = os.path.join(shelldir, "run.bat")
    with open(execDir, "w") as fp:
        fp.write(merge_cmd)
    os.chdir(unicode(shelldir, "utf-8"))
    os.system(unicode(execDir, "utf-8"))
    createpath = os.path.join(shelldir, partname)
    while True:
        if os.path.exists(createpath):
            shutil.move(createpath, outputDir)
            break


if __name__ == "__main__":
    main()