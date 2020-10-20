import unittest
import pytest

from apps.extractor.main.cleaner import clean_text
from utils.data_converter import convert_to_integer


@pytest.mark.usefixtures()
class TestDescriptionAssessment(unittest.TestCase):
    def test_clean_text_expressions_basic(self):
        text = r"test@mail.ru is test email. <head> is tag in html. http://test.com {Test.test}"

        clear_text = clean_text(text)
        assert clear_text == "is test email is tag html"

    def test_clean_text_expressions_specific(self):
        text = "Datetime 1234-12-12 21:21:21,123 "

        clear_text = clean_text(text)
        assert clear_text == "datetime"

    def test_clean_text_expressions_final(self):
        text = "test for test +100500$\t s t  "

        clear_text = clean_text(text)
        assert clear_text == "test test"

    def test_convert_to_integer(self):
        assert convert_to_integer(0.73) == 73
