import socket
import json
import struct

HOST = '127.0.0.1'
PORT = 8080
client_type = 'mongodb'

def retrieve_hotels(s, client_type):
    dic = {'client_type':client_type, 'database': 'hotels_db', 'collection':'hotels','operation':'read', 'filter':""}
    send_message(s, dic)
    data = s.recv(8192)
    print(data)
    json_data = json.loads(data)
    return list(json_data.values())

def query(s, client_type, database, collection, operation, filter):
    dic = {'client_type':client_type, 'database': database, 'collection':collection, 'operation':operation, 'filter':filter}
    send_message(s, dic)
    data = s.recv(8192)
    json_data = json.loads(data)
    return list(json_data.values())

def migration_query(s, source, destination, database, collection, operation):
    dic = {'source':source, 'destination': destination, 'database':database, 'collection':collection, 'operation':operation, 'client_type':'mongodb'}
    send_message(s, dic)

def send_message(s, msg):
    length = len(str(msg))
    packed_length = struct.pack('>I', length)
    s.sendall(packed_length)
    string_message = json.dumps(msg).encode('utf-8')
    s.sendall(string_message)
    
    
