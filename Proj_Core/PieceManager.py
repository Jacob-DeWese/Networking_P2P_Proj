from ConfigReader import read_common_cfg
from ConfigReader import read_peer_info
from math import ceil
import random

cfg = read_common_cfg()
def piece_number(cfg):
    file_size = cfg["FileSize"]
    piece_size = cfg["PieceSize"]
    pieces = ceil(file_size/piece_size)
    return pieces

peers_list = read_peer_info()

def peer_has_file(peers_list):
    peer_availability = {}
    n = piece_number(cfg)
    for peer in peers_list:
        if peer["has_file"] == 1:
            bool_list = [True]*n
        else:
            bool_list = [False]*n
        peer_availability[peer["peer_id"]] = bool_list
    return peer_availability

peer_availability = peer_has_file(peers_list)
requested_pieces = {}

def eligible_pieces(local_peer_id, neighbor_peer_id):
    eligible = []
    local_peer_bool = peer_availability[local_peer_id]
    neighbor_peer_bool = peer_availability[neighbor_peer_id]
    n = piece_number(cfg)
    for i in range(n):
        if (not local_peer_bool[i]
                and neighbor_peer_bool[i]
                and i not in requested_pieces):
            eligible.append(i)

    return eligible
# if a piece isn't in requested pieces already, store its index and the neighbor it came from
def record_request(piece_index, neighbor_peer_id):
    requested_pieces[piece_index] = neighbor_peer_id

#if the peer received the requested piece
def complete_request(piece_index):
    if piece_index in requested_pieces:
        requested_pieces.pop(piece_index)

#if the peer chokes you before the requested piece arrives
def release_requests(neighbor_peer_id):
    removed_pieces = [] # we need a list because there may be multiple pieces a peer has and that it chocked from us
    for piece, peer in requested_pieces.items():
        if peer == neighbor_peer_id:
            removed_pieces.append(piece)
    for piece in removed_pieces:
        requested_pieces.pop(piece)

#when a peer is unchocked by a neighbor, it should randomly select a piece
def select_piece(local_peer_id, neighbor_peer_id):
    eligible = eligible_pieces(local_peer_id, neighbor_peer_id)
    if not eligible:
        return None
    return random.choice(eligible)
