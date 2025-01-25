from module.crawling_data.data_mining.data_cleaning_strategy import DataCleaningStrategy
from module.crawling_data.data_mining.data_mining_type import PageType
from module.crawling_data.data_mining.impl.increase import RiseStrategy
from module.crawling_data.data_mining.impl.manager import ManagerStrategy
from module.crawling_data.data_mining.impl.overview import OverviewStrategy
from module.crawling_data.data_mining.impl.sharpe import MetricsStrategy

class DataCleaningStrategyFactory:
    _stratege_dict: dict[PageType, DataCleaningStrategy] = {
        PageType.OVERVIEW: OverviewStrategy(),
        PageType.METRICS: MetricsStrategy(),
        PageType.MANAGER: ManagerStrategy(),
        PageType.INCREASE: RiseStrategy()
    }
    
    @classmethod
    def get_strategy(cls, page_type: PageType) -> DataCleaningStrategy:
        return cls._stratege_dict[page_type]