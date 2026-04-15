from puzzles import picture_selection
import sys
from socket import socket, AF_INET, SOCK_STREAM


ADDRESS = sys.argv[1]
PORT = int(sys.argv[2])
VERSION = 4


with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((ADDRESS, PORT))
    sock.sendall(VERSION.to_bytes())

    data = sock.recv(4)
    puzzle = int.from_bytes(data[0:2])
    seed = int.from_bytes(data[2:4])

    print("puzzle:", puzzle)
    print("seed:", seed)
    match puzzle:
        case 0:
            picture_selection.run(sock, seed)
        case 1:
            picture_selection.run(sock, seed)
