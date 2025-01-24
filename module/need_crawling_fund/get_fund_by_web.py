import re
from typing import NoReturn
import requests
from process_manager import NeedCrawledFundModule

class GetNeedCrawledFundByWeb(NeedCrawledFundModule):
    def init_generator(self) -> NoReturn:
        url = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?page=1,&onlySale=0'
        page = requests.get(url, headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/78.0.3904.108 Safari/537.36'})
        fund_list = re.findall(r'"[0-9]{6}",".+?"', page.text)
        self.total = len(fund_list)
        self.task_generator = (NeedCrawledFundModule.NeedCrawledOnceFund(i[1:7], i[10:-1]) for i in fund_list)

class GetNeedCrawledFundByWeb4Test(NeedCrawledFundModule):
    test_case_num = 2
    def init_generator(self) -> NoReturn:
        url = f'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?page=1,{self.test_case_num}&onlySale=0'
        page = requests.get(url, headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/78.0.3904.108 Safari/537.36'})
        fund_list = re.findall(r'"[0-9]{6}",".+?"', page.text)
        self.total = len(fund_list)

        self.task_generator = (NeedCrawledFundModule.NeedCrawledOnceFund(i[1:7], i[10:-1]) for i in fund_list)

class GetSpecialNeedCrawledFund(NeedCrawledFundModule):
     def init_generator(self) -> NoReturn:
        # 基金目录
        fund_list = ({'code': '007746', 'name': '华安现金润利'}, {'code': '020282', 'name': '益民优势安享混合C'})
        self.total = len(fund_list)

        self.task_generator = (NeedCrawledFundModule.NeedCrawledOnceFund(
            code=t['code'], name=t['name']) for t in fund_list)
