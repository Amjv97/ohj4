from collections.abc import Callable
from flet import Page, AlertDialog, Text, TextButton
from pathlib import Path
from puzzle import PUZZLE
import asyncio
import json
import locale
import requests


class State:
    host: str
    language: str
    page: Page
    port: int
    puzzle: PUZZLE
    refresh_ui: Callable
    seed: int
    selected: set
    texts: dict[str, str]
    version: int

    def __init__(self) -> None:
        self.selected = set()

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}/"

    def click(self, selection: int) -> None:
        if selection in self.selected:
            self.selected.remove(selection)
        else:
            self.selected.add(selection)

    def verify_answer(self) -> None:
        url = self.get_url() + "verify_answer"
        data = {"answer": list(self.selected)}
        response = requests.post(url, json=data).json()

        if "result" not in response:
            raise Exception(self.texts["exception.verification.inexistent"])

        match response["result"]:
            case "correct":
                self.show_popup_correct()
            case "incorrect":
                self.show_popup_incorrect()
            case _:
                raise Exception(self.texts["exception.verification.invalid"])

    def request_new_puzzle(self) -> None:
        url = self.get_url() + "get_puzzle"
        data = {"version": self.version}
        response = requests.post(url, json=data).json()

        if not all(i in response for i in ["puzzle", "seed"]):
            raise Exception(self.texts["exception.puzzle.inexistent"])

        self.puzzle = PUZZLE(response["puzzle"])
        self.seed = response["seed"]
        self.selected = set()

    def show_popup(
        self,
        function: Callable,
        title_text: str,
        button_text: str,
        content_text: str | None = None,
    ) -> None:
        title = Text(title_text)
        content = Text(content_text) if content_text else None
        action = TextButton(button_text, on_click=function)
        dialog = AlertDialog(
            title=title,
            content=content,
            actions=[action],
        )

        self.page.show_dialog(dialog)

    def show_popup_correct(self) -> None:
        title = self.texts["ui.popup.correct.title"]
        button = self.texts["ui.popup.correct.button"]
        self.show_popup(self.exit, title, button)

    def show_popup_incorrect(self) -> None:
        title = self.texts["ui.popup.incorrect.title"]
        button = self.texts["ui.popup.incorrect.button"]
        self.show_popup(self.hide_popup_reset, title, button)

    def show_popup_info(self) -> None:
        title = self.texts["ui.popup.info.title"]
        content = self.texts["ui.popup.info.content"]
        button = self.texts["ui.popup.info.button"]
        self.show_popup(self.hide_popup, title, button, content)

    async def exit(self) -> None:
        await self.page.window.close()

    def hide_popup(self) -> None:
        self.page.pop_dialog()

    def hide_popup_reset(self) -> None:
        self.reset()
        self.hide_popup()

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

    def get_language(self) -> str:
        local, _ = locale.getlocale()
        local = local.split("_")[0] if local else "en"

        locales_file = "translations/locales.json"
        with open(locales_file, "r") as file:
            locales = set(i.split(".")[0] for i in json.load(file).values())

        if local not in locales:
            local = "en"

        return local

    def update_language(self) -> None:
        self.language = self.get_language()
        locale = f"translations/{self.language}.json"
        locale_en = "translations/en.json"

        # Add missing entries from the english locale as a backup
        with open(locale_en, "r") as file:
            self.texts = json.load(file)

        # Only add the chosen locale on top if it exists
        if Path(locale).exists():
            with open(locale, "r") as file:
                self.texts |= json.load(file)
