import requests
from flet import Page, AlertDialog, Text, TextButton
from socket import socket


class State:
    def __init__(self):
        self.selected = set()
        self.socket: socket = None  # ty:ignore[invalid-assignment]
        self.page: Page = None  # ty:ignore[invalid-assignment]
        self.seed: int = None  # ty:ignore[invalid-assignment]
        self.refresh_ui = None
        self.host = None
        self.port = None

    def click(self, container, selection):
        if selection in self.selected:
            self.selected.remove(selection)
        else:
            self.selected.add(selection)
        print("selection:", self.selected)

    def tarkista(self):
        url = f"http://{self.host}:{self.port}/set_answer"
        data = {"answer": list(self.selected)}
        response = requests.post(url, json=data)

        status = response.json()["status"]
        match status:
            case "discarded":
                self.show_popup_uudelleen()

            case "accepted":
                self.show_popup()

    def show_popup(self):
        dialog = AlertDialog(
            title=Text("Aivan oikein!!!"),
            content=Text("lorem ipsum"),
            actions=[
                TextButton("EXIT", on_click=self.close_window),
            ],
        )
        self.page.show_dialog(dialog)

    def show_popup_uudelleen(self):
        dialog = AlertDialog(
            title=Text("väärin meni"),
            content=Text("lorem ipsum"),
            actions=[
                TextButton("OK YRITÄN UUDELLEEN", on_click=self.hide_popup_reset),
            ],
        )
        self.selected = set()
        self.page.show_dialog(dialog)

    def info_popup(self):
        dialog = AlertDialog(
            title=Text("info"),
            content=Text("lorem ipsum"),
            actions=[
                TextButton("OK TAKAISIN", on_click=self.hide_popup),
            ],
        )
        self.page.show_dialog(dialog)

    async def close_window(self):
        await self.page.window.close()

    def hide_popup(self):
        self.page.pop_dialog()

    def hide_popup_reset(self):
        self.restart()
        self.page.pop_dialog()

    def restart(self):
        self.request_new_puzzle()
        self.selected = set()
        self.refresh_ui()  # ty:ignore[call-non-callable]

    def request_new_puzzle(self):
        url = f"http://{self.host}:{self.port}/get_puzzle"
        data = {"version": 0}
        response = requests.post(url, json=data)
        puzzle = response.json()["puzzle"]
        self.seed = response.json()["seed"]
        self.goto_puzzle(self.page, puzzle)

    def goto_puzzle(self, page, puzzle):
        match puzzle:
            case 0:
                page.go("/picture")
            case 1:
                page.go("/other")
