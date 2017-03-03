from . import cf_entities, rendering


def _first_accepted_per_problem(contest_data, problem):
    this_problems_submissions = [s for s in contest_data.submissions
                                 if s.problem == problem and
                                 s.verdict == cf_entities.VerdictType.ok]
    min_time_in_minutes = min((s.relative_time // 60 for s in this_problems_submissions), default=None)
    if min_time_in_minutes is None:
        return rendering.FirstAcceptedStatRow(problem, None, [])

    this_problems_submissions = [s for s in this_problems_submissions
                                 if s.relative_time // 60 == min_time_in_minutes]

    this_problems_submissions.sort(key=lambda s: (s.relative_time, s.author))

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
    def top_hackers(contest_data):
        hackers = [rendering.TopHackerStatRow(100*s.successful_hack_count - 50*s.unsuccessful_hack_count,
                                              s.party,
                                              s.successful_hack_count,
                                              s.unsuccessful_hack_count)
                   for s in contest_data.standings]
        hackers.sort(key=lambda h: (-h.hack_score, -h.hacks_plus, h.party))

        lowest_score_to_show = max(hackers[min(4, len(hackers) - 1)].hack_score,
                                   1)
        hackers = [h for h in hackers if h.hack_score >= lowest_score_to_show]
        hackers = hackers[:10]

        return rendering.List(rendering.Br(), *hackers)

    @staticmethod
    def extract_contest_stats(contest_data):
        return rendering.List(rendering.Br(),
                              StatsExtractor.first_accepted(contest_data),
                              StatsExtractor.top_hackers(contest_data),
                              )
