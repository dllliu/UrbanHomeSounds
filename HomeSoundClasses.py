from __future__ import print_function
import freesound
import os
import sys
import time
import csv
import numpy as np
from uuid import uuid4

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
            uuid = uuid4()
            rowDictionary={
            "name":new_Name,
            "url":sound.url,
            "uuid":uuid,
            "tags":New_Tags,
            "username":sound.username,
            "license":sound.license,
            "description":sound.description,
            "duration":str(sound.duration),
            "geotags":sound.geotag
            }
            sound.retrieve_preview(".",os.path.join(SOURCE_DATA,dir,new_Name+".wav"))
            count += 1
            Dataoutput.append(rowDictionary)
            print(str(count) + ": " + new_Name,sound.username)

def DownloadNextPage(arr,dir):
    looped_each_count = 0
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
            uuid = uuid4()
            rowDictionaryPaged={
            "name":new_Name,
            "url":sound.url,
            "uuid":uuid,
            "tags":New_Tags,
            "username":sound.username,
            "license":sound.license,
            "description":sound.description,
            "duration":str(sound.duration),
            "geotags":sound.geotag
            }
            sound.retrieve_preview(".",os.path.join(SOURCE_DATA,dir,new_Name+".wav"))
            Dataoutput.append(rowDictionaryPaged)
            count += 1
            print(str(count) + ": " + new_Name,sound.url)
"""
voice_arr = ["speaking","laughing","shouting","crying","coughing"]
DownloadDictOfSoundResults(voice_arr,'001 - Voices')
DownloadNextPage(voice_arr,'001 - Voices')
with open('Voices.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);


Dataoutput.clear()
bev_arr = ["splash","pour","drip","fill","boil"]
DownloadDictOfSoundResults(bev_arr,'002 - Liquids')
DownloadNextPage(bev_arr,'002 - Liquids')
with open('Liquids.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);


Dataoutput.clear()
locomotion_arr = ["walking","clapping","snapping","running"]
DownloadDictOfSoundResults(locomotion_arr,'003 - Locomotion')
DownloadNextPage(locomotion_arr,'003 - Locomotion')
with open('Motion.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
items_arr = ["box moving","coins","plastic bags","keys","velcro","silverware,","cans"]
DownloadDictOfSoundResults(items_arr,'004 - HouseItems')
DownloadNextPage(items_arr,'004 - HouseItems')
with open('HouseholdItems.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
digestive = ["chewing","biting","gargling","hiccuping"]
DownloadDictOfSoundResults(digestive,'005 - Digestive')
DownloadNextPage(digestive,'005 - Digestive')
with open('Locomotion.csv', 'w',encoding='utf-8') as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
Hyg_arr = ["hygiene","vaccum","shaving","cleaning home","aerosol","hair spray"]
DownloadDictOfSoundResults(Hyg_arr,'006 - Hygiene')
DownloadNextPage(Hyg_arr,'006 - Hygiene')
with open('Hygiene.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);
"""

Dataoutput.clear()
nature_arr = ["gusts","rain","thunder","hail"]
DownloadDictOfSoundResults(nature_arr,'007 - Elements')
DownloadNextPage(nature_arr,'007 - Elements')
with open('Nature.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);


Dataoutput.clear()
anm_arr = ["bark","mews","tweet","howl"]
DownloadDictOfSoundResults(anm_arr,'008 - Animals')
DownloadNextPage(anm_arr,'008 - Animals')
with open('Animals.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
Cooking = ["microwave","oven","refrigerator","stove","toaster","kettle"]
DownloadDictOfSoundResults(Cooking,'009 - Cooking_Appliances')
DownloadNextPage(Cooking,'009 - Cooking_Appliances')
with open('Cooking_Appliances.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()

Cleaning = ["dishwasher","washer","dryer","vaccum"]
DownloadDictOfSoundResults(Cleaning,'010 - Cleaning_Appliances')
DownloadNextPage(Cleaning,'010 - Cleaning_Appliances')
with open('Cleaning_Appliances.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()

lighting = ["light switch","flashlight","lamp"]
DownloadDictOfSoundResults(lighting, '011 - LightingAppliances')
DownloadNextPage(lighting, '011 - LightingAppliances')
with open('Lighting.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);


Dataoutput.clear()

ventilation = ["fans","heater","air conditioner","home ventilation"]
DownloadDictOfSoundResults(ventilation,'012 - Ventilation_Appliances')
DownloadNextPage(ventilation,'012 - Ventilation_Appliances')
with open('Ventilation.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
furniture = ["sofa","door","cabinet","chair","bed","drawers","closet"]
DownloadDictOfSoundResults(furniture,'013 - Furniture')
DownloadNextPage(furniture,'013 - Furniture')
with open('Furniture.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

Dataoutput.clear()
tools = ["hammer","saw","screwdriver","power dril"]
DownloadDictOfSoundResults(tools, '014 - Tools')
DownloadNextPage(tools,'014 - Tools')
with open('Tools.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);


Dataoutput.clear()
InstrumentsArr = ["guitar","piano","flute","trumpet","saxophone"]
DownloadDictOfSoundResults(InstrumentsArr,'015 - Instruments')
DownloadNextPage(InstrumentsArr,'015 - Instruments')
with open('Instruments.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = Dataoutput[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()
    for row in Dataoutput:
        writer.writerow(row);

print("Finished Downloads!!!!!!!!")
