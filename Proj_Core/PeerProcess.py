import Client
import Server
import threading
import time
import sys
import ConfigReader

class PeerProcess():
    def __init__(self, peer_ID):
        self.peer_ID = peer_ID
        self.server_thread = [];
        self.client_thread = [];
        #A list of servers listed in PeerInfo.cfg Need peerInfo reader!
        #peer0= dict(peer_ID =1001, host="192.168.1.131", port=8000)
        #peer1= dict(peer_ID =1002, host="192.168.1.139", port=8000)
        self.peerInfo = []
        self.port = None
        for peer in ConfigReader.read_peer_info():
            if peer["peer_id"] == peer_ID:
                self.port = peer["port"]
                break
            self.peerInfo.append(peer)

        if self.port is None:
            raise ValueError(f"Peer ID {peer_ID} not found in PeerInfo.cfg")

    #Attempt connections to every peer that may already be running.
    def startClient(self):
        #for the first peerprocess
        if len(self.peerInfo) == 0:
            print("No server available")
            return

        print("There are " + str(len(self.peerInfo)) + " servers available")

        for peer in self.peerInfo:
            addrLocalhost = peer["host"]
            port = peer["port"]

            try:
                if not (1 <= port <= 65535):
                    raise ValueError("Port out of range")
            except ValueError:
                print("Port out of range.")
                continue

            try:
                client = Client.Client(addrLocalhost, port, self.peer_ID)
                # IMPORTANT: pass the method itself, do NOT call it
                myClient = threading.Thread(
                    target=client.run,
                    daemon=True
                )
                myClient.start()          
                print(f"Client created for {addrLocalhost}:{port}")
                self.client_thread.append(myClient)
            except Exception as e:
                print(f"Failed client for {addrLocalhost}:{port}: {e}")

    def startServer(self):
        try:
            Server.selfPeerID = self.peer_ID
            myServer = threading.Thread(
                target=Server.Server.main,
                args=(self.port,),
                daemon=True
            )
            myServer.start()              
            print("Server started in background thread.")
            self.server_thread.append(myServer)
        except Exception as e:
            print(f"Failed to start server: {e}")


    def run(self):
        print("Starting PeerProcess.")

        self.startClient()

        time.sleep(0.5)

        self.startServer()

        # Keep the main thread alive while any clients run
        for t in self.server_thread:
            t.join()
    
def main():
    print("main is called")
    myPeerProcess = PeerProcess();
    myPeerProcess.run()
    
if __name__ == "__main__":
    main()
