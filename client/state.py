from collections.abc import Callable
from flet import Page, Container
from functools import partial
from pathlib import Path
from puzzle import PUZZLE
import asyncio
import json
import locale
import utils


class State:
    host: str
    language: str
    page: Page
    port: int
    puzzle: PUZZLE
    refresh_ui: Callable
    result: bool
    retries: int
    seed: int
    selected: set
    texts: dict[str, str]
    version: int

    def __init__(self, retries: int = 3) -> None:
        self.selected = set()
        self.texts = dict()
        self.result = False
        self.retries = retries

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}/"

    # A helper function that is assigned to a button and toggles an element on each invocation
    def click(self, selection: int, icon: Container) -> None:
        if selection in self.selected:
            icon.visible = False
            self.selected.remove(selection)
        else:
            icon.visible = True
            self.selected.add(selection)

    # Contact the server for answer verification and display the result in a popup
    def verify_answer(self) -> None:
        url = self.get_url() + "verify_answer"
        data = {"answer": list(self.selected)}
        response = utils.try_send(url, data)

        if not response:
            raise Exception(self.texts["exception.server.connection.error"])

        if "result" not in response:
            raise Exception(self.texts["exception.verification.inexistent"])

        match response["result"]:
            case "correct":
                self.result = True
                self.show_popup_correct()
            case "incorrect":
                self.retries -= 1
                self.show_popup_incorrect()
            case _:
                raise Exception(self.texts["exception.verification.invalid"])

    # Ask the server for a new puzzle and set it as active
    def request_new_puzzle(self) -> None:
        url = self.get_url() + "get_puzzle"
        data = {"version": self.version}
        response = utils.try_send(url, data)

        if not response:
            raise Exception(self.texts["exception.server.connection.error"])

        if not all(i in response for i in ["puzzle", "seed"]):
            raise Exception(self.texts["exception.puzzle.inexistent"])

        self.puzzle = PUZZLE(response["puzzle"])
        self.seed = response["seed"]
        self.selected = set()

    # The popup that is shown when the user submits the correct answer
    def show_popup_correct(self) -> None:
        title = self.texts["ui.popup.correct.title"]
        button = self.texts["ui.popup.correct.button"]
        dialog = utils.make_dialog(self.exit, title, button, modal=True)
        self.page.show_dialog(dialog)

    # The popup that is shown when the user submits the incorrect answer
    def show_popup_incorrect(self) -> None:
        if self.retries > 0:
            title_path = "ui.popup.incorrect.title"
            button_path = "ui.popup.incorrect.button"
            function = self.hide_popup_reset
        else:
            title_path = "ui.popup.incorrect.title.last"
            button_path = "ui.popup.correct.button"
            function = self.exit

        title = self.texts[title_path]
        button = self.texts[button_path]
        dialog = utils.make_dialog(function, title, button, modal=True)
        self.page.show_dialog(dialog)

    # The popup that is shown when the user activates the information menu
    def show_popup_info(self) -> None:
        title = self.texts["ui.popup.info.title"]
        content = self.texts[f"ui.popup.info.content.{self.puzzle}"]
        button = self.texts["ui.popup.info.button"]
        dialog = utils.make_dialog(self.hide_popup, title, button, content)
        self.page.show_dialog(dialog)

    # The popup that is shown when the user activates the settings menu
    def show_popup_settings(self) -> None:
        locales = self.read_language_file()

        title = self.texts["ui.popup.settings.title"]
        buttons = [i for i in locales.values()] if locales else []
        functions: list[Callable] = (
            [partial(self.hide_popup_settings, i) for i in locales.keys()]
            if locales
            else []
        )

        dialog = utils.make_dialog_multiaction(functions, title, buttons)
        self.page.show_dialog(dialog)

    async def exit(self) -> None:
        await self.page.window.close()

    def hide_popup(self) -> None:
        self.page.pop_dialog()

    # When exiting the settings menu, we need to also update the language along with refreshing the UI
    def hide_popup_settings(self, local: str) -> None:
        self.update_language(local)
        self.refresh_ui()
        self.hide_popup()

    # A function that is called if the user failed the puzzle and decided to retry
    def hide_popup_reset(self) -> None:
        self.reset()
        self.hide_popup()

    # Changing the active puzzle by requesting a new one and switching to it
    def reset(self) -> None:
        puzzle_old = self.puzzle
        self.request_new_puzzle()

        if puzzle_old == self.puzzle:
            # We need to refresh, since the new seed needs to be taken into account
            # We don't need to change the puzzle, since that's already done by refreshing
            self.refresh_ui()
        else:
            # UI doesn't need to be refreshed for some reason if the puzzle changes
            # Otherwise the puzzle gets loaded twice
            self.change_puzzle()

    # Changing the active view to match the newly set puzzle
    def change_puzzle(self) -> None:
        match self.puzzle:
            case PUZZLE.PICTURE_SELECTION:
                route = "/picture_selection"
            case PUZZLE.TETRIS:
                route = "/tetris"
            case PUZZLE.TEXT_RECOGNITION:
                route = "/text_recognition"
            case PUZZLE.SHAPE_RECOGNITION:
                route = "/shape_recognition"
            case _:
                raise Exception(self.texts["exception.puzzle.invalid"])
        asyncio.create_task(self.page.push_route(route))

    # A generic function for reading the json files contained within the assets folder
    def read_language_file(self, filename: str = "locales") -> dict[str, str] | None:
        path = f"translations/{filename}.json"
        if not Path(path).exists():
            return None

        with open(path, "r") as file:
            return {
                # If we're reading the metadata file, the file extension needs to be stripped out
                key.replace(".json", "") if filename == "locales" else key: value
                for key, value in json.load(file).items()
            }

    # Try to parse the preferred language in the following order:
    #   1) OS
    #   2) fallback to "en"
    def get_language(self) -> str:
        local, _ = locale.getlocale()
        local = local.split("_")[0] if local else "en"
        locales = self.read_language_file()

        if not locales or local not in locales.keys():
            local = "en"

        return local

    # Set a new language
    def update_language(self, language: str | None) -> None:
        # Use the language given to the program as an argument
        # If the argument is not given, fetch it from the os
        self.language = language or self.get_language()
        self.texts = dict()

        # Add missing entries from the english locale as a backup
        texts = self.read_language_file("en")
        if texts:
            self.texts |= texts

        # Only add the chosen locale on top if it exists
        texts = self.read_language_file(self.language)
        if texts:
            self.texts |= texts
