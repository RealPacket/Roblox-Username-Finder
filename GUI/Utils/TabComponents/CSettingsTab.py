from flet_core.tabs import Tab
from flet import Container, alignment, Switch, Page
import flet as ft


def get_component(page: Page):
    def theme_changed(_):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        switch.label = (
            "Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        page.update()
    switch = Switch(label="Light theme", on_change=theme_changed)
    # TODO: do things
    container = Container(
        width=700,
        bgcolor="grey",
        # border=ft.border.all(2, "red"),
        border_radius=10,
        alignment=alignment.center,
        content=switch
    )

    return container


class CSettingsTab:
    def __init__(self, STab: Tab, page: Page):
        STab.content = get_component(page)
