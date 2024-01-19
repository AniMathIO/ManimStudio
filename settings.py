import os
from pathlib import Path
import sys
import json

"""Settings"""


def load_settings(settings_path):
    """Load the settings from the settings.json file"""
    with open(settings_path, "r") as file:
        return json.load(file)


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
    with open(themes_path, "r") as file:
        return json.load(file)


def load_current_theme(settings):
    """Load the current theme"""
    theme_module = settings["theme"].get("moduleName")
    theme_name = settings["theme"].get("fileName")
    with open(Path(os.getcwd()) / "themes" / theme_module / theme_name, "r") as file:
        return json.load(file)


def update_current_theme(settings_path, settings, new_theme):
    """Update the current theme"""
    settings["theme"] = new_theme
    update_settings(settings_path, settings)
