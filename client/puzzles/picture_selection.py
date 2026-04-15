import json
import flet as ft
import utils
from random import Random
from urllib import request
from socket import socket
from state import State
from pathlib import Path
from flet import (
    GridView,
    Text,
    Row,
    Button,
    Column,
    View,
    TextAlign,
    MainAxisAlignment,
    CrossAxisAlignment,
    Page,
)

BASE_DIR = Path(__file__).resolve().parent
ADDRESS = "127.0.0.1"
PORT2 = 8000

state = State()


def run(sock: socket, seed: int):
    state.socket = sock
    state.seed = seed
    ft.app(target=main)


def main(page: Page):
    state.page = page

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def route_change(e):
        page.views.clear()
        if page.route == "/picture":
            page.views.append(get_view(page))
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/picture")


def get_view(page: Page):
    rng = Random(state.seed)

    with request.urlopen(f"http://{ADDRESS}:{PORT2}/assets/assets.json") as url:
        data = json.loads(url.read().decode())

    pictures = data["picture_selection"]
    correct = [int(i.replace(".jpg", "")) for i in pictures["correct"]]
    incorrect = [int(i.replace(".jpg", "")) for i in pictures["incorrect"]]
    politicans = rng.sample(correct + incorrect, 9)

    print("politicans:", politicans)

    images = [
        utils.make_buttons(state, f"http://{ADDRESS}:{PORT2}/assets/{i}.jpg", i)
        for i in politicans
    ]

    grid = GridView(
        runs_count=3,
        width=300,
        spacing=20,
        controls=images,
    )

    text = Text(
        value="Valitse kuvat poliitikoista",
        text_align=TextAlign.CENTER,
    )

    buttons = Row(
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Button("rest", on_click=state.restart),
            Button("info", on_click=state.info_popup),
            Button("Tarkista", on_click=state.tarkista),
        ],
    )

    column = Column(
        horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER,
        controls=[text, grid, buttons],
    )

    return View(
        route="/picture",
        controls=[column],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
