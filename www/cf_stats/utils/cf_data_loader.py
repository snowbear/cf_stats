from cf_stats.data.contest_data import ContestData
from cf_stats.utils.cf_api import api


class CodeforcesDataLoader:
    @staticmethod
    def load_contest_data(contest_id):
        contests = api.contest_list(False)
        contest_to_load = next((c for c in contests if c.id == contest_id), None)
        if contest_to_load is None:
            return None
        result = ContestData()
        result.submissions = api.contest_status(contest_id)
        result.hacks = api.contest_hacks(contest_id)

        return result
