from cf_stats.data.contest_data import ContestData
from cf_stats.utils import cf_api


class CodeforcesDataLoader:
    @staticmethod
    def load_contest_data(contest_id):
        contests = cf_api.api.contest_list(False)
        contest_to_load = next((c for c in contests if c.id == contest_id), None)
        if contest_to_load is None:
            return None

        result = ContestData()
        result.problems = cf_api.api.contest_problems(contest_id)
        result.standings = list(cf_api.api.contest_standings(contest_id)['rows'])
        result.submissions = [s for s in cf_api.api.contest_status(contest_id)
                              if s.author.participant_type == cf_api.ParticipantType.contestant]
        result.hacks = cf_api.api.contest_hacks(contest_id)

        return result
