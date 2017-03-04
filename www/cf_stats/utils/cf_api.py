import requests

import codeforces
from cf_stats.utils import cf_entities
from lxml import html


_cf_api = codeforces.CodeforcesAPI()


def _get_cf_page(url):
    return requests.get(url)


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


def contest_registrants(contest_id):
    """
    :type contest_id: int
    :rtype: list of cf_entities.ContestRegistration
    """
    def parse_contestant(row):
        rating_value = int(row.xpath('td[3]/text()')[0])
        is_rated = rating_value > 0
        is_out_of_competition = row.xpath('@class="out-of-competition"')
        is_team = row.xpath('td[2]//a[starts-with(@href, "/team/")]')

        members = \
            [cf_entities.Member({'handle': s[9:]}) for s in
                row.xpath('td[2]//a[starts-with(@href, "/profile/")]/@href')]\
            if is_team else \
            [cf_entities.Member({'handle': row.xpath('td[2]/a/text()')[0]})]
        return cf_entities.ContestRegistration(
            codeforces.Party({
                'contestId': contest_id,
                'members': members,
                'participantType':
                    cf_entities.ParticipantType.out_of_competition if is_out_of_competition
                    else cf_entities.ParticipantType.contestant,
                'ghost': False,
                'teamName': row.xpath('td//a[1]/text()')[0] if is_team else None,
            }),
            rating_value if is_rated else None,
        )

    result = []
    page = 1
    num_pages = None
    while num_pages is None or page <= num_pages:
        url = "http://codeforces.com/contestRegistrants/{0}/page/{1}".format(contest_id, page)
        response = _get_cf_page(url)
        tree = html.fromstring(response.text)
        if num_pages is None:
            pages = tree.xpath('//div[@class="pagination"]/ul/li/span[@class="page-index"]/a/text()')
            num_pages = int(pages[-1]) if pages else 1

        current_page = [parse_contestant(r) for r in tree.xpath('//table[@class="registrants"]/tr[position()>1]')]
        result.extend(current_page)
        page += 1
    return result
