from unittest import TestCase
from unittest.mock import Mock, patch


from .data_helpers import *
from cf_stats.utils.cf_data_loader import CodeforcesDataLoader


class TestCodeforcesDataLoader(TestCase):
    cf_api_patch = 'cf_stats.utils.cf_data_loader.api'

    @patch(cf_api_patch)
    def test_loading_data_for_non_existing_contest(self, cf_api):
        cf_api.contest_list = Mock(return_value=[])
        cf_api.contest_hacks = Mock()

        result = CodeforcesDataLoader.load_contest_data(10000000000)

        self.assertIsNone(result)
        self.assertFalse(cf_api.contest_hacks.called)

    @patch(cf_api_patch)
    def test_loading_hacks(self, cf_api):
        contest = mock_contest()
        cf_api.contest_list = Mock(return_value=[contest])
        cf_api.contest_status = Mock(return_value="Submissions data")
        cf_api.contest_hacks = Mock(return_value="Hacks data")

        result = CodeforcesDataLoader.load_contest_data(contest.id)

        self.assertIsNotNone(result)
        self.assertEqual(result.submissions, cf_api.contest_status())
        self.assertEqual(result.hacks, cf_api.contest_hacks())
