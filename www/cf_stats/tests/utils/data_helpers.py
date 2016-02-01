from cf_stats.utils import cf_api


def mock_contest():
    contest = cf_api.Contest()
    contest.id = 1
    return contest


def mock_problem(data='A'):
    if isinstance(data, cf_api.Problem):
        return data

    assert isinstance(data, str)

    problem = cf_api.Problem()
    problem.index = data
    return problem


def mock_member(data='CF mocked member'):
    if isinstance(data, cf_api.Member):
        return data

    assert isinstance(data, str)

    member = cf_api.Member()
    member.handle = data
    return member


def mock_party(data='CF mocked party'):
    if isinstance(data, cf_api.Party):
        return data

    party = cf_api.Party()
    party.members = [mock_member(data)]
    return party


def mock_submission(author='author', problem='A', verdict=cf_api.VerdictType.ok, relative_time=5*60):
    author = mock_party(author)

    problem = mock_problem(problem)

    assert isinstance(verdict, (cf_api.VerdictType, str))
    if not isinstance(verdict, cf_api.VerdictType):
        verdict = cf_api.VerdictType(verdict)

    assert isinstance(relative_time, int)

    submission = cf_api.Submission()
    submission.author = author
    submission.problem = problem
    submission.verdict = verdict
    submission.relative_time = relative_time
    return submission
