import datetime


def format_time(timedelta):
    s = int(timedelta.total_seconds())
    h = s // 60 // 60
    m = s // 60 % 60
    return "({h:02}:{m:02})".format(h=h, m=m)


class RenderingItemBase:
    def render(self):
        raise NotImplementedError()


class Br(RenderingItemBase):
    def render(self):
        return "<br />"


class List(RenderingItemBase):
    def __init__(self, separator, *items):
        assert isinstance(separator, (str, RenderingItemBase))

        self.separator = separator
        self.items = items

    def render(self):
        separator = self.separator if isinstance(self.separator, str) else self.separator.render()
        return separator.join(i.render() for i in self.items)


class Text(RenderingItemBase):
    def __init__(self, text, bold=False):
        self.text = text
        self.bold = bold

    def render(self):
        result = self.text
        if self.bold:
            result = "<b>{0}</b>".format(result)
        return result


class Party(RenderingItemBase):
    def __init__(self, party):
        self.party = party

    def render(self):
        return "<a>{name}<a>".format(name=self.party.party_name)


class FirstAcceptedStatRow(RenderingItemBase):
    def __init__(self, problem, relative_time, parties):
        self.problem = problem
        self.relative_time = relative_time
        self.parties = parties

    def render(self):
        problem_caption = Text(self.problem.index, bold=True)
        if self.relative_time is None:
            return problem_caption.render()
        else:
            formatted_time = format_time(datetime.timedelta(minutes=self.relative_time))
            return List(' - ',
                        problem_caption,
                        Text(formatted_time),
                        List(' ', *[Party(p) for p in self.parties])).render()


class TopHackerStatRow(RenderingItemBase):
    def __init__(self, hack_score, party, hacks_plus, hacks_minus):
        self.hack_score = hack_score
        self.party = party
        self.hacks_plus = hacks_plus
        self.hacks_minus = hacks_minus

    def render(self):
        return List(' ',
                    Text(str(self.hack_score), bold=True),
                    Party(self.party),
                    Text("+{p}:-{n}".format(p=self.hacks_plus, n=self.hacks_minus))).render()
