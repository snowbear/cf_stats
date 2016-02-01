class Br:
    def __repr__(self, *args, **kwargs):
        return "Br"


class List:
    def __init__(self, separator, *items):
        self.separator = separator
        self.items = items

    def __repr__(self):
        return "List({separator}, {items})".format(separator=self.separator.__repr__(),
                                                   items=','.join(i.__repr__() for i in self.items))


class Text:
    def __init__(self, text):
        self.text = text

    def __repr__(self, *args, **kwargs):
        return "Text({text})".format(text=self.text.__repr__())


class Party:
    def __init__(self, party):
        self.party = party

    def __repr__(self, *args, **kwargs):
        return "[{handle}]".format(handle=self.party.members[0].handle)


class FirstAcceptedStatRow:
    def __init__(self, problem, relative_time, parties):
        self.problem = problem
        self.relative_time = relative_time
        self.parties = parties
