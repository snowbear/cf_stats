import os
from unittest import TestCase

from assertpy import assert_that
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

    def test_save_contest_date(self):
        contest_id = 5
        filename = FileStorage.get_contest_cache_filename(contest_id)

        content = 'some html'

        with TempFile(filename):
            FileStorage.save_contest_data(contest_id, content)
            with open(filename, "r") as text_file:
                actual_content = text_file.read()
                assert_that(actual_content).is_equal_to(content)


class TempFile:
    def __init__(self, filename, file_content=None):
        self.filename = filename
        with open(filename, "w") as text_file:
            if file_content is not None:
                text_file.write(file_content)

    def __enter__(self):
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, *args):
        os.remove(self.filename)
