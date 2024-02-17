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
def get_settings_path() -> Path:
    """Get the settings path based on the platform"""
    home_dir: Path = Path.home()
    settings_path: Path = base_settings_path
    if platform.system() == "Linux":
        settings_path = home_dir / ".config" / "ManimStudio" / "settings.json"
    if platform.system() == "Windows":
        settings_path = home_dir / "AppData" / "Roaming" / "ManimStudio" / "settings.json"
    if platform.system() == "Darwin":
        settings_path = (
            home_dir
            / "Library"
            / "Application Support"
            / "ManimStudio"
            / "settings.json"
        )
    return settings_path


settings_path: Path = get_settings_path()
if not settings_path.exists():
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(base_settings_path, "r") as file:
        settings: Dict[str, Any] = json.load(file)
    with open(settings_path, "w") as file:
        json.dump(settings, file, indent=4)


@logger.catch
def get_themes_path() -> Path:
    """Get the themes path"""
    return base_theme_path


themes_path: Path = get_themes_path()

"""Settings"""


@logger.catch
def load_settings() -> Dict[str, Any]:
    """Load the settings from the settings.json file"""
    try:
        with open(settings_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(e)
        return {}


@logger.catch
def update_settings(new_settings: Dict[str, Any]) -> bool:
    """Overwrite the settings file with the new settings"""
    try:
        with open(settings_path, "w") as file:
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
        with open(themes_path, "r") as file:
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
            themes_path.parent / theme_module / theme_name,
            "r",
        ) as file:
            return json.load(file)
    except Exception as e:
        logger.error(e)
        return {}


@logger.catch
def add_recent_project_creation_path(project_creation_path: str) -> None:
    """Add a recent project creation path to the settings file"""
    settings: Dict[str, Any] = load_settings()
    recent_creation_paths: List[str] = settings.get("recentProjectCreationPaths", [])
    if project_creation_path not in recent_creation_paths:
        recent_creation_paths.insert(0, project_creation_path)
    if len(recent_creation_paths) > 10:  # Keep only the 10 most recent
        recent_creation_paths = recent_creation_paths[:10]
    settings["recentProjectCreationPaths"] = recent_creation_paths
    update_settings(settings)


@logger.catch
def add_recent_project_path(project_path: str) -> None:
    """Add a recent project path to the settings file"""
    settings: Dict[str, Any] = load_settings()
    recent_project_paths: List[str] = settings.get("recentProjectPaths", [])
    if project_path not in recent_project_paths:
        recent_project_paths.insert(0, project_path)
    if len(recent_project_paths) > 10:
        recent_project_paths = recent_project_paths[:10]
    settings["recentProjectPaths"] = recent_project_paths
    update_settings(settings)


@logger.catch
def get_recent_project_creation_paths() -> List[str]:
    """Get the recent project creation paths"""
    return load_settings().get("recentProjectCreationPaths", [])


@logger.catch
def get_recent_project_paths() -> List[str]:
    """Get the recent project paths"""
    return load_settings().get("recentProjectPaths", [])
