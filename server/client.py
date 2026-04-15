from enum import Enum
from socket import socket
import json
import random


class PUZZLE(Enum):
    PICTURE_SELECTION = 0
    PICTURE_SELECTION2 = 1


class Client:
    address: str
    puzzle: PUZZLE
    version: int
    seed: int
    connection: socket

    def get_random_seed(self):
        return random.randint(0, 65535)

    def get_random_puzzle(self, version):
        match version:
            case _:
                puzzles = [PUZZLE.PICTURE_SELECTION, PUZZLE.PICTURE_SELECTION2]
        return random.sample(puzzles, 1)[0]

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.version = self.receive_version()
        self.puzzle = self.get_random_puzzle(self.version)
        self.seed = self.get_random_seed()
        self.answer = self.get_answer()
        print("CLIENT CONNECTED", self.address)

    def get_answer(self):
        rng = random.Random(self.seed)

        with open("assets/assets.json", "r") as file:
            data = json.load(file)

        match self.puzzle:
            case PUZZLE.PICTURE_SELECTION:
                a = data["picture_selection"]
                correct = [int(i.replace(".jpg", "")) for i in a["correct"]]
                incorrect = [int(i.replace(".jpg", "")) for i in a["incorrect"]]
                politicans = rng.sample(correct + incorrect, 9)
                politicans = [i for i in politicans if i in correct]
                return set(politicans)
            case PUZZLE.PICTURE_SELECTION2:
                a = data["picture_selection"]
                correct = [int(i.replace(".jpg", "")) for i in a["correct"]]
                incorrect = [int(i.replace(".jpg", "")) for i in a["incorrect"]]
                politicans = rng.sample(correct + incorrect, 9)
                politicans = [i for i in politicans if i in correct]
                return set(politicans)

    def receive_version(self):
        version = int.from_bytes(self.connection.recv(1024))
        print("RECEIVED VERSION", version)
        return version

    def reset(self):
        self.puzzle = self.get_random_puzzle(self.version)
        self.seed = self.get_random_seed()
        self.answer = self.get_answer()
        print(self.answer)

    def send_puzzle_seed(self):
        print("SEND PUZZLESEED", self.puzzle.value, self.seed)
        homma = self.puzzle.value.to_bytes(2) + self.seed.to_bytes(2)

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
        if not answer:
            return None
        return answer
