import json

prefix_file_name = 'prefixes.json'
server_file_name = 'servers.json'

with open(prefix_file_name, 'r') as json_file:
    prefixes = json.loads(json_file.read())

with open(server_file_name, 'r') as json_file:
    servers = json.loads(json_file.read())

for k, v in servers.items():
    if k in prefixes:
        print(v, ':', prefixes[k])
    else:
        print(v, ':', '/')
