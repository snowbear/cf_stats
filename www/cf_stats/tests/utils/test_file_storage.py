import os
from unittest import TestCase

from cf_stats.utils.storage import FileStorage


class TestFileStorage(TestCase):
    def test_returns_contest_file_if_present(self):
        contest_id = 5
        file_content = "string 1\nstring 2"

        filename = FileStorage.get_contest_cache_filename(contest_id)

        with TempFile(filename, file_content):
            result = FileStorage.get_contest_stats(contest_id)

        self.assertEqual(result, file_content)

    def test_returns_none_if_file_is_not_present(self):
        contest_id = 5
        filename = FileStorage.get_contest_cache_filename(contest_id)

        self.assertFalse(os.path.isfile(filename))

        result = FileStorage.get_contest_stats(contest_id)
        self.assertIsNone(result)


class TempFile:
    def __init__(self, filename, file_content):
        self.filename = filename
        with open(filename, "w") as text_file:
            text_file.write(file_content)

    def __enter__(self):
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, *args):
        os.remove(self.filename)
