"""Module for custom exceptions"""

class UrlsNotFoundError(Exception):
    pass


class UrlWithExactNameNotFoundError(Exception):
    pass


class CannotScrapeWikipediaError(Exception):
    pass


class InvalidLiftRequestError(Exception):
    pass