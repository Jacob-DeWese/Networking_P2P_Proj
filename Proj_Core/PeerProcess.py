"""
File purpose: Work in tandem with PeerInfo.cfg to load and store status information
1) New peer runs: peerProcess 1001 (example)
2) Peer reads Common.cfg to set corresponding variables (consistent, defined in project scope)
3) Peer also reads PeerInfo.cfg, checks 'file or not field' for 0 (missing file) or 1 (has file)
    - If 0 set bitfield to all 0, if 1 set bitfield to all 1
4) Check: if first peer (i.e., PeerInfo.cfg is empty), no other peers to connect
5) If not first peer, connect to other peers in file one by one
6) When peer is connected to at least one other, exchange pieces as described
7) Terminate when all other peers (not just itself) have downloaded the complete file

For purpose of milestone:
To test that the peers are connecting, can run multiple peer processes on a single host (i.e. laptop)

Potential solution for how to get the peers and connect them:
PeerInfo.cfg is manually updated by each new peer.
    - We can assume that no matter what peer they connect to, each peer will have all peers in the config
1) For new peer: First peer it connects to, copy over their PeerInfo.cfg information to itself
2) Then, add itself to the PeerInfo.cfg
3) For the peer connected, also add the new peer to the end of their config file
4) Proceed with file checks, as discussed above
5) Repeat process for every other peer in the network
"""

