import json

prefix_file_name = 'prefixes.json'
server_file_name = 'servers.json'

with open(prefix_file_name, 'r') as json_file:
    prefixes = json.loads(json_file.read())

with open(server_file_name, 'r') as json_file:
    servers = json.loads(json_file.read())

for k, v in servers.items():
    print(k, ':', v)

for k, v in prefixes.items():
    if k in servers:
        print(servers[k], ':', v)
    else:
        print(k, ':', v)