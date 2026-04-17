import utils
from random import Random
from state import State
from flet import (
    Column,
    View,
    Page,
)


def get_view(state: State, page: Page) -> View:
    # Fetch the correct 9 images to be shown on the screen
    def get_politicans() -> list[int]:
        # We'll need to use the seed given by the server since the server will be calculating the same values independently for verification
        rng = Random(state.seed)
        assets = utils.read_assets(state.get_url())
        files = assets["picture_selection"]
        correct = [int(i.split(".")[0]) for i in files["correct"]]
        incorrect = [int(i.split(".")[0]) for i in files["incorrect"]]
        return rng.sample(correct + incorrect, 9)

    # Build the view as a whole
    def build_puzzle() -> None:
        politicans = get_politicans()
        images = utils.get_images(state.click, state.get_url(), politicans)

        title = utils.make_title(state.texts["ui.puzzle.picture_selection.title"])
        grid = utils.make_image_grid(images)
        buttons = utils.make_buttons_row(state)

        column = utils.make_elements_column_grid(title, grid, buttons)
        container.controls = [column]

        page.update()

    container = Column()
    build_puzzle()

    # Save the function so that we can use it for redrawing the screen after changing the language or shuffling the same puzzle
    state.refresh_ui = build_puzzle
    return utils.make_view(container)
