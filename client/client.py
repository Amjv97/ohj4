from flet import Page
from puzzles import picture_selection
from puzzles import shape_recognition
from puzzles import tetris
from puzzles import text_recognition
from state import State
import flet

state = State()


def app(page: Page) -> None:
    def on_route_change() -> None:
        match page.route:
            case "/picture_selection":
                view = picture_selection.get_view(state, page)
            case "/tetris":
                view = tetris.get_view(state, page)
            case "/text_recognition":
                view = text_recognition.get_view(state, page)
            case "/shape_recognition":
                view = shape_recognition.get_view(state, page)
            case _:
                raise Exception(state.texts["exception.route.invalid"])

        page.views = [view]
        page.update()

    page.on_route_change = on_route_change
    state.page = page
    state.change_puzzle()  # Open the given puzzle at startup


def run(host: str, port: int, language: str | None, version: int) -> bool:
    state.host = host
    state.port = port
    state.version = version
    state.update_language(language)
    state.request_new_puzzle()
    flet.app(target=app)

    # Return the result of the puzzle (correct/incorrect)
    return state.result
