'''
爬取核心
对爬取过程的管理
'''
import os
import logging
from abc import abstractmethod, ABC
from collections.abc import Generator 
from datetime import datetime
from enum import unique, StrEnum
from threading import Thread
from time import sleep
from typing import NoReturn, Optional

class NeedCrawledFundModule(ABC):
    class NeedCrawledOnceFund:
        def __init__(self, fund_name: str, fund_code: str):
            self.fund_name = fund_name
            self.fund_code = fund_code
    def __init__(self):
        self.total = None
        self.task_generator: Generator[NeedCrawledFundModule.NeedCrawledOnceFund] = None
        self.init_generator()
    @abstractmethod
    def init_generator(self) -> NoReturn:
        return NotImplemented
class FundCrawlingResult:
    @unique
    class Header(StrEnum):
        FUND_CODE = '基金代码',
        FUND_SIMPLE_NAME = '基金简称',
        FUND_TYPE = '基金类型',
        FUND_SIZE = '资产规模(亿)',
        FUND_COMPANY = '基金管理人',
        FUND_VALUE = '基金净值',
        # 兼容带新场景，A+B -> B -> B+C，此时基金经理为时长最长的B，对应的任职时间为 这三段 B连续任职的任职时间
        FUND_MANAGER = '基金经理(最近连续最长任职)',
        DATE_OF_APPOINTMENT = '基金经理的上任时间',
        STANDARD_DEVIATION_THREE_YEARS = '近三年标准差',
        SHARPE_THREE_YEARS = '近三年夏普',
        THREE_YEARS_INCREASE = '近三年涨幅',
        FIVE_YEARS_INCREASE = '近五年涨幅'
    def __init__(self, fund_name: str, fund_code: str):
        self.fund_info_dict = {FundCrawlingResult.Header.FUND_CODE: fund_code, 
                               FundCrawlingResult.Header.FUND_SIMPLE_NAME: fund_name}
class CrawlingDataModule(ABC):
    @abstractmethod
    def do_crawling(self, task: NeedCrawledFundModule.NeedCrawledOnceFund) -> NoReturn:
        return NotImplemented
    @abstractmethod
    def has_next_result(self) -> bool:
        return NotImplemented
    @abstractmethod
    def get_a_result(self) -> Optional[FundCrawlingResult]:
        return NotImplemented
    @abstractmethod
    def shutdown(self):
        return NotImplemented
class SaveResultModule(ABC):
    @abstractmethod
    def save_result(self, result: FundCrawlingResult) -> NoReturn:
        return NotImplemented
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        pass
class TaskManager:
    def __init__(self, need_crawled_fund_module: NeedCrawledFundModule, crawling_data_module: CrawlingDataModule, 
                 save_data_module: SaveResultModule, log_level = logging.DEBUG):
        
        self._need_crawled_fund_module = need_crawled_fund_module
        self._crawling_data_module = crawling_data_module
        self._save_data_module = save_data_module
        log_file_path = './log/'
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        logging.basicConfig(filename=log_file_path + 'process.txt', encoding='utf-8', level=log_level, filemode = 'w',
                             format='%(asctime)s %(message)s')
        logging.info(f'需要爬取的基金总数:{self._need_crawled_fund_module.total}')
        
        self._cur_finished_task_count = 0
        self._all_task_finished = False
        
        
    def get_task_and_crawling(self):
        generator = self._need_crawled_fund_module.task_generator
        while True:
            try:
                task: NeedCrawledFundModule.NeedCrawledOnceFund = next(generator)
            except StopIteration:
                break
            self._crawling_data_module.do_crawling(task)
        self._crawling_data_module.shutdown()
        
    def get_result_and_save(self):
        with self._save_data_module:
            while self._crawling_data_module.has_next_result():
                result: FundCrawlingResult = self._crawling_data_module.get_a_result()
                if result:
                    self._save_result_module.save_result(result)
                    self._cur_finished_task_count+=1
                
        self._all_task_finished = True
    def show_process(self):
        while not self._all_task_finished:
            logging.info(f'已爬取基金数:{self._cur_finished_task_count}')
            sleep(5)
    def run(self) -> NoReturn:
        start_time = datetime.now()
        thread1 = Thread(target=self.get_task_and_crawling)
        thread2 = Thread(target=self.get_result_and_save)
        thread3 = Thread(target=self.show_process)
        
        thread1.start()
        thread2.start()
        thread3.start()
        
        thread1.join()
        thread2.join()
        thread3.join()
        
        cur_time = datetime.now()
        logging.info(f'爬取结束，耗时:{(cur_time - start_time).seconds}')