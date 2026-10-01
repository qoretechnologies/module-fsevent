#!/usr/bin/env python3
"""Exercise the bundled POSIX realpath helper, including failing resolutions.

Copyright (C) 2026 Qore Technologies, s.r.o.
"""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name == "posix", "POSIX realpath contract")
class RealPathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="efsw-realpath-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.probe = cls.root / "realpath-probe"
        # Compile the production translation unit. Section garbage collection
        # isolates this helper from unrelated file-watcher platform services.
        subprocess.run([os.environ.get("CXX", "c++"), "-std=c++11", "-g", "-O2",
                        "-Wall", "-Wextra", "-Werror", "-ffunction-sections",
                        "-fdata-sections", "-Wl,--gc-sections",
                        "-I" + str(ROOT / "src"), "-I" + str(ROOT / "src/include"),
                        str(ROOT / "test/realpath-probe.cpp"),
                        str(ROOT / "src/efsw/FileSystem.cpp"), "-o", str(cls.probe)], check=True)

    def resolve(self, path):
        command = [str(self.probe), str(path)]
        if os.environ.get("QORE_TEST_VALGRIND") == "1":
            command = ["valgrind", "--quiet", "--leak-check=full",
                       "--show-leak-kinds=all", "--errors-for-leak-kinds=all",
                       "--error-exitcode=99", *command]
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
        self.assertEqual("", result.stderr)
        return result.stdout.removesuffix("\n")

    def test_existing_directory(self):
        self.assertEqual(str(self.root.resolve()), self.resolve(self.root / "."))

    def test_existing_file_and_symlink(self):
        target = self.root / "file with spaces"
        target.write_text("fixture")
        link = self.root / "link"
        link.symlink_to(target)
        self.assertEqual(str(target.resolve()), self.resolve(link))

    def test_missing_and_empty_paths(self):
        for path in ("", self.root / "absent", self.root / "absent/child"):
            with self.subTest(path=path):
                self.assertEqual("", self.resolve(path))

    def test_broken_and_looping_symlinks(self):
        broken = self.root / "broken"
        broken.symlink_to(self.root / "missing-target")
        loop = self.root / "loop"
        loop.symlink_to(loop)
        for path in (broken, loop):
            with self.subTest(path=path):
                self.assertEqual("", self.resolve(path))

    def test_path_too_long(self):
        self.assertEqual("", self.resolve(str(self.root) + "/" + "a" * 8192))


if __name__ == "__main__":
    unittest.main()
