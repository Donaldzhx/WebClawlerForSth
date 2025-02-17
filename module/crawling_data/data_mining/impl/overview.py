import re
from string import Template
from typing import NoReturn
from requests import Response
from module.crawling_data.data_mining.data_cleaning_strategy_factory import DataCleaningStrategy
from module.crawling_data.data_mining.impl.constants import number_in_mille
from process_manager import FundCrawlingResult
class OverviewStrategy(DataCleaningStrategy):
    url_template = Template('http://fundf10.eastmoney.com/jbgk_$fund_code.html')
    fund_type_pattern = re.compile(r'基金类型</th><td>(.+?)</td></tr><tr><th>发行日期')
    fund_size_pattern = re.compile(fr'资产规模</th><td>({number_in_mille})亿元')
    fund_company_pattern = re.compile(r'基金管理人</th><td><a.*?">(.+?)</a></td><th>基金托管人')
    fund_value_pattern = re.compile(fr'单位净值.*?:[\s\S]*?({number_in_mille})\s')
    def build_url(self, fund_code: str) -> str:
        return self.url_template.substitute(fund_code=fund_code)

    def fill_result(self, response: Response, result: FundCrawlingResult) -> NoReturn:
        page_text = response.text
        fund_kind_result = self.fund_type_pattern.search(page_text)
        if fund_kind_result:
            result.fund_info_dict[FundCrawlingResult.Header.FUND_TYPE] = fund_kind_result.group(1)
        fund_size_result = self.fund_size_pattern.search(page_text)
        if fund_size_result:
            # 1,179.10 亿元
            fund_size = fund_size_result.group(1).replace(',', '')
            result.fund_info_dict[FundCrawlingResult.Header.FUND_SIZE] = fund_size
        fund_company_result = self.fund_company_pattern.search(page_text)
        if fund_company_result:
            result.fund_info_dict[FundCrawlingResult.Header.FUND_COMPANY] = fund_company_result.group(1)
        fund_value_result = self.fund_value_pattern.search(page_text)
        if fund_value_result:
            result.fund_info_dict[FundCrawlingResult.Header.FUND_VALUE] = fund_value_result.group(1)
