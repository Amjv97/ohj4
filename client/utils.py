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
    GestureDetector,
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
        color = COLORS.LIGHT_SHADOW
    else:
        blur_radius = 64
        color = COLORS.DARK_SHADOW

    return BoxShadow(blur_radius=blur_radius, color=color)


def make_button_image(
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

    # Checkmark for indicating whether the image is selected
    checkmark_icon = Icon(
        color=COLORS.BABY_BLUE,
        icon=Icons.CHECK_CIRCLE,
        size=48,
    )

    # Put the icon into a container so that we can make it solid rather than transparent
    checkmark = Container(
        bgcolor=COLORS.BACKGROUND_PRIMARY,
        border_radius=64,
        content=checkmark_icon,
        padding=-4,
        visible=False,  # Invisible by default
        offset=Offset(-0.25, -0.25),
    )

    stack = Stack([container, checkmark])

    function = partial(function, id, checkmark)
    return GestureDetector(
        content=stack,
        on_tap=function,
    )


def make_button_text(
    function: Callable,
    text: str,
    disabled: bool = False,
    highlighted: bool = True,
) -> Container:
    color = COLORS.BABY_BLUE if highlighted else None
    button = Button(
        content=text,
        disabled=disabled,
        on_click=function,
        bgcolor=color,
    )

    return Container(
        border_radius=64,  # Buttons should be rounded along with their dropshadows
        content=button,
        height=64,
        shadow=make_shadow(True),
    )


def make_button_icon(function: Callable, icon: IconData) -> Container:
    button = IconButton(icon=icon, on_click=function)
    return Container(
        border_radius=64,  # Buttons should be rounded along with their dropshadows
        content=button,
        height=64,
        shadow=make_shadow(True),
    )


def make_buttons_row(state: State) -> Row:
    settings = make_button_icon(state.show_popup_settings, Icons.LANGUAGE_OUTLINED)
    reset = make_button_icon(state.reset, Icons.REFRESH_OUTLINED)
    info = make_button_icon(state.show_popup_info, Icons.INFO_OUTLINED)
    verify = make_button_text(state.verify_answer, state.texts["ui.button.verify"])
    spacer = Container(expand=True)

    return Row(
        controls=[reset, info, settings, spacer, verify],
        spacing=20,
    )


def make_elements_column_grid(title: Text, grid: Container, buttons: Row) -> Container:
    column = Column(
        controls=[title, grid, buttons],
        spacing=40,
        width=400,
    )
    padding = Padding(top=50)

    return Container(
        alignment=Alignment.CENTER,
        content=column,
        padding=padding,
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
        bgcolor=COLORS.BACKGROUND_SECONDARY,
        content=grid,
        shadow=make_shadow(True),
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
    color_scheme = ColorScheme(
        primary=COLORS.FOREGROUND,
    )

    text_style = TextStyle(size=20, weight=FontWeight.W_500)
    button_style = ButtonStyle(
        bgcolor=COLORS.BACKGROUND_BUTTON,  # Make the buttons visible without elevation
        elevation=0,  # Skeuomorphism not welcome here
        icon_size=32,
        padding=16,  # Make the buttons larger
        shape=RoundedRectangleBorder(),  # Make buttons rectangle since we'll be rounding them with the shadow
        text_style=text_style,  # Make the button text more bold and larger
    )
    button_theme = ButtonTheme(button_style)
    icon_button_theme = IconButtonTheme(button_style)

    return Theme(
        color_scheme=color_scheme,
        button_theme=button_theme,
        icon_button_theme=icon_button_theme,
    )


def make_view(container: Column) -> View:
    return View(controls=[container], bgcolor=COLORS.BACKGROUND_PRIMARY)
