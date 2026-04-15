import client
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
VERSION = 0

if __name__ == "__main__":
    client.run(HOST, PORT, VERSION)
