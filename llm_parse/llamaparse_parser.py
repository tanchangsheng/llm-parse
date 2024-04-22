from enum import StrEnum
from typing import Union, List, Optional

from llama_parse import LlamaParse

from llm_parse.base import BaseParser


class ResultType(StrEnum):
    Markdown = "markdown"
    Text = "text"


class LlamaParseParser(BaseParser):
    """
    Read files into Markdown/Text using Llama Parse.
    This is a wrapper for LlamaParse that implements the BaseParser interface.

    LlamaParse repo: https://github.com/run-llama/llama_parse
    """

    def __init__(self, **kwargs):
        # init LlamaParse parser.
        self.parser = LlamaParse(**kwargs)

    def load_data(
        self, file_path: Union[List[str], str], extra_info: Optional[dict] = None
    ) -> str:
        """
        Calls the load_data method of LlamaParse object and returns the content of the response document.

        Args:
            file_path: Path to file to load.
            extra_info: Optional arg by load_data of LlamaParse.

        Returns:
            str: Text from LlamaParse response document.
        """

        documents = self.parser.load_data(file_path)

        # no document returned from API
        if len(documents) == 0:
            return ""

        text = documents[0].text

        return text
