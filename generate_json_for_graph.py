import pprint,pickle

pkl_file = open('./instagram_processing/adj_list.p', 'rb')
adj_list = pickle.load(pkl_file)
pkl_file = open('./instagram_processing/id_to_name.p', 'rb')
id_to_uname = pickle.load(pkl_file)

dataset = {}
node_to_position_map = {}

dataset['nodes'] = []
dataset['edges'] = []

#print id_to_uname
#exit()

global_counter = 0

for parent,id_list in adj_list.iteritems():
    dataset['nodes'].append({'name': id_to_uname[parent]})
    node_to_position_map[parent] = global_counter
    global_counter+=1

    #print "#"
    #print id_to_uname[parent]

    # now process each children in the adj list
    for node in id_list:
        try:
            dataset['nodes'].append({'name': id_to_uname[node]})
            #print id_to_uname[node]
            node_to_position_map[node] = global_counter
            global_counter+=1
            dataset['edges'].append({'source': node_to_position_map[node], 'target': node_to_position_map[parent]})
            print str(node_to_position_map[node])+","+str(node_to_position_map[parent])
        except KeyError:
            pass
            #print "Error for node "+node

#pprint.pprint(dataset)

