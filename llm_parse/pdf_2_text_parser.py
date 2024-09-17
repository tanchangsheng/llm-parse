import logging

from pypdf import PdfReader

from llm_parse.base import BaseParser
from llm_parse.utils import remove_non_printable

# to suppress unnecessary pypdf logs
logger = logging.getLogger("pypdf")
logger.setLevel(logging.ERROR)


class PDF2TextParser(BaseParser):
    """
    Load data from PDF files into raw text.
    Built on the pdfplumber package.

    Notes:
        - pdfplumber is chosen over PyPDF2 as PyPDF2 has a tendency to present tables as a list.
            Example table in pdf (presented in Markdown format here):
            | s/n | name|
            | 1 | john |

            PyPDF2 undesirable output:
            s/n
            1
            name
            john

            pdfplumber desirable output:
            s/n name
            1 john
    """

    def load_data(
        self,
        file_path: str,
    ) -> str:
        """
        Full raw text data is extracted from the PDF, including headers, footers, tables etc.
        However, structural information is not retained. Hence, a table will be parsed as just body of text.

        Further text processing is done to clean the extracted text content to:
        - Remove non-printable ASCII characters excluding tab, newline and carriage return.
        - Remove repetitive empty lines.

        Args:
            file_path: Path of file to load.

        Returns:
            str: Text extracted from file.
        """

        reader = PdfReader(file_path)

        text = ""
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text += page.extract_text()

        text = remove_non_printable(text)

        return text
