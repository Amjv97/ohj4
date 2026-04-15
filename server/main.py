import threading
from client import Client
import uvicorn
import sys
from socket import socket, AF_INET, SOCK_STREAM
from fastapi import FastAPI
from fastapi.responses import FileResponse

ADDRESS = sys.argv[1]
PORT1 = int(sys.argv[2])
PORT2 = int(sys.argv[3])


def run_http():
    app = FastAPI()

    @app.get("/assets/{name}")
    def image(name: str):
        return FileResponse(f"assets/{name}")

    uvicorn.run(app, host=ADDRESS, port=PORT2)


def run_tcp():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((ADDRESS, PORT1))
        sock.listen()

        while True:
            connection, address = sock.accept()
            with connection:
                client = Client(connection, address)

                client.send_puzzle_seed()

                while True:
                    answer = client.receive_answer()
                    if not answer:
                        break
                    if len(answer)==0 and answer[0]==0:
                        #requesting new puzzle
                        client.send_puzzle_seed()
                        continue
                    correct = client.answer

                    if set(answer) == set(correct):
                        client.send_correct()
                        break
                    else:
                        client.send_incorrect()


if __name__ == "__main__":
    t1 = threading.Thread(target=run_http)
    t2 = threading.Thread(target=run_tcp)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
