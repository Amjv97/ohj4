import server
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

if __name__ == "__main__":
    server.run(HOST, PORT)
