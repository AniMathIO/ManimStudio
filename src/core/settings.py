import os
import platform
from pathlib import Path
import sys
import json

"""Settings"""

# Global static base settings path
base_settings_path = Path(os.getcwd()) / ".config" / "settings.json"
base_theme_path = Path(os.getcwd()) / "src" / "themes" / "themes.json"


def getSettingsPath():
    """Get the settings path based on the platform"""
    homeDir = Path.home()
    if platform.system() == "Linux":
        settingsPath = homeDir / ".config" / "ManimStudio" / "settings.json"
    if platform.system() == "Windows":
        settingsPath = homeDir / "AppData" / "Roaming" / "ManimStudio" / "settings.json"
    if platform.system() == "Darwin":
        settingsPath = (
            homeDir
            / "Library"
            / "Application Support"
            / "ManimStudio"
            / "settings.json"
        )
    return settingsPath


settingsPath = getSettingsPath()
if not settingsPath.exists():
    settingsPath.parent.mkdir(parents=True, exist_ok=True)
    with open(base_settings_path, "r") as file:
        settings = json.load(file)
    with open(settingsPath, "w") as file:
        json.dump(settings, file, indent=4)


def getThemesPath():
    """Get the themes path"""
    return base_theme_path


themesPath = getThemesPath()


def load_settings():
    """Load the settings from the settings.json file"""
    try:
        with open(settingsPath, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}


def update_settings(new_settings):
    """Overwrite the settings file with the new settings"""
    try:
        with open(settingsPath, "w") as file:
            json.dump(new_settings, file, indent=4)
        return True
    except Exception as e:
        return False


"""Themes"""


def load_themes():
    """Load the themes from the themes.json file"""
    try:
        with open(themesPath, "r") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}


def load_current_theme():
    """Load the current theme"""
    settings = load_settings()
    try:
        theme_module = settings["theme"].get("moduleName")
        theme_name = settings["theme"].get("fileName")
        with open(
            themesPath.parent / theme_module / theme_name,
            "r",
        ) as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}


def addRecentProjectPath(projectPath):
    """Add a recent project path to the settings"""
    settings = load_settings()
    recentProjects = settings.get("recentProjects", [])
    if projectPath in recentProjects:
        recentProjects.remove(projectPath)
    recentProjects.insert(0, projectPath)
    if len(recentProjects) > 10:
        recentProjects = recentProjects[:10]
    settings["recentProjects"] = recentProjects
    update_settings(settings)
    return recentProjects


def getRecentProjectPaths():
    """Get the recent project paths from the settings"""
    settings = load_settings()
    return settings.get("recentProjects", [])
