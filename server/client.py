from socket import socket
import random


class Client:
    address: str
    puzzle: int
    version: int
    seed: int
    connection: socket

    def get_random_seed(self):
        return random.randint(0, 65535)

    def get_random_puzzle(self, version):
        match version:
            case 1:
                puzzles = 0
            case 2:
                puzzles = 0
            case 3:
                puzzles = 0
            case 4:
                puzzles = 0
            case _:
                puzzles = 0
        return random.randint(0, puzzles)

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.version = self.receive_version()
        self.puzzle = self.get_random_puzzle(self.version)
        self.seed = self.get_random_seed()
        print("CLIENT CONNECTED", self.address)

    def receive_version(self):
        version = int.from_bytes(self.connection.recv(1024))
        print("RECEIVED VERSION", version)
        return version

    def send_puzzle_seed(self):
        print("SEND PUZZLESEED", self.puzzle, self.seed)
        homma = self.puzzle.to_bytes(2) + self.seed.to_bytes(2)
        self.connection.sendall(homma)

    def send_correct(self):
        print("RETURNING CORRECT")
        self.connection.sendall(int(1).to_bytes())

    def send_incorrect(self):
        print("RETURNING inCORRECT")
        self.connection.sendall(int(7).to_bytes())

    def receive_answer(self):
        answer = list(self.connection.recv(1024))
        print("GOT ANSWER", answer)
        return answer
