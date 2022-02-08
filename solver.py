#!/usr/bin/env python3
"""Wordle Solver

# Usage example:

We know we need "r", but not in the 1st position. We also need "l",
but not in the 5th position. We have already established that "o" is
in position 2 and "a" is in position 4.

$ ./solver.py -1 r -5 l -a udiceny -s _o_a_
=== 2 ===
lobar
molar
polar
solar
volar
$

From the results, we can see the answer must be one of these
options. All candidates contain 2 unique vowels.
"""

import argparse
import os
import string
import sys
from pathlib import Path


DICT_FILE = "share/dict.lst"
VOWELS = "aeiou"
WORD_LENGTH = 5


class Word(str):
    """Word class"""

    vowels = VOWELS

    @property
    def get_unique_vowel_count(self):
        """Return a count of unique vowels in the word"""
        vowel_count = 0
        for vowel in self.vowels:
            if vowel in self.__str__():
                vowel_count += 1
        return vowel_count

    def get_vowels(self):
        """Return a list of unique vowels in the word"""
        vowels_found = []
        for vowel in self.vowels:
            if vowel in self.__str__():
                vowels_found.append(vowel)
        return vowels_found


class Dictionary:
    """Dictionary class"""

    def __init__(self, dict_file=None):
        self.words = []
        if dict_file:
            self.import_dict(dict_file)

    def import_dict(self, dict_file):
        """Import words from a dictionary file"""
        with open(dict_file, "r", encoding="utf-8") as file_handler:
            while line := file_handler.readline().rstrip():
                try:
                    word = line.split("\t")[0].lower()
                except IndexError:
                    continue
                else:
                    if len(word) == WORD_LENGTH:
                        for word_char in word:
                            if word_char not in string.ascii_lowercase:
                                break
                        else:
                            self.words.append(Word(word))

    def get_words_ordered_by_vowel_count(
        self, exclude_words_with_chars=None, vowel_count=len(VOWELS)
    ):
        """Get a list of words ordered by highest vowel count"""
        counter = vowel_count
        results = []
        if not exclude_words_with_chars:
            exclude_words_with_chars = ""
        while counter >= 0:
            for word in [
                w
                for w in self.words
                if len(w.get_vowels()) == counter
                and not any(x in w for x in exclude_words_with_chars)
            ]:
                results.append(word)
            counter -= 1
        return results


class KnownWordle:
    """Manage known word data"""

    def __init__(self, dictionary, known):
        self.dictionary = dictionary
        self.possible = list(string.ascii_lowercase)
        if known.get("absent"):
            self.possible = [
                x for x in self.possible if x not in list(known["absent"])
            ]
        self.wrong_spot = {}
        for i in range(1, WORD_LENGTH + 1):
            self.wrong_spot[i - 1] = list(known.get(f"wrong_spot_{i}") or "")
        self.solved = ["_"] * WORD_LENGTH
        if known.get("solved"):
            if len(known["solved"]) != WORD_LENGTH:
                raise ValueError(f"`solved` str length != {WORD_LENGTH}")
            self.solved = list(known["solved"])

    def wrong_spot_characters(self, word):
        """Check a word has all "wrong_spot" characters in other positions"""
        for i, characters in self.wrong_spot.items():
            for character in characters:
                if character not in word or word[i] == character:
                    return False
        return True

    def get_candidates_ordered_by_vowel_count(self):
        """Get a list of word candidates ordered by unique vowels"""
        results = []
        for word in self.dictionary.get_words_ordered_by_vowel_count(
            [x for x in string.ascii_lowercase if x not in self.possible]
        ):
            if self.wrong_spot_characters(word):
                for i, word_char in enumerate(self.solved):
                    if word_char not in ("_", word[i]):
                        break
                else:
                    results.append(word)
        return results


def parse_args():
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description="Help solve Wordle puzzles.")
    parser.add_argument(
        "-a",
        "--absent",
        metavar="CHARS",
        help="Characters known to be absent from the solution",
    )
    for i in range(1, WORD_LENGTH + 1):
        parser.add_argument(
            f"-{i}",
            f"--wrong-spot-{i}",
            metavar="CHARS",
            help=(
                "Characters known to exist in the word but are not in "
                f"position {i}"
            ),
        )
    parser.add_argument(
        "-s",
        "--solved",
        metavar="CHARS",
        help=(
            f"{WORD_LENGTH} character string representing solved part "
            "of the answer (replacing remaining unknowns with an "
            "underscore character)"
        ),
    )
    args = parser.parse_args()
    if "solved" in args and args.solved:
        if len(args.solved) != 5:
            parser.error(
                f"Given solved string length is not {WORD_LENGTH} characters"
            )
        if not (
            (args.solved == "_" * WORD_LENGTH)
            or args.solved.replace("_", "").isalpha()
        ):
            parser.error(
                "Given solved string is not entirely alphabetic (excluding "
                "underscores)"
            )
    return args


def print_words_ordered_by_vowel(word_list):
    """Print a word list ordered by vowel count"""

    def print_separator(vowel_count):
        print(f"=== {vowel_count} ===")

    vowel_count = None
    for word in word_list:
        if vowel_count is None:
            vowel_count = word.get_unique_vowel_count
            print_separator(vowel_count)
        if word.get_unique_vowel_count < vowel_count:
            vowel_count = word.get_unique_vowel_count
            print()
            print_separator(vowel_count)
        print(word)


def get_full_path(file_path):
    """Return a full path to a file

    Converts a relative path based on location of this script.
    """
    abs_path = file_path
    if not abs_path.startswith("/"):
        script_dir = Path(__file__).parent
        abs_path = str(script_dir / file_path)
    return abs_path


def main():
    """Begin execution"""
    args = parse_args()
    known = vars(args)
    dict_path = get_full_path(DICT_FILE)
    try:
        dictionary = Dictionary(dict_path)
    except FileNotFoundError as error:
        print(
            f"Cannot load '{error.filename}': {error.strerror}\n\n"
            "Please install a dictionary or fix its path.",
            file=sys.stderr,
        )
        sys.exit(10)
    known = KnownWordle(dictionary, known)
    try:
        print_words_ordered_by_vowel(
            known.get_candidates_ordered_by_vowel_count()
        )
        sys.stdout.flush()
    except BrokenPipeError:
        # This handles tools like `head` as per the docs
        # https://docs.python.org/3/library/signal.html#note-on-sigpipe
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)


if __name__ == "__main__":
    main()
