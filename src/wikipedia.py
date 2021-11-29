"""
References:
    - https://stackoverflow.com/questions/14596884/remove-text-between-and
"""

from typing import Dict, List, Union

from bs4 import BeautifulSoup
from collections import Counter
import re
import requests

from errors import CannotScrapeWikipediaError


def remove_text_in_square_brackets(text: str) -> str:
    text_new = re.sub(pattern=r"([\[]).*?([\]])", repl="\g<1>\g<2>", string=text)
    text_new = text_new.replace("[]", '')
    return text_new


def is_paragraph_with_actual_content(text_in_paragraph: str) -> bool:
    return text_in_paragraph.strip() != ''


def get_paragraphs_in_wiki_page(url_from_wikipedia: str) -> Union[List[str], List]:
    """Returns list of paragraphs scraped from the given Wikipedia page. Could return an empty list."""
    response = requests.get(url=url_from_wikipedia)
    if not response.ok:
        raise CannotScrapeWikipediaError(f"No paragraphs were scraped from the given Wikipedia page. Response status code: {response.status_code}")
    dom = BeautifulSoup(markup=response.content, features='html.parser')
    text_in_paragraphs = [paragraph.get_text() for paragraph in dom.find_all(name='p')]
    text_in_paragraphs = list(filter(is_paragraph_with_actual_content, text_in_paragraphs))
    text_in_paragraphs = list(map(remove_text_in_square_brackets, text_in_paragraphs))
    return text_in_paragraphs


def get_word_character_count_frequency(words: List[str]):
    """Returns dictionary having keys = number of characters in the word; and values = number of words with the exact number of characters"""
    word_char_count = list(map(len, words))
    return dict(Counter(word_char_count))


def get_avg_word_length_frequency(paragraphs: List[str]) -> Dict[int, Union[int, float]]:
    num_paragraphs = len(paragraphs)
    all_words = []
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        all_words.extend(words)
    word_character_count_frequency = get_word_character_count_frequency(words=all_words)
    word_character_count_per_paragraph = {}
    num_desired_chars_per_word = [3, 4, 5]
    for char_count, word_count in word_character_count_frequency.items():
        if char_count in num_desired_chars_per_word:
            word_character_count_per_paragraph[char_count] = round(word_count / num_paragraphs, 3)
    return word_character_count_per_paragraph


if __name__ == "__main__":
    # url_from_wikipedia = "https://en.wikipedia.org/wiki/Earth"
    # url_from_wikipedia = "https://en.wikipedia.org/wiki/FC_Bayern_Munich"
    url_from_wikipedia = str(input("Enter Wikipedia page URL? "))
    
    paragraphs = get_paragraphs_in_wiki_page(url_from_wikipedia=url_from_wikipedia)
    avg_word_length_freq = get_avg_word_length_frequency(paragraphs=paragraphs)
    for word_length, word_freq_per_paragraph in avg_word_length_freq.items():
        print(f"There are {word_freq_per_paragraph} {word_length}-letter words per paragraph")