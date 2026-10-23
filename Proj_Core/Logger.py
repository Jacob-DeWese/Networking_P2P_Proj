import time
import os
import ConfigReader
peers = ConfigReader.read_peer_info()
logStarted = False
from datetime import datetime, timezone, timedelta
from pathlib import Path

def ensure_file_exists(filename: str):
    file_path = Path(filename)
    if file_path.is_file():
        pass
    else:
        file_path.touch()
        print(f"'{filename}' did not exist and has been created.")

class Logger:
    def __init__(self, myID, peerID):
        self.myID = myID;
        self.peerID = peerID;
        self.Time = "";
        self.filename = "log_peer_"+str(myID)+".log";
        #Check if the log file exists.
        ensure_file_exists(self.filename)

    '''
    #Currently, Client.py and Server.py call Logger.py uses mylog._functionName_
    #With the main implementation, they will call Logger.py use mylog(_option_) 
    def main(self, option):
        #Get the current time
        timestr = datetime.now(timezone(timedelta(hours=-4)));
        #self.Time = str(timestr.date()) + " " + str(timestr.time());
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")

        if option == 1:
            self.clientTCP();
        elif option == 2:
            self.serverTCP();
    '''
            
    #option 1
    def clientTCP(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)));
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "["+self.Time+"]: Peer ["+ str(self.myID)+"] makes a connection to Peer ["+ str(self.peerID)+"].\n";
        with open(self.filename, "a") as file:
            file.write(logstr)


    #option 2
    def serverTCP(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)));
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        with open(self.filename, "a") as file:
            logstr = "["+self.Time+"]: Peer ["+ str(self.myID)+"] is connected from Peer ["+ str(self.peerID)+"].\n"
            file.write(logstr)


'''
#Jacob's code. Needs to rewrite them as functions.
def log_event():
    import Server

    tcpEstablished = Server.tcpEstablished
    changeNeighPref = Server.changeNeighPref
    changeUnchokeNeigh = Server.changeUnchokeNeigh
    unchoking = Server.unchoking
    choking = Server.choking
    receiveHave = Server.receiveHave
    receiveInter = Server.receiveInter
    receiveNoInter = Server.receiveNoInter
    dwnldPiece = Server.dwnldPiece
    cmpltDwnld = Server.cmpltDwnld

    peerID1 = Server.selfPeerID # Placeholder to verify it accurately gets real id
    peerID2 = Server.connToPeer
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
'''

