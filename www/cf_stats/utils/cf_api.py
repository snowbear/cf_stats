import codeforces

# noinspection PyUnresolvedReferences
from codeforces.api.json_objects import Party, Member, Contest, Problem, Submission, VerdictType


api = codeforces.CodeforcesAPI()


@property
def party_name(self):
    if self.team_name is not None:
        return self.team_name
    assert len(self.members) == 1
    return self.members[0].handle


Party.party_name = party_name
