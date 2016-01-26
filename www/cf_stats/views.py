from django import http, shortcuts

from cf_stats.utils.storage import FileStorage


def index(request):
    return http.HttpResponse("Hello")


def contest_view(request, contest_id):
    contest_id = int(contest_id)

    content = FileStorage.get_contest_stats(contest_id)

    if content is None:
        return shortcuts.render(request, 'cf_stats/contest_data_not_present.html')

    return http.HttpResponse(content)
