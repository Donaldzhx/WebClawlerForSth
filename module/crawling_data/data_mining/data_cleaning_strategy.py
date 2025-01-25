from abc import ABC, abstractmethod
from typing import NoReturn
from process_manager import FundCrawlingResult
class Data_cleaning_strategy(ABC):
    @abstractmethod
    def build_url(self) -> str:
        pass
    @abstractmethod
    def fill_result(self) -> NoReturn:
        pass
    