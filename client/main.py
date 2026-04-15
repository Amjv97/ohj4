import arguments
import client

VERSION = 0

if __name__ == "__main__":
    host, port, language = arguments.parse()
    client.run(host, port, language, VERSION)
