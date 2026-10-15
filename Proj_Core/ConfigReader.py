#1. need to parse the value in common.cfg
config = {} # create a dictionary to store values
with open("Common.cfg", "r") as file:
    for line in file:
        parts = line.split() # split the line where there is a whitespace
        key = parts[0] # the key will be the string value
        if(key != "FileName"):
            value = int(parts[1]) #the value will the numbers and second half of the part
        else:
            value = parts[1]
        config[key] = value #place values in the dictionary
    print(config) #print the dictionary


peers = []

with open("PeerInfo.cfg", "r") as file:
    for line in file:
        parts = line.split()
        peer_id = int(parts[0])
        host = parts[1]
        port = int(parts[2])
        has_file = int(parts[3])

        peer = {
            "peer_id": peer_id,
            "host": host,
            "port": port,
            "has_file": has_file
        }

        peers.append(peer)
print(peers)

__all__ = ['config', 'peers']