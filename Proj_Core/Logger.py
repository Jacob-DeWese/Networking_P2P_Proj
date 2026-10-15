import time
import os
from ConfigReader import peers, config

def log_event():
    import Server
    import Client

    tcpEstablished = Server.tcpEstablished
    changeNeighPref = Server.changeNeighPref
    changeUnchokeNeigh = Server.changeUnchokeNeigh
    unchoking = Server.unchoking
    choking = Server.choking
    receiveHave = Server.receiveHave
    receiveInter = Server.receiveInter,
    receiveNoInter = Server.receiveNoInter
    dwnldPiece = Server.dwnldPiece
    cmpltDwnld = Server.cmpltDwnld
    cPort = Client.cPort

    peerID1 = 1000 # Placeholder to verify it accurately gets real id
    peerID2 = cPort
    for peer in peers:
        port = peer['port']
        peer_id = peer['peer_id']
        if peer_id == peerID1:
            peerID1 = peer_id
            break

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file = f'log_peer_{peerID1}.log'

    # # Testing purposes: clear logging file on new start (delete when necessary)
    # with open(file, "r+") as f:
    #     f.seek(0)
    #     f.truncate()

    log_path = os.path.join(script_dir, file)
    with open(log_path, 'a') as fp:
        if tcpEstablished:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] makes a connection to Peer [{peerID2}].\n")
        # Following requires implementation of other functions to operate properly, here for future adjustment
        elif changeNeighPref:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] has the preferred neighbors [preferred neighbor ID list].\n")
        elif changeUnchokeNeigh:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] has the optimistically unchoked neighbor [{peerID2}].\n")
        elif unchoking:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] is unchoked by [{peerID2}].\n")
        elif choking:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] is choked by [{peerID2}].\n")
        elif receiveHave:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] received the 'have' message from [{peerID2}] for the piece [piece index].\n")
        elif receiveInter:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] received the 'interested' message from [{peerID2}].\n")
        elif receiveNoInter:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] received the 'not interested' message from [{peerID2}].\n")
        elif dwnldPiece:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] has downloaded the piece [piece index] from [{peerID2}]. Now the number of pieces it has is [number of pieces]\n")
        elif cmpltDwnld:
            fp.write(f"[{time.ctime()}]: Peer [{peerID1}] has downloaded the complete file.\n")

    dir_list = os.listdir(script_dir)
    print("List of directories and files after creation: ")
    print(dir_list)