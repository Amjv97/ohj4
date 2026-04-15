import utils
from random import Random
from state import State
from flet import (
    Text,
    Column,
    View,
    Page,
)


def get_view(state: State, page: Page) -> View:
    def get_politicans() -> list[int]:
        rng = Random(state.seed)
        assets = utils.read_assets(state)
        files = assets["picture_selection"]
        correct = [int(i.split(".")[0]) for i in files["correct"]]
        incorrect = [int(i.split(".")[0]) for i in files["incorrect"]]
        return rng.sample(correct + incorrect, 9)

    def build_puzzle() -> None:
        politicans = get_politicans()
        images = utils.get_images(state, politicans)

        title = Text("Valitse kuvat poliitikoista")
        grid = utils.make_image_grid(images)
        buttons = utils.make_buttons_row(state)

        column = utils.make_elements_column_grid(title, grid, buttons)
        container.controls = [column]

        page.update()

    container = Column()
    build_puzzle()
    state.refresh_ui = build_puzzle
    return utils.make_view(container)
