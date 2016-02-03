from unittest import TestCase
from unittest.mock import patch

from assertpy import assert_that
from cf_stats.utils.cf_data_loader import CodeforcesDataLoader


class TestCodeforcesDataLoader(TestCase):
    cf_api_patch = 'cf_stats.utils.cf_data_loader.cf_api.api'

    @patch(cf_api_patch)
    def test_loading_data_for_non_existing_contest(self, cf_api):
        cf_api.contest_list.return_value = []

        result = CodeforcesDataLoader.load_contest_data(10000000000)

        assert_that(result).is_none()
        assert_that(cf_api.contest_hacks.called).is_false()
