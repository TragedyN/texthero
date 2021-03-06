import pandas as pd
from texthero import representation
from texthero import preprocessing

from . import PandasTestCase

import doctest
import unittest
import string
import warnings

"""
Test doctest
"""


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(representation))
    return tests


class TestRepresentation(PandasTestCase):
    """
    Term Frequency.
    """

    def test_term_frequency_single_document(self):
        s = pd.Series("a b c c")
        s = preprocessing.tokenize(s)
        s_true = pd.Series([[1, 1, 2]])
        self.assertEqual(representation.term_frequency(s), s_true)

    def test_term_frequency_multiple_documents(self):
        s = pd.Series(["doc_one", "doc_two"])
        s = preprocessing.tokenize(s)
        s_true = pd.Series([[1, 1, 1, 0], [1, 1, 0, 1]])
        self.assertEqual(representation.term_frequency(s), s_true)

    def test_term_frequency_not_lowercase(self):
        s = pd.Series(["one ONE"])
        s = preprocessing.tokenize(s)
        s_true = pd.Series([[1, 1]])
        self.assertEqual(representation.term_frequency(s), s_true)

    def test_term_frequency_punctuation_are_kept(self):
        s = pd.Series(["one !"])
        s = preprocessing.tokenize(s)
        s_true = pd.Series([[1, 1]])
        self.assertEqual(representation.term_frequency(s), s_true)

    def test_term_frequency_not_tokenized_yet(self):
        s = pd.Series("a b c c")
        s_true = pd.Series([[1, 1, 2]])

        with warnings.catch_warnings():  # avoid print warning
            warnings.simplefilter("ignore")
            self.assertEqual(representation.term_frequency(s), s_true)

        with self.assertWarns(DeprecationWarning):  # check raise warning
            representation.term_frequency(s)

    """
    TF-IDF
    """

    def test_idf_single_document(self):
        s = pd.Series("a")
        s = preprocessing.tokenize(s)
        s_true = pd.Series([[1]])
        self.assertEqual(representation.tfidf(s), s_true)

    def test_idf_not_tokenized_yet(self):
        s = pd.Series("a")
        s_true = pd.Series([[1]])

        with warnings.catch_warnings():  # avoid print warning
            warnings.simplefilter("ignore")
            self.assertEqual(representation.tfidf(s), s_true)

        with self.assertWarns(DeprecationWarning):  # check raise warning
            representation.tfidf(s)

    def test_idf_single_not_lowercase(self):
        tfidf_single_smooth = 0.7071067811865475  # TODO

        s = pd.Series("ONE one")
        s = preprocessing.tokenize(s)
        s_true = pd.Series([[tfidf_single_smooth, tfidf_single_smooth]])
        self.assertEqual(representation.tfidf(s), s_true)
