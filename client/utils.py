import requests
import json
from functools import partial
from requests.exceptions import ConnectionError
from state import State
from urllib import request
from flet import (
    Button,
    Column,
    Control,
    CrossAxisAlignment,
    GestureDetector,
    GridView,
    Image,
    MainAxisAlignment,
    Row,
    Text,
    View,
)


def make_buttons(
    state: State,
    url: str,
    id: int,
) -> Control:
    image = Image(url)
    function = partial(state.click, id)
    return GestureDetector(
        content=image,
        on_tap=function,
    )


def make_view(container: Column) -> View:
    return View(
        controls=[container],
        vertical_alignment=MainAxisAlignment.CENTER,
    )


def make_buttons_row(state: State) -> Row:
    settings = Button("S", on_click=state.show_popup_settings)
    reset = Button("R", on_click=state.reset)
    info = Button("I", on_click=state.show_popup_info)
    verify = Button(state.texts["ui.button.verify"], on_click=state.verify_answer)
    return Row(
        alignment=MainAxisAlignment.CENTER,
        controls=[settings, reset, info, verify],
    )


def make_elements_column_grid(title: Text, grid: GridView, buttons: Row) -> Column:
    return Column(
        horizontal_alignment=CrossAxisAlignment.CENTER,
        controls=[title, grid, buttons],
    )


def make_image_grid(images: list[Control]) -> GridView:
    return GridView(
        controls=images,
        runs_count=3,
        width=300,
    )


def get_images(state: State, files: list[int]) -> list[Control]:
    return [make_buttons(state, state.get_url() + f"assets/{i}.jpg", i) for i in files]


def read_assets(state: State) -> dict:
    url = state.get_url() + "assets/assets.json"
    with request.urlopen(url) as file:
        return json.loads(file.read().decode())


def try_send(url: str, data: dict) -> dict | None:
    try:
        return requests.post(url, json=data).json()
    except ConnectionError:
        return None
