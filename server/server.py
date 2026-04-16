from puzzle import PUZZLE
from client import Clients
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from random import Random
import json
import uvicorn

clients = Clients()


# Read the assets metadata file that contains information about the images stored within the assets directory
def read_assets() -> dict:
    with open("assets/assets.json", "r") as file:
        return json.load(file)


def run(host: str, port: int) -> None:
    app = FastAPI()
    assets = read_assets()

    # Provide an interface for accessing the assets remotely
    @app.get("/assets/{file}")
    def get_assets(file: str) -> FileResponse:
        return FileResponse(f"assets/{file}")

    # Interface for requesting a new puzzle and initializing the 1:1 connection
    @app.post("/get_puzzle")
    def post_get_puzzle(request: Request, data: dict) -> dict:
        client = clients.add_client(request, data)
        return {
            "puzzle": client.puzzle,
            "seed": client.seed,
        }

    # Interface for verifying if the answer proposed by the client matches the one calculated on the server
    @app.post("/verify_answer")
    def post_verify_answer(request: Request, data: dict) -> dict:
        client = clients.get_client(request)
        if not client:
            raise HTTPException(
                status_code=400, detail="Client hasn't requested a puzzle"
            )

        answer_correct = get_answer_correct(client.puzzle, client.seed)
        answer_proposal = get_answer_proposal(data)

        result = "correct" if answer_proposal == answer_correct else "incorrect"
        return {"result": result}

    # Calculate the answer for the puzzle using the given puzzle ID and seed
    def get_answer_correct(puzzle: PUZZLE, seed: int) -> set:
        rng = Random(seed)

        match puzzle:
            case PUZZLE.PICTURE_SELECTION:
                files = assets["picture_selection"]
                correct = [int(i.split(".")[0]) for i in files["correct"]]
                incorrect = [int(i.split(".")[0]) for i in files["incorrect"]]
                options = rng.sample(correct + incorrect, 9)
                return set(i for i in options if i in correct)
            case _:
                raise HTTPException(status_code=400, detail="Invalid puzzle provided")

    def get_answer_proposal(data: dict) -> set | None:
        return set(data["answer"]) if "answer" in data else None

    # Run the file server independently
    uvicorn.run(app, host=host, port=port)
