import flet as ft


class State:
    def __init__(self):
        self.selected = [0] * 9

    def click(self, container, selection):
        self.selected[selection] ^= 1
        print(self.selected)

    def make_buttons(
        self,
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
            on_tap=lambda x: self.click(container, imageid),
        )
        return gdetector


def tetris(page: ft.Page):
    def fetch_is_correct(selected):
        return [0, 1, 0, 0, 1, 0, 0, 1, 0] == selected

    state = State()

    def tarkista():
        right = fetch_is_correct(state.selected)
        if right:
            print("correct")
            show_popup(page)
        else:
            print("incorrect")
            show_popup_uudelleen(page)

    def show_popup(page: ft.Page):
        dialog = ft.AlertDialog(
            title=ft.Text("Aivan oikein!!!"),
            content=ft.Text("lorem ipsum"),
            actions=[
                ft.TextButton("EXIT", on_click=close_window),
            ],
        )
        page.show_dialog(dialog)

    def show_popup_uudelleen(page: ft.Page):
        dialog = ft.AlertDialog(
            title=ft.Text("väärin meni"),
            content=ft.Text("lorem ipsum"),
            actions=[
                ft.TextButton("OK YRITÄN UUDELLEEN", on_click=hide_popup),
            ],
        )
        state.selected = [0] * 9
        page.show_dialog(dialog)

    def info_popup(page: ft.Page):
        dialog = ft.AlertDialog(
            title=ft.Text("lorem ipsum"),
            content=ft.Text("lorem ipsum"),
            actions=[
                ft.TextButton("OK YRITÄN UUDELLEEN", on_click=hide_popup),
            ],
        )
        page.show_dialog(dialog)

    async def close_window():
        await page.window.close()

    def hide_popup():
        page.pop_dialog()

    def restart(page: ft.Page):
        state.selected = [0] * 9

    page.title = "v"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.theme_mode = ft.ThemeMode.LIGHT

    images = [
        state.make_buttons(
            f"/home/user/Downloads/ohj4/pulmat/poliitikkovalinta/{i}.jpg", i
        )
        for i in range(9)
    ]
    grid = ft.GridView(
        align=ft.Alignment.CENTER,
        runs_count=3,
        width=300,
        spacing=20,
        controls=images,
    )

    text = ft.Text(
        align=ft.Alignment.CENTER,
        value="voita tetris",
    )

    restart_but = ft.Button("rest", on_click=lambda e: restart(page))
    info = ft.Button("info", on_click=lambda e: info_popup(page))
    tarkistus = ft.Button("Tarkista", on_click=tarkista)
    buttons = ft.Row(
        align=ft.Alignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[restart_but, info, tarkistus],
    )
    column = ft.Column(
        align=ft.Alignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            text,
            grid,
            buttons,
        ],
    )

    page.add(column)
