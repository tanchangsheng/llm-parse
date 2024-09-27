# LLM Parse

LLM Parse is a Python library designed for parsing and extracting data from files, specifically optimized for 
downstream tasks involving large language models (LLMs).

It is built on several popular document parsing libraries with further text processing to represent the data
in a form that is more suitable for downstream LLM tasks such as RAG, summarization and drafting.

## Getting started

Install the package:
```
pip install llm-parse
```

## Examples

Parse a PDF to Markdown.
```python
from llm_parse.pdf_2_md_parser import PDF2MDParser

parser = PDF2MDParser()
text = parser.load_data("example.pdf")
```

Parse a PDF to text.
```python
from llm_parse.pdf_2_text_parser import PDF2TextParser

parser = PDF2TextParser()
text = parser.load_data("example.pdf")
```

Using LlamaParse parser.
```python
from llm_parse.llamaparse_parser import LlamaParseParser

# can use any args for LlamaParse. ref: https://github.com/run-llama/llama_parse?tab=readme-ov-file#getting-started
parser = LlamaParseParser(
    api_key="llx-...",  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    num_workers=4,  # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="en",  # Optionally you can define a language, default=en
)
text = parser.load_data("example.pdf")
```
