import os
import platform
from pathlib import Path
from typing import Any, Dict, List
import json

from src.utils.logger_utility import logger


# Global base settings and theme path
base_settings_path: Path = Path(os.getcwd()) / ".config" / "settings.json"
base_theme_path: Path = Path(os.getcwd()) / "src" / "themes" / "themes.json"


@logger.catch
def getSettingsPath() -> Path:
    """Get the settings path based on the platform"""
    homeDir: Path = Path.home()
    settingsPath: Path = base_settings_path
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


settingsPath: Path = getSettingsPath()
if not settingsPath.exists():
    settingsPath.parent.mkdir(parents=True, exist_ok=True)
    with open(base_settings_path, "r") as file:
        settings: Dict[str, Any] = json.load(file)
    with open(settingsPath, "w") as file:
        json.dump(settings, file, indent=4)


@logger.catch
def getThemesPath() -> Path:
    """Get the themes path"""
    return base_theme_path


themesPath: Path = getThemesPath()

"""Settings"""


@logger.catch
def load_settings() -> Dict[str, Any]:
    """Load the settings from the settings.json file"""
    try:
        with open(settingsPath, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(e)
        return {}


@logger.catch
def update_settings(new_settings: Dict[str, Any]) -> bool:
    """Overwrite the settings file with the new settings"""
    try:
        with open(settingsPath, "w") as file:
            json.dump(new_settings, file, indent=4)
        return True
    except Exception as e:
        logger.error(e)
        return False


"""Themes"""


@logger.catch
def load_themes():
    """Load the themes from the themes.json file"""
    try:
        with open(themesPath, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(e)
        return {}


@logger.catch
def load_current_theme() -> Dict[str, Any]:
    """Load the current theme"""
    settings: Dict[str, Any] = load_settings()
    try:
        theme_module: str = settings["theme"].get("moduleName")
        theme_name: str = settings["theme"].get("fileName")
        with open(
            themesPath.parent / theme_module / theme_name,
            "r",
        ) as file:
            return json.load(file)
    except Exception as e:
        logger.error(e)
        return {}


@logger.catch
def addRecentProjectCreationPath(projectCreationPath: str) -> None:
    """Add a recent project creation path to the settings file"""
    settings: Dict[str, Any] = load_settings()
    recentCreationPaths: List[str] = settings.get("recentProjectCreationPaths", [])
    if projectCreationPath not in recentCreationPaths:
        recentCreationPaths.insert(0, projectCreationPath)
    if len(recentCreationPaths) > 10:  # Keep only the 10 most recent
        recentCreationPaths = recentCreationPaths[:10]
    settings["recentProjectCreationPaths"] = recentCreationPaths
    update_settings(settings)


@logger.catch
def addRecentProjectPath(projectPath: str) -> None:
    """Add a recent project path to the settings file"""
    settings: Dict[str, Any] = load_settings()
    recentProjectPaths: List[str] = settings.get("recentProjectPaths", [])
    if projectPath not in recentProjectPaths:
        recentProjectPaths.insert(0, projectPath)
    if len(recentProjectPaths) > 10:
        recentProjectPaths = recentProjectPaths[:10]
    settings["recentProjectPaths"] = recentProjectPaths
    update_settings(settings)


@logger.catch
def getRecentProjectCreationPaths() -> List[str]:
    """Get the recent project creation paths"""
    return load_settings().get("recentProjectCreationPaths", [])


@logger.catch
def getRecentProjectPaths() -> List[str]:
    """Get the recent project paths"""
    return load_settings().get("recentProjectPaths", [])
