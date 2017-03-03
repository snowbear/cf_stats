# noinspection PyUnresolvedReferences
from codeforces.api.json_objects import RanklistRow, Party, Member, Contest, Problem, Submission, \
    ParticipantType, VerdictType


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
