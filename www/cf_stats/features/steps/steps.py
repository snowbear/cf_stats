from unittest import mock

from assertpy import assert_that
from behave import *
from datetime import timedelta, datetime

from cf_stats.data.contest_data import ContestData
from cf_stats.utils import stats_extractor, cf_data_loader
from cf_stats.tests.utils import data_helpers


def parse_time(s):
    if s is None or len(s) == 0:
        return None

    date_format = "%H:%M" if len(s) == 5 else "%H:%M:%S"
    date = datetime.strptime(s, date_format)
    return timedelta(hours=date.hour, minutes=date.minute, seconds=date.second)


def parse_submissions(context):
    def get_optional_parameters(row):
        yield ('problem', row.get('problem'))
        yield ('author', row.get('author'))
        yield ('submission_id', row.get('id'))

        relative_time = parse_time(row.get('time'))
        if relative_time is not None:
            yield ('relative_time', int(relative_time.total_seconds()))

        yield ('verdict', row.get('verdict'))

    for row in context.table:
        params = {kvp[0]: kvp[1] for kvp in get_optional_parameters(row) if kvp[1] is not None}
        yield data_helpers.mock_submission(**params)


def setup_problem(context, problem):
    if not hasattr(context, 'problems'):
        context.problems = []

    if problem.index not in (p.index for p in context.problems):
        context.problems.append(problem)
        context.problems.sort(key=lambda p: p.index)


def setup_submission(context, submission):
    setup_problem(context, submission.problem)

    if not hasattr(context, 'submissions'):
        context.submissions = []

    context.submissions.append(submission)


@given("submissions for the contest")
def step_impl(context):
    """ :type context: behave.runner.Context """

    for submission in parse_submissions(context):
        setup_submission(context, submission)


@then('"First accepted" stat should be like this')
def step_impl(context):
    """ :type context: behave.runner.Context """

    contest_data = ContestData()
    contest_data.problems = context.problems
    contest_data.submissions = context.submissions

    stats = stats_extractor.StatsExtractor.first_accepted(contest_data)

    assert_that(stats.items).is_length(len(context.table.rows))
    for i in range(len(context.table.rows)):
        row = context.table[i]
        stats_row = stats.items[i]
        assert_that(stats_row.problem.index).is_equal_to(row['problem'])

        expected_time = parse_time(row['time'])
        if expected_time is not None:
            expected_time = expected_time.total_seconds() // 60

        assert_that(stats_row.relative_time).is_equal_to(expected_time)

        actual_handles = [p.members[0].handle for p in stats_row.parties]
        expected_handles = row['authors'].split()

        assert_that(actual_handles).is_equal_to(expected_handles)


@then("processed submissions should be like")
@mock.patch('cf_stats.utils.cf_data_loader.cf_api.api')
def step_impl(context, cf_api):
    contest = data_helpers.mock_contest()
    cf_api.contest_list.return_value = [contest]
    cf_api.contest_status.return_value = context.submissions
    expected_submissions = list(s.id for s in parse_submissions(context))
    contest_data = cf_data_loader.CodeforcesDataLoader.load_contest_data(1)

    assert_that(contest_data).is_not_none()
    assert_that(contest_data.submissions).extract('id').is_equal_to(expected_submissions)
