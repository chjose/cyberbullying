import csv
from xlrd import open_workbook
import xlsxwriter
import ast
import requests
import random
import json

from clarifai.rest import ClarifaiApp

app = ClarifaiApp()

model = app.models.get('general-v1.3')

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

rows = []

wb = open_workbook('final_data_3_randamized.xlsx')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols


    num_cols = sheet.ncols   # Number of columns
    for row_idx in range(0, sheet.nrows):    # Iterate through rows
        row = []
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            row.append(cell_obj.value)
            #print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj.value))

        rows.append(row)
    
rows = rows[1:]
print rows[0]
print rows[1]

new_rows = []
count = 0

with open('names.csv', 'w') as csvfile:
    fieldnames = ['media_id', 'url', 'result']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)


    for d in rows:
        #if count==50:
        #    break
        row = []
        uname = d[7]
        caption = d[10]
        image_url = d[6]
        media_id = d[0]
        row.append(media_id)
       
        image_url = 'https://dl.dropboxusercontent.com/u/5887580/pictures/'+str(d[0])+'.jpg'
        print image_url
        row.append(image_url)
        if exists(image_url) == False:
                continue 

        res_json = (model.predict_by_url(image_url))
        print res_json
        #res_json = json.loads(res_json)
        row.append(res_json)
        
        writer.writerow(row)
        count += 1
            


        
