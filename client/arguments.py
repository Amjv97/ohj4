from argparse import ArgumentParser


def parse() -> tuple[str, int, str|None]:
    parser = ArgumentParser(
        prog="CaptchaClient",
        description="A client that connects to the Captcha server and displays a puzzle to the user. Upon completion, the client either relays the user back to the main application or alternatively makes the user try another puzzle if the provided solution was incorrect.",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="Which address should be used for accessing the Captcha server",
    )
    parser.add_argument(
        "-l",
        "--language",
        help="Which language should be used for the user interface",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Which port should be used for accessing the Captcha server",
    )

    arguments = parser.parse_args()
    address = arguments.address or "127.0.0.1"
    port = arguments.port or 41337
    language = arguments.language

    return address, port, language
