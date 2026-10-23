import sys
import Client
import Server
import threading
import time
from ConfigReader import read_peer_info
import socket

class PeerProcess():
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.server_thread = [];
        self.client_thread = [];
        #A list of servers listed in PeerInfo.cfg Need peerInfo reader!
        #peer0= dict(peer_ID =1001, host="192.168.1.131", port=8000)
        #peer1= dict(peer_ID =1002, host="192.168.1.139", port=8000)
        #peer0= dict(peer_ID =1001, host="10.138.187.221", port=8000)

        #A list of dicts stores peers info.
        self.peerInfo = read_peer_info()
        self.local_peer = next(
            peer for peer in self.peerInfo
            if peer["peer_id"] == self.peer_id
        )

        for peer in self.peerInfo:
            if peer['peer_id'] == self.peer_id:
                self.port = peer['port']
                break

    #Attempt connections to every peer that may already be running.
    def startClient(self):
        #for the first peerprocess
        if len(self.peerInfo) == 0:
            print("No peers available")
            return
        print("There are " + str(len(self.peerInfo)) + " peers available")
        
        aliveServer = 0;
        for peer in self.peerInfo:
            if peer["peer_id"] == self.peer_id:
                continue
            addrLocalhost = peer["host"]
            port = peer["port"]

            try:
                if not (1 <= port <= 65535):
                    raise ValueError("Port out of range")
            except ValueError:
                print("Port out of range.")
                continue

            try:
                with socket.create_connection((addrLocalhost, port), timeout=1.0):
                    pass

                client = Client.Client(addrLocalhost, port, self.peer_id, peer["peer_id"])
                # IMPORTANT: pass the method itself, do NOT call it
                myClient = threading.Thread(
                    target=client.run,
                    daemon=True,
                )
                myClient.start()
                print(f"Client created for {addrLocalhost}:{port}")
                time.sleep(0.5)
                self.client_thread.append(myClient)
                aliveServer = aliveServer+1

            except Exception as e:
                print(f"Failed client for {addrLocalhost}:{port}: {e}")
                print("Note that it is normal for the first running peer to fail to connect to other peers.")
        if aliveServer == 0:
            print("The connection failed because the server(s) provided is not alive.")
        print("This end is peerID = "+ str(self.peer_id) +" There are " + str(aliveServer) + " servers alive.\n")

    def startServer(self):
        try:
            server = Server.Server(self.peer_id,self.port)
            myServer = threading.Thread(
                target=server.main,
                args = (self.peer_id,self.port),
                daemon=True
            )
            myServer.start()
            print("Server started in background thread.")
            self.server_thread.append(myServer)
        except Exception as e:
            print(f"Failed to start server: {e}")


    def run(self):
        print(f"Starting PeerProcess {self.peer_id}.")

        self.startServer()

        time.sleep(0.5)

        self.startClient()

        # Keep the main thread alive while any clients run
        for t in self.server_thread:
            t.join()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("PeerProcess shutting down.")
    
def main():
    print("Main is called")
    peer_id = int(sys.argv[1])
    myPeerProcess = PeerProcess(peer_id);
    myPeerProcess.run()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a peer_ID.")
        sys.exit(1)
    main()   