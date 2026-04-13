import flet as ft


def make_buttons(
    state,
    imagesrc,
    imageid,
):
    image = ft.Image(
        src=imagesrc,
        width=100,
        height=100,
    )
    container = ft.Container(content=image)
    gdetector = ft.GestureDetector(
        content=container,
        on_tap=lambda x: state.click(container, imageid),
    )
    return gdetector
