from argparse import ArgumentParser


def parse() -> tuple[str, int]:
    parser = ArgumentParser(
        prog="CaptchaServer",
        description="A server that connects to the Captcha client and feeds it puzzles to solve. Additionally, it enables the client to access images contained within the assets directory for puzzles that need them.",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="Which address should be used for accessing the Captcha server",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Which port should be used for accessing the Captcha server",
    )

    arguments = parser.parse_args()
    address = arguments.address or "127.0.0.1"
    port = arguments.port or 41337

    return address, port
