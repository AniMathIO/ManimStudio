import os
from pathlib import Path
import sys
import json

"""Settings"""


def load_settings(settings_path):
    """Load the settings from the settings.json file"""
    try:
        with open(settings_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return json.load({})


def update_settings(settings_path, new_settings):
    """Overwrite the settings file with the new settings"""
    try:
        with open(settings_path, "w") as file:
            json.dump(new_settings, file, indent=4)
        return True
    except Exception as e:
        return False


"""Themes"""


def load_themes(themes_path):
    """Load the themes from the themes.json file"""
    try:
        with open(themes_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return json.load({})


def load_current_theme(settings):
    """Load the current theme"""
    try:
        theme_module = settings["theme"].get("moduleName")
        theme_name = settings["theme"].get("fileName")
        with open(
            Path(os.getcwd()) / "themes" / theme_module / theme_name, "r"
        ) as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return json.load({})
