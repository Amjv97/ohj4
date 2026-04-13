import sys
from socket import socket
import flet as ft


class State:
    def __init__(self):
        self.selected = set()
        self.socket: socket = None  # ty:ignore[invalid-assignment]
        self.page: ft.Page = None  # ty:ignore[invalid-assignment]
        self.seed: int = None  # ty:ignore[invalid-assignment]

    def click(self, container, selection):

        if selection in self.selected:
            self.selected.remove(selection)
        else:
            self.selected.add(selection)
        # self.selected[selection] ^= 1
        print(self.selected)

    def tarkista(self):
        self.socket.sendall(bytes(self.selected))
        iscorrect = int.from_bytes(self.socket.recv(1024)) == 1
        if iscorrect:
            print("correct")
            self.show_popup()
        else:
            print("incorrect")
            self.show_popup_uudelleen()

    def show_popup(self):
        dialog = ft.AlertDialog(
            title=ft.Text("Aivan oikein!!!"),
            content=ft.Text("lorem ipsum"),
            actions=[
                ft.TextButton("EXIT", on_click=self.close_window),
            ],
        )
        self.page.show_dialog(dialog)

    def show_popup_uudelleen(self):
        dialog = ft.AlertDialog(
            title=ft.Text("väärin meni"),
            content=ft.Text("lorem ipsum"),
            actions=[
                ft.TextButton("OK YRITÄN UUDELLEEN", on_click=self.hide_popup),
            ],
        )
        self.selected = set()
        self.page.show_dialog(dialog)

    def info_popup(self):
        dialog = ft.AlertDialog(
            title=ft.Text("lorem ipsum"),
            content=ft.Text("lorem ipsum"),
            actions=[
                ft.TextButton("OK YRITÄN UUDELLEEN", on_click=self.hide_popup),
            ],
        )
        self.page.show_dialog(dialog)

    async def close_window(self):
        await self.page.window.close()
        sys.exit(3)

    def hide_popup(self):
        self.page.pop_dialog()

    def restart(self):
        self.selected = set()
