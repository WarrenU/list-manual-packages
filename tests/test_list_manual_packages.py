import unittest
import tempfile
import os
import sys
import textwrap

# Ensure the script directory is on the import path
SCRIPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'usr', 'bin')
)
sys.path.insert(0, SCRIPT_DIR)

import list_manual_packages

class TestListManualPackages(unittest.TestCase):
    def setUp(self):
        # 1) Prepare extended_states tempfile
        self.extended = tempfile.NamedTemporaryFile(delete=False)
        sample_ext = textwrap.dedent("""\
            Package: pkgA
            Auto-Installed: 0

            Package: pkgB
            Auto-Installed: 1

            Package: pkgC
            Auto-Installed: 0
        """)
        self.extended.write(sample_ext.encode('utf-8'))
        self.extended.flush()
        self.extended.close()

        # Monkey‑patch the EXTENDED_STATES_PATH
        self.orig_extended = list_manual_packages.EXTENDED_STATES_PATH
        list_manual_packages.EXTENDED_STATES_PATH = self.extended.name

        # 2) Prepare dpkg status tempfile
        self.status = tempfile.NamedTemporaryFile(delete=False)
        sample_status = textwrap.dedent("""\
            Package: pkgA
            Version: 1.2.3

            Package: pkgB
            Version: 2.3.4

            Package: pkgC
            Version: 3.4.5
        """)
        self.status.write(sample_status.encode('utf-8'))
        self.status.flush()
        self.status.close()

        # Monkey‑patch the DPKG_STATUS_PATH
        self.orig_status = list_manual_packages.DPKG_STATUS_PATH
        list_manual_packages.DPKG_STATUS_PATH = self.status.name

    def tearDown(self):
        os.unlink(self.extended.name)
        os.unlink(self.status.name)
        list_manual_packages.EXTENDED_STATES_PATH = self.orig_extended
        list_manual_packages.DPKG_STATUS_PATH = self.orig_status

    def test_manual_packages(self):
        manual = list_manual_packages.parse_extended_states()
        # Expect only pkgA and pkgC
        self.assertCountEqual(manual, ['pkgA', 'pkgC'])

    def test_parse_dpkg_status(self):
        versions = list_manual_packages.parse_dpkg_status()
        # All three packages should be present with correct versions
        self.assertEqual(versions['pkgA'], '1.2.3')
        self.assertEqual(versions['pkgB'], '2.3.4')
        self.assertEqual(versions['pkgC'], '3.4.5')

    def test_manual_packages_with_versions(self):
        manual = list_manual_packages.parse_extended_states()
        versions = list_manual_packages.parse_dpkg_status()
        # Build a dict of only the manually installed packages and their versions
        manual_with_versions = {pkg: versions[pkg] for pkg in manual}
        self.assertEqual(manual_with_versions, {
            'pkgA': '1.2.3',
            'pkgC': '3.4.5'
        })

if __name__ == '__main__':
    unittest.main()
