from collections.abc import Callable
from flet import Page, AlertDialog, Text, TextButton
import asyncio
import requests


class State:
    host: str
    page: Page
    port: int
    puzzle: int
    refresh_ui: Callable
    seed: int
    selected: set
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
            raise Exception("No result provided by the server")

        match response["result"]:
            case "correct":
                self.show_popup_correct()
            case "incorrect":
                self.show_popup_incorrect()

    def request_new_puzzle(self) -> None:
        url = self.get_url() + "get_puzzle"
        data = {"version": self.version}
        response = requests.post(url, json=data).json()

        if not all(i in response for i in ["puzzle", "seed"]):
            raise Exception("No puzzle/seed provided by the server")

        self.puzzle = response["puzzle"]
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
        title = "Olet ihminen ✔️"
        button = "Takaisin pääsovellukseen"
        self.show_popup(self.exit, title, button)

    def show_popup_incorrect(self) -> None:
        title = "Hups! Yritä vielä kerran"
        button = "Yritä toista pulmaa"
        self.show_popup(self.hide_popup_reset, title, button)

    def show_popup_info(self) -> None:
        title = "TODO"
        content = "TODO"
        button = "Takaisin pulmaan"
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
            case 0:
                route = "/picture_selection"
            case 1:
                route = "/tetris"
            case 2:
                route = "/text_recognition"
            case 3:
                route = "/shape_recognition"
        asyncio.create_task(self.page.push_route(route))
