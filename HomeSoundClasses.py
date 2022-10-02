from __future__ import print_function
import freesound
import os
import sys
import time
import csv
import numpy as np
import random

api_key = os.getenv('FREESOUND_API_KEY', "BLkaRWL7Vr8nl6K2yvzDw3q3SKKYiuMlclJU7ECy")
client_secret = "BLkaRWL7Vr8nl6K2yvzDw3q3SKKYiuMlclJU7ECy"
client_id = "uPkz0WfINfbiy8r7exNy"
token = client_secret

delay = 2;

client = freesound.FreesoundClient()
client.set_token(token,"token")
#Voice Class

Dataoutput=[]

TARGETITEMCOUNT= 0

TotalItemCount=0

finished = False

SOURCE_DATA = 'AudioData'

sub_dirs = os.listdir(SOURCE_DATA)

dict_classID = {}
for i in range(10):
    dict_classID[sub_dirs[i]] = i

print(dict_classID)

def DownloadDictOfSoundResults(arr,dir):
    count = 0
    finished = False
    temp = []
    for x in arr:
        page = client.text_search(query=x,fields="id,name,previews,duration,username,tags,description,geotag,license,url")
        for sound in page:
            #blacklisted user for uploading incorrectly classified sounds
            if sound.duration <= 5 or str(sound.username) == "Duisterwho" or "\\" in str(sound.name) or "/" in str(sound.name):
                #print("Skipped" + str(sound))
                continue
            tags = str(sound.tags)
            New_Tags = tags.replace(",","+")
            Name = str(sound.name)
            new_Name = Name.replace("\\","-")
            fold_no = random.randrange(0,11)
            rowDictionary={
            "id":sound.id,
            "name":new_Name,
            "url":sound.url,
            "className":dir,
            "classID":dict_classID[dir],
            "tags":New_Tags,
            "username":sound.username,
            "license":sound.license,
            "description":sound.description,
            "duration":str(sound.duration),
            "geotags":sound.geotag,
            "fold":fold_no
            }
            sound.retrieve_preview(".",os.path.join(SOURCE_DATA,dir,str(sound.id)+"-"+str(dict_classID[dir])+"-"+str(fold_no)+".wav"))
            count += 1
            Dataoutput.append(rowDictionary)
            print(str(count) + ": " + new_Name)

def DownloadNextPage(arr,dir):
    count = 0
    for x in arr:
        page = client.text_search(query=x,fields="id,name,previews,duration,username,tags,description,geotag,license,url")
        nextPage = page.next_page()
        for sound in nextPage:
            if sound.duration <= 5 or str(sound.username) == "Duisterwho" or "\\" in str(sound.name) or "/" in str(sound.name):
            #print("Skipped" + str(sound))
                continue
            tags = str(sound.tags)
            New_Tags = tags.replace(",","+")
            Name = str(sound.name)
            new_Name = Name.replace("\\","-")
            fold_no = random.randrange(0,11)
            rowDictionaryPaged={
            "id":sound.id,
            "name":new_Name,
            "url":sound.url,
            "className":dir,
            "classID":dict_classID[dir],
            "tags":New_Tags,
            "username":sound.username,
            "license":sound.license,
            "description":sound.description,
            "duration":str(sound.duration),
            "geotags":sound.geotag,
            "fold":fold_no
            }
            sound.retrieve_preview(".",os.path.join(SOURCE_DATA,dir,str(sound.id)+"-"+str(dict_classID[dir])+"-"+str(fold_no)+".wav"))
            Dataoutput.append(rowDictionaryPaged)
            count += 1
            print(str(count) + ": " + new_Name)

def DownloadThirdPage(arr,dir):
    count = 0
    for x in arr:
        page = client.text_search(query=x,fields="id,name,previews,duration,username,tags,description,geotag,license,url")
        nextPage = page.next_page()
        thirdPage = nextPage.next_page()
        fold_no = random.randrange(0,11)
        for sound in thirdPage:
            if sound.duration <= 5 or str(sound.username) == "Duisterwho" or "\\" in str(sound.name) or "/" in str(sound.name):
            #print("Skipped" + str(sound))
                continue
            tags = str(sound.tags)
            New_Tags = tags.replace(",","+")
            Name = str(sound.name)
            new_Name = Name.replace("\\","-")
            rowDictionaryPaged={
            "id":sound.id,
            "name":new_Name,
            "url":sound.url,
            "className":dir,
            "classID":dict_classID[dir],
            "tags":New_Tags,
            "username":sound.username,
            "license":sound.license,
            "description":sound.description,
            "duration":str(sound.duration),
            "geotags":sound.geotag,
            "fold":fold_no
            }
            sound.retrieve_preview(".",os.path.join(SOURCE_DATA,dir,str(sound.id)+"-"+str(dict_classID[dir])+"-"+str(fold_no)+".wav"))
            Dataoutput.append(rowDictionaryPaged)
            count += 1
            print(str(count) + ": " + new_Name)

voice_arr = ["speaking","laughing","shouting","crying","coughing","sneezing"]
DownloadDictOfSoundResults(voice_arr,'001 - Voices')
DownloadNextPage(voice_arr,'001 - Voices')
with open('Voices.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
locomotion_arr = ["walking","clapping","snapping","running","footsteps"]
DownloadDictOfSoundResults(locomotion_arr,'002 - Locomotion')
DownloadNextPage(locomotion_arr,'002 - Locomotion')
DownloadThirdPage(locomotion_arr,'002 - Locomotion')
with open('Motion.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
digestive = ["chewing","biting","gargling","hiccuping","burping","stomach rumbling"]
DownloadDictOfSoundResults(digestive,'003 - Digestive')
DownloadNextPage(digestive,'003 - Digestive')
DownloadThirdPage(digestive,'003 - Digestive')
with open('Digestive.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);


Dataoutput.clear()
Hyg_arr = ["hygiene","shaving","cleaning home","aerosol","hair spray","ventilator"]
DownloadDictOfSoundResults(Hyg_arr,'004 - Hygiene')
DownloadNextPage(Hyg_arr,'004 - Hygiene')
with open('Hygiene.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
anm_arr = ["dog","cat","bark","mews","howl"]
DownloadDictOfSoundResults(anm_arr,'005 - Animals')
DownloadNextPage(anm_arr,'005 - Animals')
DownloadThirdPage(anm_arr,'005 - Animals')
with open('Animals.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
Cooking = ["microwave","oven","refrigerator","stove","toaster","kettle"]
DownloadDictOfSoundResults(Cooking,'006 - Cooking_Appliances')
DownloadNextPage(Cooking,'006 - Cooking_Appliances')
with open('Cooking_Appliances.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()

Cleaning = ["dishwasher","washer","dryer","vaccum cleaner","toilet","laundry"]
DownloadDictOfSoundResults(Cleaning,'007 - Cleaning_Appliances')
#DownloadNextPage(Cleaning,'007 - Cleaning_Appliances')
with open('Cleaning_Appliances.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()

ventilation = ["fans","heater","air conditioner","home ventilation"]
DownloadDictOfSoundResults(ventilation,'008 - Ventilation_Appliances')
DownloadNextPage(ventilation,'008 - Ventilation_Appliances')
with open('Ventilation.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
furniture = ["sofa","door","cabinet","chair","bed","drawers","closet"]
DownloadDictOfSoundResults(furniture,'009 - Furniture')
DownloadNextPage(furniture,'009 - Furniture')
with open('Furniture.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
InstrumentsArr = ["guitar","piano","flute","trumpet","saxophone"]
DownloadDictOfSoundResults(InstrumentsArr,'010 - Instruments')
DownloadNextPage(InstrumentsArr,'010 - Instruments')
with open('Instruments.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

print("Finished Downloads!!!!!!!!")