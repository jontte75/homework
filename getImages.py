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

theUrl = "www.mtv.fi"
result = requests.get("http://"+theUrl)
parsedPage = BeautifulSoup(result.content,"lxml")
imageList = []
unknownList = []
for imageTag in parsedPage.findAll("img"):
    print(imageTag["src"])
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
    r = requests.get(image)
    if r.status_code == 200:
        with open(stripSecToken(image.split('/')[-1]), "wb") as code: 
            code.write(r.content)
for string in unknownList:
    print(string)
sys.exit(1)
#print(page)
