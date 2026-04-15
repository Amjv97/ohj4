import requests
from puzzles import picture_selection
import sys


HOST = sys.argv[1]
PORT = int(sys.argv[2])
VERSION = 4

data = {"version": 0}
response = requests.post(f"http://{HOST}:{PORT}/get_puzzle", json=data)
puzzle = response.json()["puzzle"]
seed = response.json()["seed"]

match puzzle:
    case _:
        picture_selection.run(HOST, PORT, seed)
