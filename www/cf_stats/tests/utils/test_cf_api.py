import unittest

from assertpy.assertpy import assert_that
from cf_stats.tests.decorators import slow_test
from cf_stats.utils import cf_api, cf_entities


class TestCfApi(unittest.TestCase):
    @slow_test
    def test_contest_registrants_single_page(self):
        result = cf_api.contest_registrants(1)

        assert_that(result).is_length(175)
        assert_that(result[0].party.members).is_length(1)
        assert_that(result[0].party.members[0].handle).is_equal_to('Igor_Kudryashov')
        assert_that(result[0].party.participant_type).is_equal_to(cf_entities.ParticipantType.contestant)

    @slow_test
    def test_contest_registrants_rating(self):
        result = cf_api.contest_registrants(2)

        assert_that(result[0].rating).is_none()
        assert_that(result[1].rating).is_equal_to(1532)

    @slow_test
    def test_contest_registrants_multiple_pages(self):
        result = cf_api.contest_registrants(2)

        assert_that(result).is_length(269)

    @slow_test
    def test_contest_registrants_out_of_competition(self):
        result = cf_api.contest_registrants(16)

        assert_that(result[4].party.participant_type).is_equal_to(cf_entities.ParticipantType.out_of_competition)

    @slow_test
    def test_contest_registrants_teams(self):
        result = cf_api.contest_registrants(643)
        itmo_team = result[27]

        assert_that(itmo_team.party.team_name).is_equal_to('Never Lucky')
        assert_that(itmo_team.party.members).is_length(2)
        assert_that(itmo_team.party.members[0].handle).is_equal_to('subscriber')
        assert_that(itmo_team.party.members[1].handle).is_equal_to('tourist')

    @slow_test
    def test_contest_registrants_checks_unrated_users_by_zero_rating(self):
        # There is a user with 0 rating registered for this contest but he is not displayed as unrated though.
        # A cheater probably.
        result = cf_api.contest_registrants(777)

        rated_users_with_zero_users = [p for p in result if p.rating == 0]
        assert_that(rated_users_with_zero_users).is_empty()
