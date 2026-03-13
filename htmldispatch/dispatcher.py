import re
import subprocess

from .config import load_config
from .history import add_entry


def find_matching_rule(url):
    config = load_config()
    for rule in config.get("rules", []):
        if re.search(rule["pattern"], url):
            return rule
    return None


def open_url(url, browser, profile=None, rule_name=None):
    cmd = build_command(browser, profile, url)
    subprocess.Popen(cmd)
    add_entry(url, browser, profile, rule_name)


def build_command(browser, profile, url):
    if browser == "firefox":
        cmd = ["firefox"]
        if profile:
            cmd += ["-P", profile]
        cmd.append(url)
        return cmd
    elif browser == "chrome":
        cmd = ["google-chrome"]
        if profile:
            cmd += [f"--profile-directory={profile}"]
        cmd.append(url)
        return cmd
    else:
        return [browser, url]


def dispatch(url):
    """Try to dispatch URL by rules. Returns True if matched, False if not."""
    rule = find_matching_rule(url)
    if rule:
        open_url(url, rule["browser"], rule.get("profile"), rule.get("name"))
        return True
    config = load_config()
    if not config.get("popup_on_unknown", True):
        browser = config.get("default_browser", "firefox")
        profile = config.get("default_profile")
        open_url(url, browser, profile, "default")
        return True
    return False
