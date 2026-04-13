import random
from socket import socket
import flet as ft
from state import State
import utils
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


state = State()


def run(sock: socket, seed: int):
    state.socket = sock
    state.seed = seed
    ft.run(main)


def main(page: ft.Page):
    state.page = page
    print(BASE_DIR)

    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    images = [utils.make_buttons(state, f"{BASE_DIR}/{i}.jpg", i) for i in range(9)]
    random.seed(1)
    random.shuffle(images)
    grid = ft.GridView(
        align=ft.Alignment.CENTER,
        runs_count=3,
        width=300,
        spacing=20,
        controls=images,
    )

    text = ft.Text(
        align=ft.Alignment.CENTER,
        value="Valitse kuvat poliitikoista",
    )

    restart_but = ft.Button("rest", on_click=state.restart)
    info = ft.Button("info", on_click=state.info_popup)
    tarkistus = ft.Button("Tarkista", on_click=state.tarkista)
    buttons = ft.Row(
        align=ft.Alignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[restart_but, info, tarkistus],
    )
    column = ft.Column(
        align=ft.Alignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            text,
            grid,
            buttons,
        ],
    )

    page.add(column)
