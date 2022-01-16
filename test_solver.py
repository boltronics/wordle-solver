import unittest

import solver


class TestWord(unittest.TestCase):
    def test_get_unique_vowel_count(self):
        word = solver.Word("audio")
        self.assertEqual(word.get_unique_vowel_count, 4)

        word = solver.Word("glyph")
        self.assertEqual(word.get_unique_vowel_count, 0)

        word = solver.Word("goose")
        self.assertEqual(word.get_unique_vowel_count, 2)

    def test_get_vowels(self):
        word = solver.Word("audio")
        self.assertEqual(word.get_vowels(), ["a", "i", "o", "u"])

        word = solver.Word("glyph")
        self.assertEqual(word.get_vowels(), [])

        word = solver.Word("goose")
        self.assertEqual(word.get_vowels(), ["e", "o"])


class TestDictionary(unittest.TestCase):
    def test_get_words_ordered_by_vowel_count(self):
        dictionary = solver.Dictionary()
        for word in ("audio", "glyph", "goose"):
            dictionary.words.append(solver.Word(word))
        self.assertEqual(
            dictionary.get_words_ordered_by_vowel_count(
                exclude_words_with_chars=["a", "d"]
            ),
            [dictionary.words[2], dictionary.words[1]],
        )


class TestKnownWordle(unittest.TestCase):
    def setUp(self):
        self.dictionary = solver.Dictionary()
        for word in ("audio", "glyph", "goose"):
            self.dictionary.words.append(solver.Word(word))

    def test_wrong_spot_characters(self):
        # No wrong spot characters
        known = solver.KnownWordle(
            self.dictionary, {"absent": "ln", "solved": "_oose"}
        )
        expected_results = (True, True, True)
        for i, word in enumerate(self.dictionary.words):
            self.assertEqual(
                known.wrong_spot_characters(word), expected_results[i]
            )
        # Some wrong spot characters
        known = solver.KnownWordle(
            self.dictionary,
            {
                "absent": "ln",
                "solved": "_oo__",
                "wrong_spot_1": "se",
                "wrong_spot_5": "g",
            },
        )
        expected_results = (False, False, True)
        for i, word in enumerate(self.dictionary.words):
            self.assertEqual(
                known.wrong_spot_characters(word), expected_results[i]
            )

    def test_get_candidates_ordered_by_vowel_count(self):
        # Focused result
        known = solver.KnownWordle(
            self.dictionary,
            {
                "absent": "ln",
                "solved": "_oo__",
                "wrong_spot_1": "se",
                "wrong_spot_5": "g",
            },
        )
        self.assertEqual(
            known.get_candidates_ordered_by_vowel_count(),
            [self.dictionary.words[2]],  # goose
        )
        # All results, re-ordered
        known = solver.KnownWordle(self.dictionary, {})
        self.assertEqual(
            known.get_candidates_ordered_by_vowel_count(),
            [
                self.dictionary.words[0],  # audio
                self.dictionary.words[2],  # goose
                self.dictionary.words[1],  # glyph
            ],
        )
