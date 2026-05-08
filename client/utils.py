from puzzle import PUZZLE
from urllib3.util.connection import _set_socket_options
import requests
import json
from collections.abc import Callable
from colors import COLORS
from functools import partial
from requests.exceptions import ConnectionError
from state import State
from urllib import request
from flet import (
    AlertDialog,
    Animation,
    Dropdown,
    DropdownOption,
    Event,
    AnimationCurve,
    BoxShadow,
    Button,
    ButtonStyle,
    ButtonTheme,
    ColorScheme,
    Column,
    Container,
    Control,
    FilterQuality,
    GridView,
    Image,
    Padding,
    RoundedRectangleBorder,
    Row,
    Text,
    TextButton,
    Theme,
    Icons,
    IconData,
    IconButton,
    IconButtonTheme,
    TextStyle,
    FontWeight,
    Alignment,
    View,
    Stack,
    Icon,
    Offset,
)


# Helper function for creating popups with a title and multiple buttons
def make_dialog_multiaction(
    functions: list[Callable],
    title_text: str,
    button_texts: list[str],
    modal: bool = False,
) -> AlertDialog:
    actions: list[Control] = [
        TextButton(button_text, on_click=function)
        for function, button_text in zip(functions, button_texts)
    ]

    return AlertDialog(
        Column(actions, tight=True),  # Limit the dialog vertically
        modal=modal,
        title=Text(title_text),
    )


# Helper function for creating popups with a title and a button. Content is optional
def make_dialog(
    function: Callable,
    title_text: str,
    button_text: str,
    content_text: str | None = None,
    modal: bool = False,
) -> AlertDialog:
    return AlertDialog(
        Text(content_text) if content_text else None,
        modal=modal,
        title=Text(title_text),
        actions=[TextButton(button_text, on_click=function)],
    )


def make_shadow() -> BoxShadow:
    return BoxShadow(blur_radius=16, color=COLORS.SHADOW)


def make_button_image(
    function: Callable,
    url: str,
    id: int,
) -> Stack:
    # Checkmark for indicating whether the image is selected
    checkmark_icon = Icon(
        color=COLORS.BABY_BLUE,
        icon=Icons.CHECK_CIRCLE,
        size=48,
    )

    # Put the icon into a container so that we can make it solid rather than transparent
    checkmark = Container(
        checkmark_icon,
        bgcolor=COLORS.BACKGROUND_PRIMARY,
        border_radius=64,
        offset=Offset(0.1, 0.1),
        padding=-4,
        shadow=make_shadow(),
        visible=False,  # Invisible by default
    )

    image = Image(
        url,
        fade_in_animation=Animation(300, AnimationCurve.LINEAR),
        filter_quality=FilterQuality.HIGH,  # Increases the sharpness by a noticable amount
    )
    image_container = Container(
        image,
        border_radius=20,
        shadow=make_shadow(),
    )
    button = Button(
        image_container,
        aspect_ratio=1,
        bgcolor=COLORS.BACKGROUND_SECONDARY,  # Make the background invisible unless focused
        on_click=partial(function, id, checkmark),
        elevation=0,
    )
    button_container = Container(
        button,
        border_radius=36,
    )

    return Stack([button_container, checkmark])


def make_button_text(
    function: Callable,
    text: str,
    disabled: bool = False,
    highlighted: bool = True,
) -> Container:
    button = Button(
        text,
        disabled=disabled,
        on_click=function,
        bgcolor=COLORS.BABY_BLUE if highlighted else None,
    )

    return Container(
        button,
        border_radius=64,  # Buttons should be rounded along with their dropshadows
        height=64,
        shadow=make_shadow(),
    )


def make_button_icon(function: Callable, icon: IconData) -> Container:
    return Container(
        IconButton(icon=icon, on_click=function),
        border_radius=64,  # Buttons should be rounded along with their dropshadows
        height=64,
        shadow=make_shadow(),
    )


def make_dropdown(
    function: Callable, icon: IconData, puzzle_current: PUZZLE
) -> Container:
    def call(e: Event[Dropdown]) -> None:
        request = int(e.control.value or "0")
        function(request)

    puzzles = [
        "Picture selection",
        "Shape recognition",
        "Text recognition",
    ]

    dropdown = Dropdown(
        "Choose the puzzle",
        on_select=call,
        hint_text=puzzles[puzzle_current.value],
        options=[
            DropdownOption("0", puzzles[0]),
            DropdownOption("1", puzzles[1]),
            DropdownOption("2", puzzles[2]),
        ],
    )
    return Container(
        dropdown,
        width=128,
        height=64,
        shadow=make_shadow(),
    )


def make_buttons_row(state: State) -> Row:
    settings = make_button_icon(state.show_popup_settings, Icons.LANGUAGE_OUTLINED)
    reset = make_dropdown(state.reset, Icons.REFRESH_OUTLINED, state.puzzle)
    info = make_button_icon(state.show_popup_info, Icons.INFO_OUTLINED)
    verify = make_button_text(state.verify_answer, state.texts["ui.button.verify"])
    spacer = Container(expand=True)

    return Row(
        [reset, info, settings, spacer, verify],
        spacing=10,
    )


def make_elements_column_grid(title: Text, grid: Container, buttons: Row) -> Container:
    column = Column(
        [title, grid, buttons],
        spacing=40,
        width=400,
    )

    return Container(
        column,
        alignment=Alignment.CENTER,
        padding=Padding(top=50),
    )


def make_image_grid(images: list[Control]) -> Container:
    grid = GridView(
        images,
        runs_count=3,
        run_spacing=0,
        spacing=0,
    )

    return Container(
        grid,
        border_radius=48,
        padding=15,
        bgcolor=COLORS.BACKGROUND_SECONDARY,
        shadow=make_shadow(),
    )


def make_title(text: str) -> Text:
    return Text(text, weight=FontWeight.W_500, size=24)


# Create a list of buttons from the given list of filenames that exist on the server
def get_images(function: Callable, base_url: str, files: list[int]) -> list[Control]:
    return [make_button_image(function, base_url + f"assets/{i}.jpg", i) for i in files]


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
    button_style = ButtonStyle(
        bgcolor=COLORS.BACKGROUND_BUTTON,  # Make the buttons visible without elevation
        elevation=0,  # Skeuomorphism not welcome here
        icon_size=32,
        padding=16,  # Make the buttons larger
        shape=RoundedRectangleBorder(),  # Make buttons rectangle since we'll be rounding them with the shadow
        text_style=TextStyle(size=20, weight=FontWeight.W_500),
    )

    return Theme(
        color_scheme=ColorScheme(COLORS.FOREGROUND),
        button_theme=ButtonTheme(button_style),
        icon_button_theme=IconButtonTheme(button_style),
    )


def make_view(container: Column) -> View:
    return View([container], bgcolor=COLORS.BACKGROUND_PRIMARY)
