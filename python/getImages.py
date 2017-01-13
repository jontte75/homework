#!/usr/bin/env python
import sys
import argparse
import os.path
import os
import urllib
try:
    import requests
    from bs4 import BeautifulSoup
except:
    print("Note this script requires requests and BeautifulSoup4!")
    sys.exit(-1)

#workaround python 2.x vs 3
try:
    input = raw_input
except NameError:
    pass

#some pages have/use security token added to the image url 
stripSecToken = lambda name: name.split("?")[0]

#sometimes img url can point to something unknown, we do not want to copy so accept only "standard" web image formats
supImgExtensions = ('.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.jp2', '.j2k', '.jpf',
                    '.jpx', '.jpm', '.mj2', '.jxr', '.hdp', '.wdp', '.webp', '.gif', '.png',
                    '.apng', '.mng', '.tiff', '.tif', '.svg', '.svgz', '.xbm', '.bmp', '.dib',
                    '.bmp', '.ico')

#supported image file name minimum length is 5, like x.yyy
IMG_NAME_MIN = 5
cmdLineArgs = None

def handleCmdLineArgs():
    global cmdLineArgs
    parser = argparse.ArgumentParser(description='Get all images from a given web page')
    parser.add_argument('-a','--addr', action="store", dest='addr', help='Give the address of web page, like www.mtv.fi')
    parser.add_argument('-f','--file', action="store", dest='file', default='Result.txt', 
                        help='Name of result file, default Result.txt')
    parser.add_argument('-p','--path', action="store", dest='path', default=os.curdir, 
                        help='Destination dir where to store files, default current')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0rc1')

    cmdLineArgs = parser.parse_args()

    if (not cmdLineArgs.addr):
       cmdLineArgs.addr = input('Give address of web page: ')

    cmdLineArgs.addr = cmdLineArgs.addr.lstrip('http://').rstrip('/')

    if (not os.path.isdir(cmdLineArgs.path)):
        print("Path %s does not exist!"%cmdLineArgs.path)
        sys.exit(-1) 
#start
handleCmdLineArgs()

try:
    result = requests.get("http://"+cmdLineArgs.addr)
except:
    print("Could not connect to %s"%cmdLineArgs.addr)
    sys.exit(-1)

parsedPage = BeautifulSoup(result.content,"lxml")
imageList = []
unknownList = []

for imageTag in parsedPage.findAll("img"):
    if (imageTag["src"].startswith("http")):
        imageList.append(imageTag["src"])
    elif (imageTag["src"].startswith("//")):
        imageList.append("http:"+imageTag["src"])
    elif (imageTag["src"].startswith("/")):
        #as it did not start with // but with / assume http://theUrl needed in front
        imageList.append("http://"+cmdLineArgs.addr+imageTag["src"])
    else:
        unknownList.append(imageTag["src"])

for image in imageList:
    imgName = stripSecToken(image.split('/')[-1])
    #to be on safe side
    if (False == imgName.endswith(supImgExtensions) or IMG_NAME_MIN > len(imgName)):
        unknownList.append(image)
        continue
    r = requests.get(image)
    if r.status_code == 200:
        with open(os.path.join(cmdLineArgs.path,stripSecToken(imgName)), "wb") as code: 
            code.write(r.content)
    else:
        unknownList.append(image)
        imageList.remove(image)

for item in unknownList:
   if item in imageList:
       imageList.remove(item)

with open(os.path.join(cmdLineArgs.path,cmdLineArgs.file), "w") as text_file:
    text_file.write("\n".join(imageList))

#let's write possible unknown image urls and other issues to Issues.txt
if (len(unknownList)):
    for string in unknownList:
        with open(os.path.join(cmdLineArgs.path,"Issues.txt"), "w") as text_file:
            text_file.write("\n".join(unknownList))

