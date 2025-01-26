import json
from csv import DictReader
from datetime import date, timedelta
from typing import NoReturn
from heapq import heappush, heappop 
from process_manager import FundCrawlingResult

debt_shape_remain = 200
other_shape_remain = 200

manager_long_remain = 10
manager_4_n_years = 10

debt_increase_remain = 5
other_increase_remain = 10

def analyze():
    debt_holder = FundHolder(retain_num = debt_shape_remain)
    other_holder = FundHolder(retain_num = other_shape_remain)
    manager_long_years_holder = FundHolder(retain_num = manager_long_remain)
    
    with open('../result/result.csv', 'r', encoding = 'utf-8') as csvfile:
        reader: DictReader = DictReader(csvfile)
        today = date.today()
        for row in reader:
            try:
                date_of_appointment: date = date.fromisoformat(row[FundCrawlingResult.Header.DATE_OF_APPOINTMENT])
                delta: timedelta = today - date_of_appointment
                manager_4_more_3_yeas = delta.days > 365 * 3
                manager_4_long_times = delta.days > 365 * manager_4_n_years
                three_years_sharpe: str = row[FundCrawlingResult.Header.SHARPE_THREE_YEARS]
                three_years_increase = row[FundCrawlingResult.Header.THREE_YEARS_INCREASE]
                if manager_4_more_3_yeas is False or three_years_sharpe == None:
                    continue
                fund_type: str = row[FundCrawlingResult.Header.FUND_TYPE]
                if '债' in fund_type:
                    debt_holder.put_fund(float(three_years_sharpe), row)
                elif manager_4_long_times and three_years_increase != 'None':
                    manager_long_years_holder.put_fund(float(three_years_increase[:-1]), row)
                else:
                    other_holder.put_fund(float(three_years_sharpe), row)            
            except Exception as e:
                print(f'基金{row[FundCrawlingResult.Header.FUND_CODE]}分析失败', e)
                                                               
    debt_increase_holder = FundHolder(retain_num = debt_increase_remain)
    for fund in debt_holder.get_result():
        increase = fund[FundCrawlingResult.Header.THREE_YEARS_INCREASE]
        if increase != None:
            debt_increase_holder.put_fund(float(increase[:-1]), fund)    
class FundHolder:
    def __init__(self):
        pass
    def put_fund(self):
        pass
    def get_result(self):
        pass
    class SpecialDict(dict):
        pass

        

    