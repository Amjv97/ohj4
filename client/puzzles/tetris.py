from random import Random
from urllib import request
import json
import utils
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


def get_view(state, page: Page) -> View:
    container = Column()

    def build_puzzle():
        container.controls.clear()

        rng = Random(state.seed)

        with request.urlopen(
            f"http://{state.host}:{state.port}/assets/assets.json"
        ) as url:
            data = json.loads(url.read().decode())

        pictures = data["picture_selection"]
        correct = [int(i.replace(".jpg", "")) for i in pictures["correct"]]
        incorrect = [int(i.replace(".jpg", "")) for i in pictures["incorrect"]]
        politicans = rng.sample(correct + incorrect, 9)

        print("politicans:", politicans)

        images = [
            utils.make_buttons(
                state, f"http://{state.host}:{state.port}/assets/{i}.jpg", i
            )
            for i in politicans
        ]
        grid = GridView(
            runs_count=3,
            width=300,
            spacing=20,
            controls=images,
        )

        text = Text(
            value="Valitse kuvat OOOOOOOOOOOOO",
            text_align=TextAlign.CENTER,
        )

        buttons = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Button("rest", on_click=state.reset),
                Button("info", on_click=state.show_popup_info),
                Button("Tarkista", on_click=state.verify_answer),
            ],
        )

        column = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            controls=[text, grid, buttons],
        )

        container.controls.extend([column])
        page.update()

    build_puzzle()
    state.refresh_ui = build_puzzle
    return View(
        route="/picture",
        controls=[container],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
