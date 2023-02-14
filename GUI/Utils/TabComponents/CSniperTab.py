import math

from flet_core.tabs import Tab
from flet_core import LabelPosition
from flet import Container, alignment, Switch, Slider, Stack
from flet_core.control_event import ControlEvent


def get_component():

    def on_slider_change(e: ControlEvent):
        slider.label = math.floor(e.control.value)
        slider.update()

    def on_switch_change(e: ControlEvent):
        if switch.value:
            print("Cool")
            pass  # do things while toggled
        else:
            print("Drool")
            pass  # stop
    # TODO: do things
    switch = Switch(
        tooltip="The state of the sniper being on", label="Start?",
        label_position=LabelPosition.LEFT,
        on_change=on_switch_change
    )
    slider = Slider(min=3, max=20, divisions=400, label="{value}", on_change=on_slider_change)
    stack = Stack(
        controls=[
            slider,
            switch
        ]
    )
    return stack


class CSniper:
    def __init__(self, STab: Tab):
        STab.content = get_component()
