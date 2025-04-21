#!/usr/bin/env python3

"""
List explicitly installed (manually selected) packages on a Debian system,
along with their versions.
REPO with Tests and README.md at: https://github.com/WarrenU/list-manual-packages
Target: Debian 12
Author: Warren Urbina
"""

import os
from typing import List, Dict

# Path to the APT extended states file to get EXPLICITLY installed packages (Auto-Installed: 0)
EXTENDED_STATES_PATH = "/var/lib/apt/extended_states"
# Path to the dpkg status file for package metadata (including versions of the packages)
DPKG_STATUS_PATH   = "/var/lib/dpkg/status"


def parse_extended_states() -> List[str]:
    """
    Parse /var/lib/apt/extended_states to find manually installed packages.
    Returns a list of package names where 'Auto-Installed: 0' meaning it's manually installed.
    """
    manually_installed = []
    current_package = None

    with open(EXTENDED_STATES_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Package:"):
                current_package = line.split(":", 1)[1].strip()
            elif line.startswith("Auto-Installed:") and current_package:
                if line.split(":", 1)[1].strip() == "0":
                    manually_installed.append(current_package)
                current_package = None

    return manually_installed


def parse_dpkg_status() -> Dict[str, str]:
    """
    Parse /var/lib/dpkg/status to build a map of package to version.
    Returns a dict where keys are package names and values are version strings.
    """
    versions: Dict[str, str] = {}
    pkg_name = None

    with open(DPKG_STATUS_PATH, "r") as f:
        for line in f:
            if line.startswith("Package:"):
                pkg_name = line.split(":", 1)[1].strip()
            elif line.startswith("Version:") and pkg_name:
                versions[pkg_name] = line.split(":", 1)[1].strip()
                pkg_name = None

    return versions


def main():
    manual_pkgs = parse_extended_states()
    all_versions = parse_dpkg_status()

    print("Manually installed packages (with versions):\n")
    for pkg in sorted(manual_pkgs):
        version = all_versions.get(pkg, "unknown")
        print(f"{pkg} ({version})")


if __name__ == "__main__":
    main()
