from re import sub, compile
from itertools import chain

REGULAR_EXPRESSIONS = {
    "basic": [
        # symbols enclosed in {} brackets and placed {}between{} brackets.
        compile(r"{.*}\n[\s\S]*\n{.*}"),
        # links and file paths
        compile(r"(?:http[s]?:\/\/|www\.)[\S]+\.[\S]+\.*[\S]+?"),
        # html tags
        compile(r"<[^>]*>"),
        # email
        compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"),
        # windows directory path
        compile(r"[a-zA-Z]:(\?[a-zA-Z0-9]+)+"),
        # filename
        compile(r"[\S]+\.[a-zA-Z-]+"),
    ],
    "specific": [
        # java stack trace timestamp
        compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s"),
        # java stack trace
        compile(
            r"(INFO|ERROR|WARN|TRACE|DEBUG|FATAL)\s+(\[\S+\].+\n)(\S+\.[^\n]+\s+at\s+)+(\S+\.[^\n]+\s+)?"
        ),
        # r"(?<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s(?<level>INFO|ERROR|WARN|TRACE|DEBUG|FATAL)\s+(\[\S+\].+\n)(\S+\.[^\n]+\s+at\s+)+(?<last_string>\S+\.[^\n]+\s+)?",
        # java stack trace
        compile(
            r"(INFO|ERROR|WARN|TRACE|DEBUG|FATAL)\s+\[([^\]]+)]-\[([^\]]+)]\s+([^\n]+\n?[^\n]+)"
        )
        # r"(?<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s(?<level>INFO|ERROR|WARN|TRACE|DEBUG|FATAL)\s+\[(?<class>[^\]]+)]-\[(?<thread>[^\]]+)]\s+(?<text>[^\n]+\n?[^\n]+)",
    ],
    "final": [
        compile(r"( the | a | an | at | in | on | by | for )"),
        compile(r"[$-/:-?{-~!\"^_`\[\]◾╙“”‘’​–•\#@]+"),  # special characters
        compile(r"[\d]+"),  # digits
        compile(r"[\s]{2,}"),  # spaces
        compile(r"[\n\t]+"),  # line breakers, tabs
    ],
}


def clean_text(
    text: str, regular_expressions: list = REGULAR_EXPRESSIONS
) -> str:
    """Cleans up handled text.

    Parameters
    ----------
    text:
        Text to be processed.
    regular_expressions:
        List of compiled regular expressions.

    Returns
    -------
        Cleaned up text.
    """
    basic_regexes = regular_expressions.get("basic")
    specific_regexes = regular_expressions.get("specific")
    final_regexes = regular_expressions.get("final")
    if not text:
        return ""
    else:
        cleaned_text = text
        for regex in chain(basic_regexes, specific_regexes, final_regexes):
            cleaned_text = sub(regex, " ", cleaned_text).strip()
            if not cleaned_text:
                return ""
        return cleaned_text.lower()
