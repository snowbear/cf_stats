import codeforces

# noinspection PyUnresolvedReferences
from codeforces.api.json_objects import RanklistRow, Party, Member, Contest, Problem, Submission, \
    ParticipantType, VerdictType


def contest_problems(self, contest_id):
    return self.contest_standings(contest_id, from_=1, count=1)['problems']


codeforces.CodeforcesAPI.contest_problems = contest_problems


api = codeforces.CodeforcesAPI()


@property
def party_name(self):
    if self.team_name is not None:
        return self.team_name
    assert len(self.members) == 1
    return self.members[0].handle


def party_le_comparer(self, other):
    if not isinstance(other, Party):
        return NotImplemented
    return self.party_name < other.party_name


Party.party_name = party_name
Party.__lt__ = party_le_comparer
