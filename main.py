import random
import flet as ft
from pulmat.poliitikkovalinta.main import poliitikkovalinta
from pulmat.tetris.main import tetris


def get_pulma():
    intti = random.randint(0, 1)
    match intti:
        case 0:
            ft.run(poliitikkovalinta)
        case 1:
            ft.run(tetris)


get_pulma()
