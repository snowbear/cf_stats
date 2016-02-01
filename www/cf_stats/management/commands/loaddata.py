from django.core.management.base import BaseCommand

from cf_stats.utils.cf_data_loader import CodeforcesDataLoader
from cf_stats.utils.stats_extractor import StatsExtractor
from cf_stats.utils.storage import FileStorage


class Command(BaseCommand):
    help = 'Loads data for a single contest'

    def add_arguments(self, parser):
        parser.add_argument('contest_id', type=int)

    def handle(self, contest_id, *args, **options):
        contest_data = CodeforcesDataLoader.load_contest_data(contest_id)
        if contest_data is None:
            self.stdout.write('Contest with id {contest_id} was not found'.format(contest_id=contest_id))
            return

        contest_stats = StatsExtractor.extract_contest_stats(contest_data)
        html_output = contest_stats.render()
        FileStorage.save_contest_data(contest_id, html_output)
