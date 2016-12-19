import csv
from xlrd import open_workbook
import xlsxwriter
import ast
import requests
import random

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

rows = []

wb = open_workbook('final_data.xlsx')
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
for d in rows:

        if count == 100:
            break
        
        uname = d[7]
        caption = d[10]
        image_url = d[6]
        media_id = d[0]
       
        #print image_url 
        if exists(image_url) == False:
                image_url = 'https://dl.dropboxusercontent.com/u/5887580/pictures/'+str(d[0])+'.jpg'
                print image_url 
                if exists(image_url) == False:
                        continue 

        if d[11] != 'None':
                comment = str(d[11])
                comment = ast.literal_eval(comment)
                if 'count' in comment:
                        continue

        row = []
        row.append('SECTION_HEADER')
        row.append('Media ID: '+media_id)
        new_rows.append(row)

        row = []
        row.append('SECTION_HEADER')
        row.append('Username: '+uname)
        new_rows.append(row)
        
        row = []
        row.append('SECTION_HEADER')
        row.append('Caption: '+caption)
        new_rows.append(row)
        
        row = []
        row.append('IMAGE')


        count+=1
        row.append('')
        row.append('')
        row.append('=Image("'+image_url+'")')

        new_rows.append(row)

        comment_str = "No Comments"
        if d[11] != 'None':
                comment = str(d[11])
                comment = ast.literal_eval(comment)
                #print comment

                print d[11]
                for ele in comment:
                        comment_str = "Username: "+ele['from']['username']+" "
                        comment_str += "Text: "+ele['text']+" "

                        row = []
                        row.append('SECTION_HEADER')
                        row.append(comment_str)
                        new_rows.append(row)

                        #print ele['text']
                        print ele['from']['username']
        else:
                row = []
                row.append('SECTION_HEADER')
                row.append(comment_str)
                new_rows.append(row)
        
        row = []

        row.append('CHECKBOX')
        row.append('Not Required ?')
        row.append('') 
        row.append('')
        row.append('NO')
        #1. Very unlikely        2. Unlikely     3. Can't tell.  4. Possible     5. Very possible
        row.append('YES')

        
        new_rows.append(row)
                
        row = []
        row.append('PAGE_BREAK')
        new_rows.append(row)

print new_rows


workbook = xlsxwriter.Workbook('form_demo.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item in new_rows:
    col = 0
    for ele in item:
        worksheet.write(row, col, ele)
        col += 1
    row += 1


workbook.close()

                                  
                  


            
