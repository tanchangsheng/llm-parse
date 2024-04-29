"""
Contains common string processing helper functions that can be used across parser modules.
"""

import re


def remove_non_printable(text: str) -> str:
    r"""
    Removes any characters that are not printable ASCII characters (hexadecimal range: 0x20 to 0x7E) and also preserves
    tab (\t), newline (\n), and carriage return (\r) characters.

    Args:
        text: Text string to process.

    Returns:
        str: Processed text.
    """

    pattern = r"[^\x20-\x7E\t\n\r]"
    return re.sub(pattern, "", text)


def compress_multiline(text: str) -> str:
    r"""
    Replace consecutive empty lines with one empty line.

    Regex explanation:
    - (\n\s*): This part of the pattern matches a newline character \n followed by zero or more whitespace characters
        \s*. The parentheses () capturing group allows us to treat enclosing pattern as a single unit.
    - {2,}: This quantifier specifies that the capturing group () should occur at least 2 or more times consecutively.

    Args:
        text: Text string to process.

    Returns:
        str: Processed text.
    """

    pattern = r"(\n\s*){2,}"
    return re.sub(pattern, "\n\n", text)


def remove_redundant_hash(text: str) -> str:
    r"""
    Remove one or more `#` that appears in empty spaces.
    It should not remove `#` that are used for actual headers.

    Regex explanation:
    - #+: Matches one or more "#" characters.
    - \s+: Matches one or more whitespace characters [ \n\r\t\f].
    - (?= ...): Positive lookahead assertion. It matches the preceding pattern only if it's followed by the pattern
        inside the lookahead.
    - [^\w\s]|$: Matches any character that is not a word character (a-z, A-Z, 0-9, underscore) or whitespace
        character, or the end of the line.

    Args:
        text: Text string to process.

    Returns:
        str: Processed text.
    """

    pattern = r"#+\s+(?=[^\w\s]|$)"
    pattern = re.compile(pattern, re.MULTILINE)
    text = re.sub(pattern, "", text)

    return text


def merge_bold(text: str) -> str:
    r"""
    If there are multiple groups of text in Markdown bold (enclosed by **), on a single line of text,
    the whole line can be grouped as a single group of bold text.

    Regex explanation
    - ^([ \r\t\f]*\*{2}[^*]*\*{2}[ \r\t\f]*)+:
        - ^: Starts with this group.
        - [ \r\t\f]*: Matches zero or more whitespace characters except \n.
        - \*{2}[^*]*\*{2}: Matches text enclosed within **.
        - +: Matches one or more of this group.
    - (\*{2}[^*]*\*{2}[ \r\t\f]*)$: Ends with text enclosed within **.

    Args:
        text: Text string to process.

    Returns:
        str: Processed text.
    """

    def remove_stars(match):
        matched_group = match.group(0)
        matched_group = matched_group.strip()
        replaced_group = matched_group.replace("*", "")
        return f"**{replaced_group}**"

    pattern = r"^([ \r\t\f]*\*{2}[^*]*\*{2}[ \r\t\f]*)+(\*{2}[^*]*\*{2}[ \r\t\f]*)$"
    pattern = re.compile(pattern, re.MULTILINE)
    text = re.sub(pattern, remove_stars, text)

    return text


def merge_spaces(text: str) -> str:
    """
    Keeps only one of repeated white space characters (excluding \n).

    Args:
        text: Text string to process.

    Returns:
        str: Processed text.
    """

    pattern = r"( |\r|\t|\f)+"
    text = re.sub(pattern, r"\1", text)
    return text


def merge_headers(text):
    r"""
    If a line of text is a header, remove redundant occurrences of header symbols from the line.

    Regex explanation:
    - ^: Starts with group.
    - (): Groups a pattern.
    - #+: One or more hash symbol.
    - \s+: One or more whitespace characters.
    - .+: One or more any character.
    - $: Ends with group.

    Args:
        text: Text string to process.

    Returns:
        str: Processed text.
    """

    def remove_hash(match):
        matched_group = match.group(0)
        header_size = 0
        for ch in matched_group:
            if ch == "#":
                header_size += 1
            else:
                break
        header = "#" * header_size
        replaced_group = matched_group.replace(header, "")
        return f"{header}{replaced_group}"

    pattern = re.compile(r"^(#+\s+.+)$", re.MULTILINE)
    text = re.sub(pattern, remove_hash, text)
    return text
