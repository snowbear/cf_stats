import os
from django.conf import settings


class FileStorage:
    @staticmethod
    def get_contest_cache_filename(contest_id):
        return os.path.join(settings.FILE_STORAGE_FOLDER, str(contest_id)+'.html')

    @staticmethod
    def get_contest_stats(contest_id):
        filename = FileStorage.get_contest_cache_filename(contest_id)
        if not os.path.isfile(filename):
            return None

        with open(filename, "r") as cache_file:
            return cache_file.read()
