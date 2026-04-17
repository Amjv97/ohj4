import requests
import json
from collections.abc import Callable
from functools import partial
from requests.exceptions import ConnectionError
from state import State
from urllib import request
from flet import (
    AlertDialog,
    Animation,
    AnimationCurve,
    BoxShadow,
    Button,
    ButtonStyle,
    ButtonTheme,
    ColorScheme,
    Colors,
    Column,
    Container,
    Control,
    CrossAxisAlignment,
    FilterQuality,
    GestureDetector,
    GridView,
    Image,
    MainAxisAlignment,
    Padding,
    RoundedRectangleBorder,
    Row,
    Text,
    TextButton,
    Theme,
    View,
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


def make_shadow(light: bool) -> BoxShadow:
    if light:
        blur_radius = 16
        color = Colors.BLACK_12
    else:
        blur_radius = 64
        color = Colors.BLACK_26

    return BoxShadow(blur_radius=blur_radius, color=color)


def make_image_button(
    function: Callable,
    url: str,
    id: int,
) -> Control:
    animation = Animation(duration=300, curve=AnimationCurve.LINEAR)
    image = Image(
        fade_in_animation=animation,  # Don't immediately display pictures that haven't been cached yet
        filter_quality=FilterQuality.HIGH,  # Increases the sharpness by a noticable amount
        src=url,
    )

    container = Container(
        border_radius=24,
        content=image,
        shadow=make_shadow(True),
    )

    function = partial(function, id)
    return GestureDetector(
        content=container,
        on_tap=function,
    )


def make_view(container: Column) -> View:
    padding = Padding(top=60)
    return View(controls=[container], padding=padding)


def make_button(text: str, function: Callable) -> Container:
    button = Button(text, on_click=function)
    return Container(
        border_radius=999,  # Buttons should be rounded along with their dropshadows
        content=button,
        shadow=make_shadow(True),
    )


def make_buttons_row(state: State) -> Row:
    settings = make_button("S", state.show_popup_settings)
    reset = make_button("R", state.reset)
    info = make_button("I", state.show_popup_info)
    verify = make_button(state.texts["ui.button.verify"], state.verify_answer)
    return Row(
        alignment=MainAxisAlignment.CENTER,
        controls=[settings, reset, info, verify],
        spacing=20,
    )


def make_elements_column_grid(title: Text, grid: Container, buttons: Row) -> Column:
    return Column(
        controls=[title, grid, buttons],
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=40,
    )


def make_image_grid(images: list[Control]) -> Container:
    spacing = 20
    grid = GridView(
        runs_count=3,
        controls=images,
        run_spacing=spacing,
        spacing=spacing,
    )

    return Container(
        border_radius=48,
        padding=30,
        width=380,
        bgcolor=Colors.WHITE,
        content=grid,
        shadow=make_shadow(True),
    )


# Create a list of buttons from the given list of filenames that exist on the server
def get_images(function: Callable, base_url: str, files: list[int]) -> list[Control]:
    return [make_image_button(function, base_url + f"assets/{i}.jpg", i) for i in files]


# Read the assets metadata json file from the remote server
def read_assets(base_url: str) -> dict:
    url = base_url + "assets/assets.json"
    with request.urlopen(url) as file:
        return json.loads(file.read().decode())


# Contact the url using a post request with the given data
def try_send(url: str, data: dict) -> dict | None:
    try:
        # Return the json given as a response if the contact was successful
        return requests.post(url, json=data).json()
    except ConnectionError:
        return None


def make_theme() -> Theme:
    color_scheme = ColorScheme(
        primary=Colors.BLACK,  # FG COLOR
    )
    button_style = ButtonStyle(
        bgcolor="#CECECE",  # Make the buttons visible without elevation
        elevation=0,  # Skeuomorphism not welcome here
        padding=30,  # Make the buttons larger
        shape=RoundedRectangleBorder(),  # Make buttons rectangle since we'll be rounding them with the shadow
    )
    button_theme = ButtonTheme(button_style)

    return Theme(
        color_scheme=color_scheme,
        button_theme=button_theme,
    )
