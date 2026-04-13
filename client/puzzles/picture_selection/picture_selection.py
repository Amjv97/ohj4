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
    rng = random.Random(state.seed)
    mount_politicans = rng.randint(1, 9)
    politicans = rng.sample(range(1, 20 + 1), mount_politicans)
    nonpoliticans = rng.sample(range(1, 24 + 1), 9 - mount_politicans)

    state.page = page
    ADDRESS = "127.0.0.1"

    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    images = [
        utils.make_buttons(state, f"http://{ADDRESS}:8000/ok/{i}.jpg", i)
        for i in politicans
    ] + [
        utils.make_buttons(state, f"http://{ADDRESS}:8000/ei/{i}.jpg", i)
        for i in nonpoliticans
    ]

    print([f"{ADDRESS}:8000/ei/{i}.jpg" for i in nonpoliticans])
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
