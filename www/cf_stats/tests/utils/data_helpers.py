from unittest import mock as _mock

from cf_stats.utils import cf_api


def _create_mock(mocked_type, values):
    mock = _mock.Mock()

    for property_name in values:
        assert hasattr(mocked_type, property_name), \
            "{class_name} has no property '{property}'".format(class_name=mocked_type, property=property_name)
        mock.__setattr__(property_name, values[property_name])

    return mock


def mock_contest(contest_id=1):
    return _create_mock(cf_api.Contest, {
        'id': contest_id,
    })


def mock_problem(index='A'):
    return _create_mock(cf_api.Problem, {
        'index': index,
    })


def mock_member(handle):
    return _create_mock(cf_api.Member, {
        'handle': handle,
    })


def mock_party(handle):
    return _create_mock(cf_api.Party, {
        'members': [mock_member(handle)],
    })


def mock_submission(author, problem, verdict, relative_time=5*60):
    return _create_mock(cf_api.Submission, {
        'author': author,
        'problem': problem,
        'verdict': verdict,
        'relative_time': relative_time,
    })
