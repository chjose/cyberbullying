#!/usr/bin/env python
"""
Uses the Google Cloud Vision API to determine what entities are found within the image.
As a further step, annotates the image itself with a parsed version of the API response.
"""

import argparse
import base64
import csv
import httplib2
import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials


# Globals
timestamp = str(datetime.datetime.now())  # Use timestamp to store data in unique filenames
json_file_name = "output data/" + timestamp + "-vision-api-output.json"
csv_file_name = "output data/" + timestamp + "-vision-api-output.csv"

super_labels = set()

def process_images(image_input):
    """Determines whether to run the API on a single image or a directory of images """

    image_exts = ['.bmp', '.gif', '.jpg', '.jpeg', '.png']
    ignore_files = ['.DS_Store']  # For Mac OS X 
    all_rows = []

    # Check if folder
    if image_input[-1] == "/":
        dir_name = image_input

        for file_name in os.listdir(dir_name):
            ext = os.path.splitext(file_name)
        
            if file_name not in ignore_files and ext[1].lower() in image_exts and not os.path.isdir(file_name):
                print(file_name)
                resp = main(dir_name + file_name)
                parse_response(dir_name + file_name, resp, all_rows)
    else:
        print(image_input)
        resp = main(image_input)
        print resp
        parse_response(image_input, resp)

    with open('google_api_op_hdata_new.csv', 'w') as csvfile:
        #fieldnames = ['media_id', 'label_result','text_result']
        fieldnames = ['media_id', 'label_result']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for row in all_rows:
            writer.writerow(row)
    
    print len(super_labels)


def store_json(json_input):
    """Log the full JSON response"""

    with open(json_file_name, "a") as f:
        f.write(json_input + '\n')


def store_csv(csv_input):
    """Log the full data in CSV form"""

    with open(csv_file_name, 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        try:
            csv_writer.writerow(csv_input)
        except UnicodeEncodeError:  # TODO: handle unicode OR just run with Python 3 :)
            csv_writer.writerow(["ERROR"])


def main(photo_file):
    """Run a request on a single image"""

    API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
            ['https://www.googleapis.com/auth/cloud-platform'])
    credentials.authorize(http)

    service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(
                body={
                    'requests': [{
                        'image': {
                            'content': image_content
                        },
                        'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 20,
                        },
                            {
                            'type': 'TEXT_DETECTION',
                            'maxResults': 20,
                            }]
                    }]
                })
    response = service_request.execute()

    return response


def parse_response(photo_file, response, all_rows):
    """ Parse response into relevant fields"""
    
    response = response
    query = photo_file
    all_labels = ''
    all_text = ''
    img_labels = '**Labels Found: \n'  # For image annotation
    img_text = '**Text Found: \n'  # For image annotation

    row = []
    row.append(photo_file.split('/')[1].split('.')[0])


    label_dict = {}
    label_list = []

    try:
        labels = response['responses'][0]['labelAnnotations']
        for label in labels:
            label_val = label['description']
            label_list.append(str(label_val))
            super_labels.add(str(label_val))
            #score = str(label['score'])
            #label_dict[label_val] = score
    except KeyError:
        print("N/A labels found")

    row.append(str(label_list)[1:-1].replace(',',' ').replace('\'',''))

    print('\n')
    text_list = []

    try:
        texts = response['responses'][0]['textAnnotations']
        for text in texts:
            text_val = text['description']
            #text_list.append(str(text_val))
    except KeyError:
        print("N/A text found")

    print text_list
    #row.append(str(text_list)[1:-1].replace(',',' ').replace('\'',''))
    print('\n= = = = = Image Processed = = = = =\n')

    all_rows.append(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_input', help='The folder containing images or the image you\'d like to query')
    args = parser.parse_args()
    process_images(args.image_input)
