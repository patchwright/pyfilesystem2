from __future__ import unicode_literals

import unittest

from fs import filesize


class TestFilesize(unittest.TestCase):
    def test_traditional(self):

        self.assertEqual(filesize.traditional(0), "0 bytes")
        self.assertEqual(filesize.traditional(1), "1 byte")
        self.assertEqual(filesize.traditional(2), "2 bytes")
        self.assertEqual(filesize.traditional(1024), "1.0 KB")

        self.assertEqual(filesize.traditional(1024 * 1024), "1.0 MB")

        self.assertEqual(filesize.traditional(1024 * 1024 + 1), "1.0 MB")

        self.assertEqual(filesize.traditional(1.5 * 1024 * 1024), "1.5 MB")

    def test_binary(self):

        self.assertEqual(filesize.binary(0), "0 bytes")
        self.assertEqual(filesize.binary(1), "1 byte")
        self.assertEqual(filesize.binary(2), "2 bytes")
        self.assertEqual(filesize.binary(1024), "1.0 KiB")

        self.assertEqual(filesize.binary(1024 * 1024), "1.0 MiB")

        self.assertEqual(filesize.binary(1024 * 1024 + 1), "1.0 MiB")

        self.assertEqual(filesize.binary(1.5 * 1024 * 1024), "1.5 MiB")

    def test_decimal(self):

        self.assertEqual(filesize.decimal(0), "0 bytes")
        self.assertEqual(filesize.decimal(1), "1 byte")
        self.assertEqual(filesize.decimal(2), "2 bytes")
        self.assertEqual(filesize.decimal(1000), "1.0 kB")

        self.assertEqual(filesize.decimal(1000 * 1000), "1.0 MB")

        self.assertEqual(filesize.decimal(1000 * 1000 + 1), "1.0 MB")

        self.assertEqual(filesize.decimal(1200 * 1000), "1.2 MB")

    def test_rollover_decimal(self):
        # Mantissa rounds up to base — must carry to the next suffix
        self.assertEqual(filesize.decimal(999_999), "1.0 MB")
        self.assertEqual(filesize.decimal(999_999_999), "1.0 GB")
        self.assertEqual(filesize.decimal(999_999_999_999), "1.0 TB")

    def test_rollover_traditional(self):
        # 1024**2 - 1 bytes is 1023.999 KB, which rounds to 1,024.0 KB
        self.assertEqual(filesize.traditional(1024**2 - 1), "1.0 MB")
        self.assertEqual(filesize.traditional(1024**3 - 1), "1.0 GB")

    def test_rollover_binary(self):
        self.assertEqual(filesize.binary(1024**2 - 1), "1.0 MiB")
        self.assertEqual(filesize.binary(1024**3 - 1), "1.0 GiB")

    def test_errors(self):

        with self.assertRaises(TypeError):
            filesize.traditional("foo")
