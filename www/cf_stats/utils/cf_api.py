import codeforces


_cf_api = codeforces.CodeforcesAPI()


def contest_list():
    return codeforces.CodeforcesAPI().contest_list(False)


def contest_problems(contest_id):
    return _cf_api.contest_standings(contest_id, from_=1, count=1)['problems']


def contest_standings(contest_id):
    return _cf_api.contest_standings(contest_id)['rows']


def contest_status(contest_id):
    return _cf_api.contest_status(contest_id)


def contest_hacks(contest_id):
    return _cf_api.contest_hacks(contest_id)
