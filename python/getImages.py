#!/usr/bin/python
import sys
try:
    import urllib
    import requests
    from bs4 import BeautifulSoup
except:
    print("Note this script requires urllib, requests and BeautifulSoup4!")
    sys.exit(-1)

#some pages have/use security token added to the image url 
stripSecToken = lambda name: name.split("?")[0]

#some pages img url can point to something "different", so copy just what we think we know
supImgExtensions = ('.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.jp2', '.j2k', '.jpf',
                    '.jpx', '.jpm', '.mj2', '.jxr', '.hdp', '.wdp', '.webp', '.gif', '.png',
                    '.apng', '.mng', '.tiff', '.tif', '.svg', '.svgz', '.xbm', '.bmp', '.dib',
                    '.bmp', '.ico')

theUrl = "www.mtv.fi"
result = requests.get("http://"+theUrl)
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
        imageList.append("http://"+theUrl+imageTag["src"])
    else:
        unknownList.append(imageTag["src"])

for image in imageList:
    imgName = stripSecToken(image.split('/')[-1])
    #to be on safe side
    if (False == imgName.endswith(supImgExtensions) or 5 > len(imgName)):
        unknownList.append(image)
        continue
    r = requests.get(image)
    if r.status_code == 200:
        with open(stripSecToken(imgName), "wb") as code: 
            code.write(r.content)
    else:
        unknownList.append(image)
        imageList.remove(image)

for item in unknownList:
   if item in imageList:
       imageList.remove(item)

with open("Output.txt", "w") as text_file:
    text_file.write("\n".join(imageList))

#for string in unknownList:
#    print(string)
