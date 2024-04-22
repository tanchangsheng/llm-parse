from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """Interface for loading data from a directory."""

    @abstractmethod
    def load_data(self, *args: Any, **load_kwargs: Any) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not provide load_data method currently"
        )
