import urllib
import json
import urllib.request
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


ADDRESS = "127.0.0.1"
PORT2 = 8000


def main(page: ft.Page):
    rng = random.Random(state.seed)

    with urllib.request.urlopen(f"http://{ADDRESS}:{PORT2}/assets/assets.json") as url:
        data = json.loads(url.read().decode())

    a = data["picture_selection"]
    correct = [int(i.replace(".jpg", "")) for i in a["correct"]]
    incorrect = [int(i.replace(".jpg", "")) for i in a["incorrect"]]

    politicans = rng.sample(correct + incorrect, 9)
    print(politicans)

    state.page = page

    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    images = [
        utils.make_buttons(state, f"http://{ADDRESS}:{PORT2}/assets/{i}.jpg", i)
        for i in politicans
    ]

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
