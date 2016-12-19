import csv
from BeautifulSoup import BeautifulSoup as BSHTML
import pickle
from instagram.client import InstagramAPI

access_token = "268816162.98a6839.7238b21eb02a442a883d17b728c8e159"
#access_token = "268816162.1677ed0.b9a0ccc6d9794d27b44a20c41bf60cc6"
#client_secret = "7ed5a33e3d3f4b18aab4a27881b6f9e7"
client_secret = "9953ec9b94054192b18982d3b2eac27e"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)


user_ids = {}
user_id = {}
def get_user_names():

    with open('sessions.csv', 'r') as f:
            data = [row for row in csv.reader(f.read().splitlines())]
            #print data[0][9]
            data = data[1:]

    for row in data:
            i = 0
            ids = []
            for element in row:
                
                if i<9 or i>203:
                    i=i+1
                    continue
                i = i+1

                if element.find('<')!=-1:
                    BS = BSHTML(element)
                    #print(BS.font.contents[0].strip())
                    ids.append(BS.font.contents[0].strip())
           
            user_ids[row[0]] = ids

    output = open('user_ids_comments.p', 'wb')
    pickle.dump(user_ids, output)
    print user_ids

def get_user_names_all():

    with open('all_images.csv', 'r') as f:
            data = [row for row in csv.reader(f.read().splitlines())]
            #print data[0][9]
            data = data[1:]

    for row in data:
            i = 0
            ids = []
            for element in row:
                
                if i<9 or i>203:
                    i=i+1
                    continue
                i = i+1

                if element.find('<')!=-1:
                    BS = BSHTML(element)
                    #print(BS.font.contents[0].strip())
                    ids.append(BS.font.contents[0].strip())
           
            user_ids[row[0]] = ids

    output = open('user_ids_comments.p', 'wb')
    pickle.dump(user_ids, output)
    print "Stored the User Names"

def convert_user_name_to_id():
    #only for testing
    #not completely implemented
    pkl_file = open('user_ids_comments.p', 'rb')
    user_ids = pickle.load(pkl_file)

    ele = user_ids['702714440']

    # stores all the converted user names for all ids
    all_ids = {}

    for ele in user_ids.keys():
        all_ids[ele] = []
        list_id = all_ids[ele]
        for d in user_ids[ele]:
            print d
            user = api.user_search(q=d, count=1)
            try:
                    if d != user[0].username:
                            print 'Username to ID failed'
                            continue
            except:
                    print 'Username to ID failed: Error 2'
                    continue
            list_id.append(user[0].id)
            print(user[0].id)

    print all_ids
    exit()
    #user_id['702714440'] = list_id
    output = open('user_ids_numbers.p', 'wb')
    pickle.dump(all_ids, output)
    #print len(user_ids['702714440'])
    #print len(user_id['702714440'])

def main():
    get_user_names_all()
    convert_user_name_to_id()

if __name__ == "__main__":
    main()
