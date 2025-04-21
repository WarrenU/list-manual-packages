# list-manual-packages

A small Python 3 script that lists packages manually installed by the user on Debian. This script parses the underlying APT metadata file at `/var/lib/apt/extended_states`.
Project Repo Available at: https://github.com/WarrenU/list-manual-packages

## What it Does

Debian marks packages as "automatically installed" when pulled in as dependencies. This script filters those out and returns only the explicitly installed packages.

It behaves similarly to Gentoo's [selected set](https://wiki.gentoo.org/wiki/Selected_set_(Portage)).

## How to Install

To build and install the package:

```bash
dpkg-buildpackage -us -uc -b
sudo dpkg -i ../list-manual-packages_1.0_all.deb
```

##  How to Run
Once installed, run the script with:

`list_manual_packages.py`

Or directly via Python:

`python3 /usr/bin/list_manual_packages.py`

The script will output a list of explicitly installed packages, one per line.

## Tested On
Debian 12 (Bookworm)

## Notes
Make sure you have python3 installed (should be default on Debian 12).

You can redirect the output to a file if needed:
`list_manual_packages.py > manual-packages.txt`

## Running Unit Tests (Not included in debian package):

To run tests with verbose output:

```bash
python3 -m unittest discover -s tests -v
Expected output will look like:
```


```bash
test_manual_packages (test_list_manual_packages.TestListManualPackages.test_manual_packages) ... ok
test_manual_packages_with_versions (test_list_manual_packages.TestListManualPackages.test_manual_packages_with_versions) ... ok
test_parse_dpkg_status (test_list_manual_packages.TestListManualPackages.test_parse_dpkg_status) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.002s
OK
```