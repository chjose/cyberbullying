import csv
import json
import requests
from clarifai.rest import ClarifaiApp

app = ClarifaiApp()

model = app.models.get('general-v1.3')

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

rows = []

URL = []
with open("all_images.csv",'r') as f:
    data = [row for row in csv.reader(f.read().splitlines())]
    for row in data:
        # URL, ID, cyberaggression, cyberbullying
        #URL.append([row[11],row[18],row[19],row[20]])
        URL.append([row[205],row[212],row[213],row[214]])

# print URL
# exit()
URL = URL[1:]

new_rows = []
count = 0
# Keeps track of all the categories
super_categories = set()

with open('clarifai_output.csv', 'w') as csvfile:
    fieldnames = ['filename','media_id', 'url', 'result']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)


    for d in URL:
        #if count==50:
        #    break
        row = []
        #uname = d[7]
        #caption = d[10]
        image_url = d[0]
        media_id = d[1]
        row.append(image_url.split('/')[-1].split('.')[0])
        row.append(media_id)
       
        #image_url = 'https://dl.dropboxusercontent.com/u/5887580/pictures/'+str(d[0])+'.jpg'
        #print image_url
        row.append(image_url)
        if exists(image_url) == False:
                continue 

        category_list = []
        res_json = (model.predict_by_url(image_url))
        for categories in res_json['outputs'][0]['data']['concepts']:
            print categories
            category_list.append(str(categories['name']))
            super_categories.add(categories['name'])

        row.append(str(category_list)[1:-1].replace(',',' ').replace('\'',''))
        #print json.load(res_json)
        #row.append(res_json)
        
        writer.writerow(row)
        count += 1


print len(super_categories)
