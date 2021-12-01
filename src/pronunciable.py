"""
Assumptions:
    - Minimum substring length is 2
References:
    - https://stackoverflow.com/questions/22469997/how-to-get-all-the-contiguous-substrings-of-a-string-in-python
"""

import string
from typing import List, Union


def is_vowel(character: str) -> bool:
    return character in 'aeiouAEIOU'


def is_consonant(character: str) -> bool:
    alphabets = string.ascii_lowercase + string.ascii_uppercase
    return (character in alphabets and not is_vowel(character=character))


def mark_vowels_and_consonants(text: str) -> str:
    """Replaces vowels with 'v' and consonants with 'c'. Other characters will be marked by 'o'."""
    # "".join(('v' if is_vowel(character=character) else 'c' for character in word))
    marked_text = ""
    for character in text:
        if is_vowel(character=character):
            marked_text += 'v'
        elif is_consonant(character=character):
            marked_text += 'c'
        else:
            marked_text += 'o'
    return marked_text


def get_indexes(seq, start=0):
    return (i for i,_ in enumerate(seq, start=start))

def generate_all_substrings(s):
    return (s[i:j] for i in get_indexes(s) for j in get_indexes(s[i:], i+1))

def get_all_substrings(word: str, min_substring_length: int) -> List[str]:
    all_substrings = list(generate_all_substrings(s=word))
    all_substrings = list(filter(lambda substring: len(substring) >= min_substring_length, all_substrings))
    return all_substrings


def is_pronunciable(word: str) -> bool:
    word_length = len(word)
    vowel_and_consonant_marker = mark_vowels_and_consonants(text=word).replace('o', '')
    if word_length < 2:
        return False
    if word_length == 2:
        return 'v' in vowel_and_consonant_marker
    return 'ccc' not in vowel_and_consonant_marker


def get_pronunciable_substrings(all_substrings: List[str]) -> Union[List[str], List]:
    return list(filter(is_pronunciable, all_substrings))


if __name__ == "__main__":
    word = str(input("Word? ")) # ["scrabble", "house"]
    all_substrings = get_all_substrings(word=word, min_substring_length=2)
    pronunciable_substrings = get_pronunciable_substrings(all_substrings=all_substrings)
    print(
        f"Word: '{word}'",
        f"All substrings: {all_substrings}",
        f"Pronunciable substrings: {pronunciable_substrings}",
        sep="\n",
    )