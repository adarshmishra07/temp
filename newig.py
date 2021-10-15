!pip install urlextract
import requests
from bs4 import BeautifulSoup
import re
import requests
import json
import itertools
import os 
import sys
import subprocess
from urlextract import URLExtract
import urllib.request



myjsonfile = open('thisit.json', 'r',encoding="utf8")
jsondata = myjsonfile.read()

obj=json.loads(jsondata)


# The Extractor 9000 for getting any  key from nested json


def json_extract(obj, key):
    
    arr = []

    def extract(obj, arr, key):
        
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res
     
def scrapeLinks():
    # Extracting usefull information like devUrl,ids,imgUrls

    urls = json_extract(obj ,'devUrl')
    ids = json_extract(obj ,'_id')
    imageurls = json_extract(obj ,'imgUrl')


    # Image url for first/main image link of the listing 
    baseimage="//d2kcmk0r62r1qk.cloudfront.net/imageSponsors/xlarge/"

    start_urls = "https://www.buzzbuzzhome.com/ca/"
    final_url = ""
    final_list=[]
    for u in urls:
        final_url = start_urls+u 
        final_list.append(final_url)   
    #Command to print all the urls 

        #print(final_url)

    #print("No of urls is :{}".format(len(final_list)))
    Test_list = final_list[:10]
    #print(Test_list)
    dict = {}
    mydict=dict.fromkeys(ids,None)
    hes = []
    appenddict = {}
    for j in range(len(Test_list)):
        #To print the image id that we are currently working on 
        #print(ids[j])
        url=str(Test_list[j])
        res = requests.get(url)
        #print(source)
        # If else loop  for checking if the image is none so 
        if imageurls[j] == 'None':
            pass
        else:
            print(imageurls[j])
            k =str(imageurls[j])
            specialimage=baseimage +  k
            
            #print(specialimage)
        try:
            
            soup = BeautifulSoup(res.text,"lxml")
            key = ids[j]
            dict.setdefault(key,[]).append(specialimage)
            appenddict = Merge(appenddict,dict)
            for items in soup.select(".thumb"):
                image = items['style'].split("url(")[1].split(")")[0]
                x = image.replace('/MapImages/ListView/','/xlarge/')
                x = x.replace("'",'')
            
                result = re.match("/Development/.", x)
                if result:
                    pass
                else:
                    hes.append(x)
                    print(images)
                    key = ids[j]
                    
                    
                    dict.setdefault(key,[]).append(x)
                    appenddict = Merge(appenddict,dict)
                    
        except:
            #print("Something went wrong")
            pass



    print(dict) 

    out_file = open("imagelinks.json", "w") 
    json.dump(appenddict, out_file, indent = 6) 

    out_file.close() 
    print("We are done ")

    #print(mydict)
    print(appenddict)
    return(appenddict)



scrapeLinks()