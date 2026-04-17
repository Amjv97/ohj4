from collections.abc import Callable
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
    Animation,
    AnimationCurve,
    FilterQuality,
    Container,
    BoxShadow,
    Colors,
    AlertDialog,
    TextButton,
)


# Helper function for creating popups with a title and multiple buttons
def make_dialog_multiaction(
    functions: list[Callable],
    title_text: str,
    button_texts: list[str],
    modal: bool = False,
    tight: bool = True,
) -> AlertDialog:
    title = Text(title_text)
    actions: list[Control] = [
        TextButton(button_text, on_click=function)
        for function, button_text in zip(functions, button_texts)
    ]
    content = Column(
        controls=actions,
        tight=tight,  # Don't let the dialog grow vertically to infinitum
    )
    return AlertDialog(
        modal=modal,
        title=title,
        content=content,
    )


# Helper function for creating popups with a title and a button. Content is optional
def make_dialog(
    function: Callable,
    title_text: str,
    button_text: str,
    content_text: str | None = None,
    modal: bool = False,
) -> AlertDialog:
    title = Text(title_text)
    content = Text(content_text) if content_text else None
    action = TextButton(button_text, on_click=function)
    return AlertDialog(
        modal=modal,
        title=title,
        content=content,
        actions=[action],
    )


def make_button(
    state: State,
    url: str,
    id: int,
) -> Control:
    animation = Animation(duration=300, curve=AnimationCurve.LINEAR)
    image = Image(
        fade_in_animation=animation,  # Don't immediately display pictures that haven't been cached yet
        filter_quality=FilterQuality.HIGH,  # Increases the sharpness by a noticable amount
        src=url,
    )

    shadow = BoxShadow(blur_radius=16, color=Colors.BLACK_12)
    container = Container(
        border_radius=24,
        content=image,
        shadow=shadow,
    )

    function = partial(state.click, id)
    return GestureDetector(
        content=container,
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


def make_image_grid(images: list[Control]) -> Container:
    spacing = 20
    grid = GridView(
        runs_count=3,
        controls=images,
        run_spacing=spacing,
        spacing=spacing,
    )

    shadow = BoxShadow(blur_radius=64, color=Colors.BLACK_26)
    return Container(
        border_radius=48,
        padding=30,
        width=380,
        bgcolor=Colors.WHITE,
        content=grid,
        shadow=shadow,
    )


# Create a list of buttons from the given list of filenames that exist on the server
def get_images(state: State, files: list[int]) -> list[Control]:
    return [make_button(state, state.get_url() + f"assets/{i}.jpg", i) for i in files]


# Read the assets metadata json file from the remote server
def read_assets(state: State) -> dict:
    url = state.get_url() + "assets/assets.json"
    with request.urlopen(url) as file:
        return json.loads(file.read().decode())


# Contact the url using a post request with the given data
def try_send(url: str, data: dict) -> dict | None:
    try:
        # Return the json given as a response if the contact was successful
        return requests.post(url, json=data).json()
    except ConnectionError:
        return None
