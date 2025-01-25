import logging
from typing import NoReturn, Optional, Any
from module.crawling_data.data_mining.data_cleaning_strategy_factory import DataCleaningStrategyFactory
from module.crawling_data.data_mining.data_mining_type import PageType
from process_manager import CrawlingDataModule, FundCrawlingResult, NeedCrawledFundModule
from utils.downloader.async_downloader import AsyncHttpDownloader, BaseRequest
from utils.downloader.impl.http_request_downloader import AsyncHttpRequestDownloader, Request

class AsyncCrawlingData(CrawlingDataModule):
    def __init__(self):
        pass
    def do_crawling(self):
        pass
    def has_next_result(self):
        pass
    def get_a_result(self):
        pass
    def get_context_id_and_increase(self) -> int:
        pass
    def shutdown(self):
        pass
    class Context:
        def __init__(self):
            pass
        def get_context_id_and_increase(self) -> int:
            pass
        def all_task_finished(self) -> bool:
            pass
        def finish_task(self) -> bool:
            pass
        class UniqueKey(BaseRequest.UniqueKey):
            def __init__(self):
                pass
    class PageCrawlingTask:
        def __init__(self):
            pass
    