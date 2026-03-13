"""Detect available browsers and Firefox profiles."""

import configparser
import shutil
from pathlib import Path


def get_firefox_profiles():
    """Return list of Firefox profile names."""
    profiles = []
    for profiles_ini in [
        Path.home() / "snap/firefox/common/.mozilla/firefox/profiles.ini",
        Path.home() / ".mozilla/firefox/profiles.ini",
    ]:
        if profiles_ini.exists():
            config = configparser.ConfigParser()
            config.read(profiles_ini)
            for section in config.sections():
                if section.startswith("Profile"):
                    name = config.get(section, "Name", fallback=None)
                    if name:
                        profiles.append(name)
    return profiles


def get_chrome_profiles():
    """Return list of Chrome profile directory names."""
    profiles = []
    for chrome_dir in [
        Path.home() / ".config/google-chrome",
        Path.home() / "snap/chromium/common/chromium",
    ]:
        if chrome_dir.exists():
            for p in sorted(chrome_dir.iterdir()):
                if p.is_dir() and (p / "Preferences").exists():
                    profiles.append(p.name)
    return profiles


def get_available_browsers():
    """Return dict of browser name -> path."""
    browsers = {}
    for name, cmds in [
        ("firefox", ["firefox"]),
        ("chrome", ["google-chrome", "chromium-browser", "chromium"]),
    ]:
        for cmd in cmds:
            if shutil.which(cmd):
                browsers[name] = cmd
                break
    return browsers
