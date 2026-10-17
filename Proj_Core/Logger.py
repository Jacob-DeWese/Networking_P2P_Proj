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
        logstr = "["+self.Time+"]: Peer ["+ str(self.myID)+"] makes a connection to Peer ["+ str(self.peerID)+"].\n";
        with open(self.filename, "a") as file:
            file.write(logstr)

