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
    party.participant_type = cf_api.ParticipantType.contestant

    special_symbols_for_participant_type = {
        '*': cf_api.ParticipantType.out_of_competition,
        '#': cf_api.ParticipantType.virtual,
    }

    if isinstance(data, str) and data[-1] in special_symbols_for_participant_type:
        party.participant_type = special_symbols_for_participant_type[data[-1]]
        data = data[0:-1]

    party.members = [mock_member(data)]

    return party


def mock_submission(submission_id=1, author='author', problem='A', verdict=cf_api.VerdictType.ok, relative_time=5*60):
    author = mock_party(author)

    problem = mock_problem(problem)

    assert isinstance(verdict, (cf_api.VerdictType, str))
    if not isinstance(verdict, cf_api.VerdictType):
        verdict = cf_api.VerdictType(verdict)

    assert isinstance(relative_time, int)

    submission = cf_api.Submission()
    submission.id = submission_id
    submission.author = author
    submission.problem = problem
    submission.verdict = verdict
    submission.relative_time = relative_time
    return submission


def mock_standing(party='contestant', successful_hacks=0, unsuccessful_hacks=0):
    party = mock_party(party)
    successful_hacks = int(successful_hacks)
    unsuccessful_hacks = int(unsuccessful_hacks)

    standing = cf_api.RanklistRow()
    standing.party = party
    standing.successful_hack_count = successful_hacks
    standing.unsuccessful_hack_count = unsuccessful_hacks
    return standing
