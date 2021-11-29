"""
Assumptions:
    - Minimum substring length is 2
References:
    - https://stackoverflow.com/questions/22469997/how-to-get-all-the-contiguous-substrings-of-a-string-in-python
"""

from typing import List, Union


def is_vowel(character: str) -> bool:
    return character in 'aeiouAEIOU'


def get_indexes(seq, start=0):
    return (i for i,_ in enumerate(seq, start=start))

def generate_all_substrings(s):
    return (s[i:j] for i in get_indexes(s) for j in get_indexes(s[i:], i+1))

def get_all_substrings(word: str, min_substring_length: int) -> List[str]:
    all_substrings = list(generate_all_substrings(s=word))
    all_substrings = list(filter(lambda substring: len(substring) >= min_substring_length, all_substrings))
    return all_substrings


def is_pronunciable(word: str) -> bool:
    """
    Word is said to be pronunciable if it has at-least 1 vowel after at-most 2 consonants.
    i.e; must not have 3 or more consecutive consonants.
    """
    # return 'ccc' not in "".join(('v' if is_vowel(character=character) else 'c' for character in text))
    consecutive_consonant_count = 0
    for character in word:
        if is_vowel(character=character):
            consecutive_consonant_count = 0
        else:
            consecutive_consonant_count += 1
            if consecutive_consonant_count == 3:
                return False
    return True


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