from flet import Page, AlertDialog, Text, TextButton
from socket import socket


class State:
    def __init__(self):
        self.selected = set()
        self.socket: socket = None  # ty:ignore[invalid-assignment]
        self.page: Page = None  # ty:ignore[invalid-assignment]
        self.seed: int = None  # ty:ignore[invalid-assignment]

    def click(self, container, selection):
        if selection in self.selected:
            self.selected.remove(selection)
        else:
            self.selected.add(selection)
        print("selection:", self.selected)

    def tarkista(self):
        self.socket.sendall(bytes(self.selected))
        iscorrect = int.from_bytes(self.socket.recv(1024)) == 1
        if iscorrect:
            self.show_popup()
        else:
            self.show_popup_uudelleen()

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
                TextButton("OK YRITÄN UUDELLEEN", on_click=self.hide_popup),
            ],
        )
        self.selected = set()
        self.page.show_dialog(dialog)

    def info_popup(self):
        dialog = AlertDialog(
            title=Text("info"),
            content=Text("lorem ipsum"),
            actions=[
                TextButton("OK YRITÄN UUDELLEEN", on_click=self.hide_popup),
            ],
        )
        self.page.show_dialog(dialog)

    async def close_window(self):
        await self.page.window.close()

    def hide_popup(self):
        self.page.pop_dialog()

    def restart(self):
        # self.request_new_puzzle()
        self.selected = set()

    # def request_new_puzzle(self):
    #     o = 0
    #     self.socket.sendall(o.to_bytes())
    #     data = self.socket.recv(1024)
    #     puzzle = int.from_bytes(data[0:2])
    #     self.seed = int.from_bytes(data[2:4])
    #     self.page
