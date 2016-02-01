from . import cf_api, rendering


def _first_accepted_per_problem(contest_data, problem):
    this_problems_submissions = [s for s in contest_data.submissions
                                 if s.problem == problem and
                                 s.verdict == cf_api.VerdictType.ok]
    min_time_in_minutes = min((s.relative_time // 60 for s in this_problems_submissions), default=None)
    if min_time_in_minutes is None:
        return rendering.FirstAcceptedStatRow(problem, None, [])

    this_problems_submissions = [s for s in this_problems_submissions
                                 if s.relative_time // 60 == min_time_in_minutes]

    this_problems_submissions.sort(key=lambda s: (s.relative_time, s.author.party_name))

    first_solvers = [s.author for s in this_problems_submissions]

    return rendering.FirstAcceptedStatRow(problem,
                                          min_time_in_minutes,
                                          first_solvers)


class StatsExtractor:
    @staticmethod
    def first_accepted(contest_data):
        rows = list(_first_accepted_per_problem(contest_data, p) for p in contest_data.problems)
        return rendering.List(rendering.Br(), *rows)

    @staticmethod
    def extract_contest_stats(contest_data):
        raise NotImplementedError()
