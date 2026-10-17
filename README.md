# CNT4007 P2P Network Project

Testing process: 
1. Update PeerInfo.cfg, like:
1001 192.168.1.131 6008 1
1002 192.168.1.140 6008 0
One of the entries must be your IPv4 address. The rest of the entries can be the IPv4 addresses of  your other computers or made-up IPv4 addresses. 
For the made-up IPv4 addresses, PeerProcess's startClient will not break. It will tell that those peer servers are not alive.

2. CMD commands:
Scenario 1: PeerProcesss is the first running process, so it acts as a server.
python PeerProcess.py _your peerID_
python Client.py  192.168.1.140,6008,1001,1002
2. Testing Server and Client without PeerProcess
python Server.py 1002 6008
python Client.py  192.168.1.140,6008,1001,1002

##Updated 10172026
My sister and I have updated Server.py and Client.py. They merged Laurence's code.
We also rewrote Logger.py. Now it can log the TCP connections and produce "log_peer_id.log".
PeerProcess.py was also updated to support those changes.
We haven't merged those changes on Main branch
