import json
from random import Random
import random
from enum import Enum
import uvicorn
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request

clients: dict[str, Client] = {}


class PUZZLE(Enum):
    PICTURE_SELECTION = 0
    TETRIS = 1
    TEXT_RECOGNITION = 2
    SHAPE_RECOGNITION = 3


class Client:
    puzzle: PUZZLE
    version: int
    seed: int


def get_random_puzzle(version):
    match version:
        case 0:
            puzzles = [PUZZLE.PICTURE_SELECTION]
        case _:
            puzzles = list(PUZZLE)
    return random.choice(puzzles)


def get_random_seed():
    return random.randint(0, 65535)


def add_client(host: str, data: dict) -> None:
    version = data["version"]
    puzzle = get_random_puzzle(version)
    seed = get_random_seed()

    client = Client()
    client.puzzle = puzzle
    client.seed = seed
    client.version = version
    clients[host] = client


def run(host: str, port: int) -> None:
    app = FastAPI()

    @app.get("/assets/{name}")
    def image(name: str):
        return FileResponse(f"assets/{name}")

    @app.post("/get_puzzle")
    def get_puzzle(request: Request, data: dict):
        host = request.client.host

        add_client(host, data)
        client = clients[host]

        return {
            "puzzle": client.puzzle,
            "seed": client.seed,
        }

    @app.post("/set_answer")
    def process(request: Request, data2: dict):
        print("set answer for her")
        host = request.client.host

        if host not in clients:
            print("FUCK")
            return {"status": "error"}
        client = clients[host]

        rng = Random(client.seed)

        with open("assets/assets.json", "r") as file:
            data = json.load(file)

        answer = None
        match client.puzzle:
            case _:
                a = data["picture_selection"]
                correct = [int(i.replace(".jpg", "")) for i in a["correct"]]
                incorrect = [int(i.replace(".jpg", "")) for i in a["incorrect"]]
                politicans = rng.sample(correct + incorrect, 9)
                politicans = [i for i in politicans if i in correct]
                answer = set(politicans)

        proposed=set(data2["answer"])
        answer=set(answer)
        print(proposed,answer)
        if proposed == set(answer):
            return {"status": "accepted"}
        else:
            return {"status": "discarded"}

    uvicorn.run(app, host=host, port=port)
