import csv
from collections import OrderedDict

with open('processed_data.csv', 'rb') as f:
    r = csv.reader(f)
    dict2 = {row[0]: row[1:] for row in r}

with open('all_images.csv', 'rb') as f:
    r = csv.reader(f)
    dict1 = OrderedDict((row[0], row[1:]) for row in r)

result = OrderedDict()

all_rows = []

for key in dict1.keys():
    if key in dict2:
        row = []
        row.append(key)
        for d in dict1[key]:
            row.append(d)
        for d in dict2[key]:
            row.append(d)

        all_rows.append(row)


#print all_rows
#exit()
with open('apis_combined.csv', 'wb') as f:
    w = csv.writer(f)
    w.writerow(['fname','media_id','url','clarifai_labels','google_labels'])
    for row in all_rows:
        w.writerow(row)
