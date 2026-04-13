from client import Client
import sys
import random
from socket import socket, AF_INET, SOCK_STREAM

ADDRESS = (sys.argv[1], int(sys.argv[2]))


answers = {
    0: [0, 1, 0, 0, 1, 0, 1, 1, 0],
    # 1: [0, 1, 0, 0, 0, 0, 0, 1, 0],
}


with socket(AF_INET, SOCK_STREAM) as sock:
    sock.bind(ADDRESS)
    sock.listen()

    while True:
        connection, address = sock.accept()
        with connection:
            client = Client(connection, address)

            client.send_puzzle_seed()

            while True:
                answer = client.receive_answer()
                correct = answers[client.puzzle]

                if answer == correct:
                    client.send_correct()
                    break
                else:
                    client.send_incorrect()
