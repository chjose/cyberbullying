from instagram.client import InstagramAPI
import pprint, pickle

access_token = "268816162.1677ed0.b9a0ccc6d9794d27b44a20c41bf60cc6"
client_secret = "9953ec9b94054192b18982d3b2eac27e"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)

adj_list = {}
id_to_uname = {}


def get_followed_by(parent,user_ids,id_to_uname,adj_list):
    for id in user_ids:
        print id
        try: 
                user_p = api.user(id)
        except:
                continue
        print user_p.username
        id_to_uname[id] = user_p.username
        try:
            user_follows, next = api.user_followed_by(id)
            users = []
            for user in user_follows:
                #print user.id
                #print user.username
                users.append(user.id)
                id_to_uname[user.id] = user.username
                #exit()
            while next:
                #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                user_follows, next = api.user_followed_by(with_next_url=next)
                for user in user_follows:
                    users.append(user.id)
                    #print user
            adj_list[id] = users
        except Exception as e:
            print(e)
    #print id_to_uname


def main():

    pkl_file = open('user_ids_numbers.p', 'rb')
    data1 = pickle.load(pkl_file)
    #pprint.pprint(data1) 

    pkl_file = open('id_to_name.p', 'rb')
    id_to_uname = pickle.load(pkl_file)
    pkl_file = open('adj_list.p', 'rb')
    adj_list = pickle.load(pkl_file)
    for key,user_id_list in data1.iteritems():
        get_followed_by(key,user_id_list,id_to_uname,adj_list)

    output = open('adj_list.p', 'wb')
    pickle.dump(adj_list, output)
    output = open('id_to_name.p', 'wb')
    pickle.dump(id_to_uname, output)
    print id_to_uname
    print len(adj_list)

if __name__ == "__main__":
    main()


