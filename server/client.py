from fastapi import Request, HTTPException
from puzzle import PUZZLE
import random


class Clients:
    clients: dict[str, Client]

    def __init__(self):
        self.clients = {}

    def get_client(self, request: Request) -> Client | None:
        host = request.client.host  # ty:ignore[unresolved-attribute]
        return self.clients[host] if host in self.clients else None

    def add_client(self, request: Request, data: dict) -> Client:
        host = request.client.host  # ty:ignore[unresolved-attribute]
        version = data["version"] if "version" in data else -1
        client = Client(version)
        self.clients[host] = client
        return client


class Client:
    puzzle: PUZZLE
    seed: int
    version: int

    def __init__(self, version: int) -> None:
        self.version = version
        self.puzzle = self.get_random_puzzle()
        self.seed = self.get_random_seed()

    def get_random_puzzle(self) -> PUZZLE:
        match self.version:
            case 0:
                puzzles = [PUZZLE.PICTURE_SELECTION]
            case 1:
                puzzles = [PUZZLE.PICTURE_SELECTION, PUZZLE.TETRIS]
            case 2:
                puzzles = [
                    PUZZLE.PICTURE_SELECTION,
                    PUZZLE.TETRIS,
                    PUZZLE.TEXT_RECOGNITION,
                    PUZZLE.SHAPE_RECOGNITION,
                ]
            case _:
                raise HTTPException(status_code=400, detail="Unsupported version")
        return random.choice(puzzles)

    def get_random_seed(self) -> int:
        return random.randint(0, 2**16)
