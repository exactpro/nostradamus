from utils.cleaner import clean_text

text_for_cleaning = """
Test at passed
https://regex101.com/
{{text that will be removed}}
C:\This\Folder\Will\Be\Removed
test_email@gmail.com
{code}
code which should be deleted
{code}
"""


def test_clean_text():
    assert clean_text(text_for_cleaning) == "test passed"
