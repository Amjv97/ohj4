import server
import arguments

if __name__ == "__main__":
    host, port = arguments.parse()
    server.run(host, port)
