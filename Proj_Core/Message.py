MESSAGE_TYPES = {
    "CHOKE": 0,
    "UNCHOKE": 1,
    "INTERESTED": 2,
    "NOT_INTERESTED": 3,
    "HAVE": 4,
    "BITFIELD": 5,
    "REQUEST": 6,
    "PIECE": 7
}

MESSAGE_NAMES = {
    0: "CHOKE",
    1: "UNCHOKE",
    2: "INTERESTED",
    3: "NOT_INTERESTED",
    4: "HAVE",
    5: "BITFIELD",
    6: "REQUEST",
    7: "PIECE"
}

def build_message(msg_type, payload=b''):
    length = 1 + len(payload)

    return (
        length.to_bytes(4, 'big')
        + bytes([msg_type])
        + payload
    )
    
'''
    def parse_message():
        length = recv(4)
        type = recv(1)
        payload = recv(length-1)
'''

'''
File purpose:
Used by PeerProcess.py
'''
