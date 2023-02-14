"""
The Settings Manager.
This manager manages settings,
like implied in the name,
if a user wants to change things like:
[1] the theme of the app
[2] the border color of the Account Manager DataTable
I just don't know of other things that a user would change,
 because I'm trying to go fast, and hopefully have a decent implementation.
TODO: Add more settings.
"""
from typing import Dict


class SettingsManager:
    def __init__(self):
        self.Settings: Dict[str | bool | int | any] = {
            "Theme": "Dark"
        }

    def add_setting(self, SettingName: str, default_value: any):
        self.Settings[SettingName] = default_value
    
    def set_setting(self, SettingName: str, new_value: any):
        assert self.Settings[SettingName], f"\"{SettingName}\" not found in Settings."
        assert new_value, f"No new value."
        self.Settings[SettingName] = new_value

    def get_setting(self, SettingName: str) -> any:
        assert self.Settings[SettingName], f"\"{SettingName}\" not found in Settings."
        return self.Settings[SettingName]
