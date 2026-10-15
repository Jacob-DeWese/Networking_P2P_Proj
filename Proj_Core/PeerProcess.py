
class PeerProcess:
    def __init__(self, userID):
        self.server_thread = [];
        self.client_thread = [];
        #A list of servers listed in PeerInfo.cfg. Hardcoding for testing purpose.
        peer1= dict(peer_ID =1001, host="10.138.79.226", port=8000)
        peer2= dict(peer_ID =1002, host="10.138.245.53", port=8000)

        #A list of dicts stores peers info.
        self.peerInfo = [peer1, peer2]
        self.userID = userID;

    #Attempt connections to every peer that may already be running.
    def startClient(self):
        #for the first peerprocess
        if len(self.peerInfo) == 0:
            print("No server available")
            return

        aliveServer = 0;

        for peer in self.peerInfo:

            if peer["peer_ID"] == self.userID:
                continue;

            addrLocalhost = peer["host"]
            port = peer["port"]

            try:
                if not (1 <= port <= 65535):
                    raise ValueError("Port out of range")
            except ValueError:
                print("Port out of range.")
                continue

            try:
                
                client = Client.Client(addrLocalhost, port, self.userID)
                # IMPORTANT: pass the method itself, do NOT call it
                myClient = threading.Thread(
                    target=client.run,
                    daemon=True
                )

                myClient.start()
                aliveServer = aliveServer+1;          
                print(f"Client created for {addrLocalhost}:{port}")
                self.client_thread.append(myClient)
                time.sleep(0.5)

            except Exception as e:
                print(f"Failed client for {addrLocalhost}:{port}: {e}")
        print("This end is peerID = "+ str(self.userID) +" There are " + str(aliveServer) + " servers alive.")

    #Server starts listening for incoming connections
    def startServer(self):
        try:
            server = Server.Server()
            myServer = threading.Thread(
                target=server.main,
                args=(self.userID,),
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

        # Keep the main thread alive while the server (and any clients) run
        for t in self.server_thread:
            t.join()
    
def main():
    print("main is called")
    userID = int(sys.argv[1])
    myPeerProcess = PeerProcess(userID);
    myPeerProcess.run()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a peer_ID.")
        sys.exit(1)
    main()   
    
"""
File purpose:


Thinking through (for reading PeerInfo.cfg):
1) PeerProcess gets the information that is within PeerInfo.cfg
2) It then runs Client, loading the [listening port] of the peer into client
3) If a failure occurs, output message, disregard for now (peer could still be in-network)
4) If a success occurs, output success message
    - PeerProcess becomes either the core file that calls others to run, or just offloads role to
    next file in process. Regardless, step 5:
5) Establish handshake connection
"""

