import arguments
import client
import sys

VERSION = 1

if __name__ == "__main__":
    host, port, language = arguments.parse()
    result = client.run(host, port, language, VERSION)

    # Exit code == 2 means that the user completed the puzzle succesfully
    # Exit code != 2 means that the user failed the puzzle
    exit_code = 2 if result else 0
    sys.exit(exit_code)
