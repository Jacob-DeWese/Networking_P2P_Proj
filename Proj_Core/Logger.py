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

# Will probably need to pass in the list of preferred neighbors as a parameter, that way it is easier for the function
# to read it later, and limit passing data through
class Logger:
    def __init__(self, myID, peerID):
        self.myID = myID;
        self.peerID = peerID
        self.Time = ""
        self.filename = "log_peer_"+str(myID)+".log"
        #Check if the log file exists.
        ensure_file_exists(self.filename)

    """
    Examples of how these functions will be called:
    mylog.main(1)
    mylog.main(3, [neighbor_list])
    mylog.main(7, pieceIndex)
    mylog.main(10, pieceIndex, numPieces)
    """
    #Currently, Client.py and Server.py call Logger.py uses mylog._functionName_
    #With the main implementation, they will call Logger.py use mylog(_option_)
    def main(self, option, *args):
        #Get the current time
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        #self.Time = str(timestr.date()) + " " + str(timestr.time())
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")

        if option == 1:
            self.clientTCP()
        elif option == 2:
            self.serverTCP()
        elif option == 3:
            self.changeNeighPref(*args)
        elif option == 4:
            self.changeUnchokeNeigh()
        elif option == 5:
            self.unchoking()
        elif option == 6:
            self.choking()
        elif option == 7:
            self.receiveHave(*args)
        elif option == 8:
            self.receiveInter()
        elif option == 9:
            self.receiveNoInter()
        elif option == 10:
            self.downloadPiece(*args)
        elif option == 11:
            self.downloadComp()

    # Option 1
    def clientTCP(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "["+self.Time+"]: Peer ["+ str(self.myID)+"] makes a connection to Peer ["+ str(self.peerID)+"].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 2
    def serverTCP(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        with open(self.filename, "a") as file:
            logstr = "["+self.Time+"]: Peer ["+ str(self.myID)+"] is connected from Peer ["+ str(self.peerID)+"].\n"
            file.write(logstr)

    # Option 3
    # This will need to be updated once neighbor preference is established, and I can get the list. Proof of concept
    def changeNeighPref(self, neighList):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = ("[" + self.Time + "]: Peer [" + str(self.myID) + "] has the preferred neighbors [" +
            ",".join(str(i) for i in neighList) + "].\n")
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 4
    def changeUnchokeNeigh(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "[" + self.Time + "]: Peer [" + str(self.myID) + "] has the optimistically unchoked neighbor [" + str(
            self.peerID) + "].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 5
    def unchoking(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "[" + self.Time + "]: Peer [" + str(self.myID) + "] is unchoked by [" + str(
            self.peerID) + "].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 6
    def choking(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "[" + self.Time + "]: Peer [" + str(self.myID) + "] is choked by [" + str(
            self.peerID) + "].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 7
    # This will need to be updated to get the actual piece
    def receiveHave(self, pieceInd):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "[" + self.Time + "]: Peer [" + str(self.myID) + "] received the 'have' message from [" + str(
            self.peerID) + "] for the piece [" + str(pieceInd) + "].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 8
    def receiveInter(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "[" + self.Time + "]: Peer [" + str(self.myID) + "] received the 'interested' message from [" + str(
            self.peerID) + "].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 9
    def receiveNoInter(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = "[" + self.Time + "]: Peer [" + str(self.myID) + "] received the 'not interested' message from [" + str(
            self.peerID) + "].\n"
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 10
    def downloadPiece(self, pieceInd, numPieces):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = ("[" + self.Time + "]: Peer [" + str(self.myID) + "] has downloaded the piece [" + str(pieceInd)
                  + "] from [" + str(self.peerID) + "]. Now the number of pieces it has is [" + str(numPieces)
                  + "].\n")
        with open(self.filename, "a") as file:
            file.write(logstr)

    # Option 11
    def downloadComp(self):
        timestr = datetime.now(timezone(timedelta(hours=-4)))
        self.Time = timestr.strftime("%m-%d-%Y %H:%M:%S")
        logstr = ("[" + self.Time + "]: Peer [" + str(self.myID) + "] has downloaded the complete file.\n")
        with open(self.filename, "a") as file:
            file.write(logstr)