from django.utils.six import StringIO

from unittest import TestCase
from unittest.mock import Mock, patch

from django.core.management import call_command


class TestCommand(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.contest_id = 5

    def execute_command(self):
        call_command('loaddata', str(self.contest_id), stdout=self.out)

    @patch('cf_stats.management.commands.loaddata.CodeforcesDataLoader')
    def test_does_nothing_for_non_existing_contest(self, cf_data_loader):
        cf_data_loader.load_contest_data = Mock(return_value=None)

        self.execute_command()

        output = self.out.getvalue()
        self.assertIn('Contest with id ' + str(self.contest_id) + ' was not found', output)
        cf_data_loader.load_contest_data.assert_called_once_with(self.contest_id)

    @patch('cf_stats.management.commands.loaddata.FileStorage')
    @patch('cf_stats.management.commands.loaddata.StatsExtractor')
    @patch('cf_stats.management.commands.loaddata.CodeforcesDataLoader')
    def test_command_execution(self, cf_data_loader, stats_extractor, file_storage):
        cf_data_loader.load_contest_data = Mock(return_value="Contest data")
        contest_stats = Mock()
        contest_stats.render = Mock(return_value="Html output")
        stats_extractor.extract_contest_stats = Mock(return_value=contest_stats)

        self.execute_command()

        cf_data_loader.load_contest_data.assert_called_once_with(self.contest_id)
        stats_extractor.extract_contest_stats.assert_called_once_with(cf_data_loader.load_contest_data())
        contest_stats.render.assert_called_once_with()
        file_storage.save_contest_data.assert_called_once_with(self.contest_id, contest_stats.render())
