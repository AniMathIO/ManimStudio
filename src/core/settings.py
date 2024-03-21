import os
import json
import platform
from pathlib import Path
from typing import Any, Dict, List
from PySide6.QtWidgets import QDialog, QSizePolicy
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtCore import Qt

# UI imports
from src.ui.settings_ui import Ui_Form  # noqa: E402

# Utils imports
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
        settings_path = (
            home_dir / "AppData" / "Roaming" / "ManimStudio" / "settings.json"
        )
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


"""Recent Projects Paths"""


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
    """Add a recent project path to the settings file with last modification date and size"""
    settings: Dict[str, Any] = load_settings()
    recent_project_paths: List[Dict[str, Any]] = settings.get("recentProjectPaths", [])

    # Get last modification time and size
    modification_time = os.path.getmtime(project_path)
    size = os.path.getsize(project_path)

    # Create a new entry for the project
    new_project_entry = {
        "path": project_path,
        "last_modified": modification_time,
        "size": size,
    }

    # Check if the project already exists in the list and update it
    for project in recent_project_paths:
        if project["path"] == project_path:
            project.update(new_project_entry)
            break
    else:
        # If the project is not in the list, add it
        recent_project_paths.insert(0, new_project_entry)

    # Keep only the 10 most recent
    recent_project_paths = recent_project_paths[:10]

    settings["recentProjectPaths"] = recent_project_paths
    update_settings(settings)


@logger.catch
def get_recent_project_creation_paths() -> List[str]:
    """Get the recent project creation paths"""
    return load_settings().get("recentProjectCreationPaths", [])


@logger.catch
def get_recent_project_paths() -> List[Dict[str, Any]]:
    """Get the recent project paths with their last modification date and size"""
    return load_settings().get("recentProjectPaths", [])


@logger.catch
def update_image(ui, current_theme) -> None:
    """Update the image based on the theme and resize event."""
    if (
        "latte" in current_theme["name"].lower()
        or "light" in current_theme["name"].lower()
    ):
        image_path: str = "docs/_static/ManimStudioLogoLight.png"
    else:
        image_path: str = "docs/_static/ManimStudioLogoDark.png"
    pixmap: QPixmap = QPixmap(image_path)
    if not pixmap.isNull() and not pixmap.size().isEmpty():
        scaledPixmap: QPixmap = pixmap.scaled(
            ui.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        ui.label.setPixmap(scaledPixmap)
    ui.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


@logger.catch
def apply_stylesheet(main_window, ui, settings, current_theme) -> None:
    """Apply the stylesheet to the main window and update the image based on the theme"""

    # Set the custom stylesheet based on the current theme
    customStyleSheet: str = f"background-color: {current_theme['background']}; color: {current_theme['font']}; border-color: {current_theme['primary']}; font-size: {settings['fontSize']}px; font-family: {settings['fontFamily']}; "
    main_window.customStyleSheet = customStyleSheet
    main_window.setStyleSheet(customStyleSheet)
    if hasattr(main_window, "styleSheetUpdated"):
        main_window.styleSheetUpdated.emit(customStyleSheet)

    customMenubarStylesheet = str(
        f"background-color: {current_theme['primary']}; color: {current_theme['font']}; border-color: {current_theme['primary']}; font-size: {settings['fontSize']}px; font-family: {settings['fontFamily']}; "
    )

    if hasattr(ui, "menubar"):
        ui.menubar.setStyleSheet(customMenubarStylesheet)
    else:
        main_window.menuBar().setStyleSheet(customMenubarStylesheet)

    # Update the image
    if hasattr(ui, "label"):
        update_image(ui, current_theme)

    main_window.styleSheetUpdated.emit(customStyleSheet)
    logger.info("Stylesheet applied")


@logger.catch
def load_ui(main_window, ui, settings, current_theme, themes):
    """Load the UI from the .ui file"""

    ui.setupUi(main_window)

    ui.label.setSizePolicy(
        QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    )

    # Apply the theme
    apply_stylesheet(main_window, ui, settings, current_theme)

    # Create new menubar item
    settings_action = QAction("Settings", main_window)
    settings_action.triggered.connect(
        lambda: open_settings_dialog(main_window, settings, themes, current_theme)
    )

    ui.menubar.addAction(settings_action)
    ui.newProjectBtn.clicked.connect(lambda: main_window.show_project_creation_dialog())
    ui.openProjectBtn.clicked.connect(lambda: main_window.show_project_open_dialog())

    logger.info("UI loaded")
    return ui


@logger.catch
def open_settings_dialog(main_window, settings, themes, current_theme) -> None:
    """Open the settings dialog"""

    settingsDialog: QDialog = QDialog()
    uiSettings: Ui_Form = Ui_Form()
    uiSettings.setupUi(settingsDialog)

    # Change window title
    settingsDialog.setWindowTitle("Settings")

    # Inherit the theme from the main window
    settingsDialog.setStyleSheet(main_window.customStyleSheet)
    main_window.styleSheetUpdated.connect(settingsDialog.setStyleSheet)

    # Load settings and themes to the dialog
    uiSettings.fontSizeSpinBox.setValue(settings["fontSize"])
    uiSettings.fontComboBox.setCurrentText(settings["fontFamily"])
    uiSettings.themeComboBox.clear()

    # Populate the theme combobox with full theme data
    for theme_module in themes:
        for variant in theme_module["variants"]:
            variant_data = json.dumps(variant)
            uiSettings.themeComboBox.addItem(variant["name"], variant_data)

    # Set the current theme in the combobox
    current_theme_index = uiSettings.themeComboBox.findText(current_theme["name"])

    if current_theme_index >= 0:
        uiSettings.themeComboBox.setCurrentIndex(current_theme_index)
    uiSettings.saveSettingsBtn.clicked.connect(
        lambda: update_settings_from_dialog(
            main_window, uiSettings, settings, themes, current_theme
        )
    )
    settingsDialog.exec()


@logger.catch
def update_settings_from_dialog(
    main_window, uiSettings, settings, themes, current_theme
) -> None:
    """Update the settings from the dialog, and update the UI"""

    # Get recentProjects array from the current settings
    recentProjectPaths: List[str] = settings.get("recentProjectPaths", [])

    # Get recentProjectCreationPaths array from the current settings
    recentProjectCreationPaths: List[str] = settings.get(
        "recentProjectCreationPaths", []
    )

    # Get the current values from the dialog
    fontSize: int = uiSettings.fontSizeSpinBox.value()
    fontFamily: str = uiSettings.fontComboBox.currentText()

    # Extract full theme data from the selected item in the combobox
    theme_data_json: str = uiSettings.themeComboBox.currentData()
    selected_theme: Dict = json.loads(theme_data_json)

    # Create a new settings object
    new_settings: Dict = {
        "fontSize": fontSize,
        "fontFamily": fontFamily,
        "theme": selected_theme,
        "recentProjectCreationPaths": recentProjectCreationPaths,
        "recentProjectPaths": recentProjectPaths,
    }
    # Pass the new settings to the settings module
    if update_settings(new_settings):
        # Update the global settings variable
        settings = new_settings
        # Update the current theme
        current_theme = load_current_theme()
        # Apply the stylesheet
        apply_stylesheet(main_window, main_window.ui, settings, current_theme)
