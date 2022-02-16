# Film.py


class Film:
    """
    Film class
    """
    def __init__(self, title=None, year=None, link=None, rating=None):
        self.title = title
        self.year = year
        self.link = link
        self.rating = rating
        self.torrents = []

    def title(self, title=None):
        if title is None:
            return self.title
        self.title = title

    def link(self, link=None):
        if link is None:
            return self.link
        self.link = link

    def year(self, year=None):
        if year is None:
            return self.year
        self.year = year

    def rating(self, rating=None):
        if rating is None:
            return self.rating
        self.rating = rating

    def __repr__(self):
        return '<Film.title {}>'.format(self.title)
