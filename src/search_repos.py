from typing import List, Union

from bs4 import BeautifulSoup
import requests

from errors import UrlWithExactNameNotFoundError, UrlsNotFoundError


def is_valid_url(url: str) -> bool:
    url = url.strip()
    if url == '':
        return False
    if url[0] == '#':
        return False
    return True


def get_urls_in_github_repo(url_of_repository: str) -> Union[List[str], List]:
    """Returns list of URLs scraped from the given GitHub repository. Could return an empty list."""
    response = requests.get(url=url_of_repository)
    if not response.ok:
        raise UrlsNotFoundError(f"No URLs were scraped from the given GitHub repository: '{url_of_repository}'. Response status code: {response.status_code}")
    dom = BeautifulSoup(markup=response.content, features='html.parser')
    links = [link['href'] for link in dom.find_all(name='a', href=True)]
    links = list(filter(is_valid_url, links))
    return links


def search_url_by_exact_name(list_of_urls: List[str], name_to_find: str) -> str:
    for url in list_of_urls:
        if name_to_find in url.split('/'):
            return url
    raise UrlWithExactNameNotFoundError("Desired URL not found")


if __name__ == "__main__":
    name_to_find = str(input("Query? ")) # ["graphene", "stackless", "algorithms"]
    urls = get_urls_in_github_repo(url_of_repository="https://github.com/vinta/awesome-python")
    url_searched = search_url_by_exact_name(list_of_urls=urls, name_to_find=name_to_find)
    print(f"Desired URL: {url_searched}")