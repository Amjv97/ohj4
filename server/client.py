from fastapi import Request, HTTPException
from puzzle import PUZZLE
import random


# List of unique clients stored using their ip-addresses
class Clients:
    clients: dict[str, Client]

    def __init__(self) -> None:
        self.clients = {}

    # Based on an incoming request, see if the same client has already been saved in the dictionary
    def get_client(self, request: Request) -> Client | None:
        host = request.client.host  # ty:ignore[unresolved-attribute]
        return self.clients[host] if host in self.clients else None

    # Add a new client to the dictionary using an incoming request along with its data
    def add_client(self, request: Request, data: dict) -> Client:
        host = request.client.host  # ty:ignore[unresolved-attribute]
        version = data["version"] if "version" in data else -1
        puzzle = data["request"] if "request" in data else -1
        client = Client(version, puzzle)
        self.clients[host] = client
        return client


# A class for storing information about the client needed for retaining the session for multiple function calls
class Client:
    puzzle: PUZZLE
    seed: int
    version: int

    def __init__(self, version: int, puzzle: int) -> None:
        self.version = version
        self.puzzle = self.get_random_puzzle(puzzle)
        self.seed = self.get_random_seed()

    # Based on the version provided by the client, choose a random puzzle from the list of supported puzzles for that version
    def get_random_puzzle(self, puzzle: int) -> PUZZLE:
        if puzzle != -1:
            return PUZZLE(puzzle)

        match self.version:
            case 0:
                puzzles = [PUZZLE.PICTURE_SELECTION]
            case 1:
                puzzles = [PUZZLE.PICTURE_SELECTION, PUZZLE.SHAPE_RECOGNITION]
            case 2:
                puzzles = [
                    PUZZLE.PICTURE_SELECTION,
                    PUZZLE.SHAPE_RECOGNITION,
                    PUZZLE.TEXT_RECOGNITION,
                ]
            case _:
                raise HTTPException(status_code=400, detail="Unsupported version")
        return random.choice(puzzles)

    # Generate a random seed for mutating the puzzle such that it is random enough but can be individually calculated on the server and the client
    def get_random_seed(self) -> int:
        return random.randint(0, 2**16)
