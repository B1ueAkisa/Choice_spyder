#%%
import requests,json,os,time,sys,datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
import urllib.parse
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()
今天=datetime.date.today().strftime("%Y-%m-%d")

#%% basic
def 反复抓(表单):
    url='https://datacenter-choice.eastmoney.com/choice/api/data/v1/get?source=choice'
    while True:
                try:
                    response = requests.get(url,params=表单,timeout=10, verify=False,headers={'Connection':'close'})#cookies=cookies,
                    response.close()
                    if response.ok: break
                except Exception as e:
                    print(e,end=' ')
                    time.sleep(60) #sys.exit()
    return response
def 抓取(表单):
    response=反复抓(表单)
    try:
        结果dict=response.json()
    except Exception as e: 
        print('js有误',e,response.text)
        #sys.exit()
    if 结果dict['message']=='ok':       
        结果DT=pd.DataFrame(结果dict['result']['data'])
        return(结果DT)
    else:        
        if not 结果dict['message']=='返回数据为空':
            print('msg:',结果dict['message'],end=' ')
        return 结果dict['message']
#%% 
class 板块名单类():
    def __init__(self):
        self.可下载方法=[mf for  mf in  板块名单类.__dict__.keys() if not mf.startswith('__')]

    def 城投平台大全(self):
        表单={'reportName': 'RPT_BOND_BS_URBATERR',
    'columns': 'ORG_CODE,REPORT_DATE,REPORT_YEAR,REPORT_TYPE_CODE,REPORT_TYPE,ORG_NAME,PROVINCE_CODE,CITY_CODE,DISTRICT_CODE,ADMINISTRATIVE_LEVEL,BOND_BALANCE,CURRENT_AMT,GOVSNPRO_RATIO,CURRENT_AMT_STD,TOI_RATIO,AMOUNT_STD,PURCHASE_AMT_RATIO,PURCHASE_AMT_STD,TOTAL_ASSETS,INVECONT_RATIO,CIP_RATIO,ACCOCONT_RATIO,LIMITEDASSET,LIMITEDASSET_RATIO,LIABILITIES_RATIO,INTEREST_DEBT,CURRENT_LIAB_RATIO,DEBT_LEVER,BALANCE_INTE_DEBT,PARENT_ROE,MINORITY_ROE,RELATED_PARTY_NAME,AREA,RATING_NUM,CREDIT_RATING',
    'quoteColumns': '',
    'filter': '(REPORT_YEAR="2022")(REPORT_TYPE_CODE="6")',
    'sortColumns': 'RATING_NUM,ORG_CODE',
    'sortTypes': '1,1',
    'pageSize': '',
    'pageNumber': '',
    'client': 'SW'}
        结果DT=抓取(表单)
        return 结果DT

    def 全部发行人融资统计(self):
    #全部发行人融资统计
        表单={'reportName': 'RPT_CUSTOM_ISSUQ_FINANCE_BOND',
        'columns': 'ISSUE_NAME,PAYBACK_BOND_COUNT,PAYBACK_TOTAL_AMT,EBITDA_BP_RATION,CASH_YEARMU_RATION,IE_STOCKWEIGHT_YEAR,NCF_BP_RATION,IPAYBACK_ANNUAL_AMT,IR_STOCKWEIGHT_PER,BOND_PAY,IR_ALLWEIGHT_PER,ISSUE_CODE,ISSUE_BOND_COUNT,IE_ALLWEIGHT_YEAR,ISSUE_TOTAL_AMT',
            'sortColumns':'ISSUE_TOTAL_AMT',
        'sortTypes'	:'-1',
        'filter': '(BOARD_CODE in ("187001"))(FLITER_TYPE=1)(FILTER_BOND_TYPE in ("-"))',
        'client': 'SW'}
        结果DT=抓取(表单)
        return 结果DT

    def 城投发行人融资统计(self):
        表单={'reportName': 'RPT_CUSTOM_ISSUQ_FINANCE_BOND',
        'columns': 'ISSUE_NAME,PAYBACK_BOND_COUNT,PAYBACK_TOTAL_AMT,EBITDA_BP_RATION,CASH_YEARMU_RATION,IE_STOCKWEIGHT_YEAR,NCF_BP_RATION,IPAYBACK_ANNUAL_AMT,IR_STOCKWEIGHT_PER,BOND_PAY,IR_ALLWEIGHT_PER,ISSUE_CODE,ISSUE_BOND_COUNT,IE_ALLWEIGHT_YEAR,ISSUE_TOTAL_AMT',
            'sortColumns':'ISSUE_TOTAL_AMT',
        'sortTypes'	:'-1',
        'filter': '(BOARD_CODE in ("184003"))(FLITER_TYPE=1)(FILTER_BOND_TYPE in ("-"))',
        'client': 'SW'}
        结果DT=抓取(表单)
        return 结果DT

    def 东财房地产发行人融资统计(self):
        表单={'reportName': 'RPT_CUSTOM_ISSUQ_FINANCE_BOND',
        'columns': 'ISSUE_NAME,PAYBACK_BOND_COUNT,PAYBACK_TOTAL_AMT,EBITDA_BP_RATION,CASH_YEARMU_RATION,IE_STOCKWEIGHT_YEAR,NCF_BP_RATION,IPAYBACK_ANNUAL_AMT,IR_STOCKWEIGHT_PER,BOND_PAY,IR_ALLWEIGHT_PER,ISSUE_CODE,ISSUE_BOND_COUNT,IE_ALLWEIGHT_YEAR,ISSUE_TOTAL_AMT',
            'sortColumns':'ISSUE_TOTAL_AMT',
        'sortTypes'	:'-1',
        'filter': '(BOARD_CODE in ("181001014"))(FLITER_TYPE=1)(FILTER_BOND_TYPE in ("-"))',
        'client': 'SW'}
        结果DT=抓取(表单)
        return 结果DT
    
class 违约类():
    def __init__(self):
        self.可下载方法=[mf for  mf in  违约类.__dict__.keys() if not mf.startswith('__')]

    def 违约下载(self):
        表单={'reportName'	:'RPT_BOND_NEGATIVE_VIOLATE',
                'columns'	:'ALL',
                    'sortColumns':'VIOLATE_DATE',
                'sortTypes'	:'-1',
                'pageNumber':	'',
                'pageSize'	:'',
                'client':	'SW',
                'filter':	'',
                }
        结果DT=抓取(表单)
        return(结果DT)

class 对应类():
    def __init__(self):
        self.可下载方法=[mf for  mf in  对应类.__dict__.keys() if not mf.startswith('__')]
    def 债券找发行人(self,SECUCODE):#债券找发行人
        表单={'reportName': 'RPT_BOND_BS_INFO',
        'columns': 'SECUCODE,SECURITY_CODE,BOND_NAME_ABBR,ISSUE_CODE,ISSUE_NAME',
            'quoteColumns': '',
        'filter': '(SECUCODE="%s")'%(SECUCODE),
        'client': 'SW'}
        结果DT=抓取(表单)
        return(结果DT.ISSUE_CODE[0])


#%% 债券部分
class 债券类():
    def __init__(self):
        self.可下载方法=[mf for  mf in  债券类.__dict__.keys() if not mf.startswith('__')]
    def 单债券行情(self,SECUCODE,开始日期='2001-01-01',结束日期=今天):
        url='https://datacenter-choice.eastmoney.com/choice/api/data/v1/get?source=choice'
        表单={'reportName'	:'RPT_BOND_BS_INFO;RPT_F5_BOND_DEEPTS_LSCJSP',
        'columns'	:'@ISSUE_CODE,BOND_NAME_ABBR;@ISSUE_CODE,TRADE_DATE,SECUCODE,REMTERM,SOURCE,CLOSE_YIELD,WEIGHTAVG_YIELD,VOLUME,VALUE_BP,A_YTM_DQ,A_YTM_XQ,A_PRICE_DQ,A_PRICE_XQ,OPEN_YIELD,HIGH_YIELD,LOW_YIELD,YIELD_CHANGE,YIELD_CHANGE_EM,FULL_OPEN_PRICE,FULL_HIGH_PRICE,FULL_LOW_PRICE,FULL_CLOSE_PRICE,FULL_WEIGHTAVG_PRICE,FULL_CHANGE_RATE,NET_OPEN_PRICE,NET_HIGH_PRICE,NET_LOW_PRICE,NET_CLOSE_PRICE,NET_WEIGHTAVG_PRICE,NET_CHANGE_RATE,NET_YIELD_CHANGE,DEAL_AMOUNT,DEAL_NUM,MODIFIED_DURATION,CJ_STATE,B_YTM_TJ,B_PRICE_TJ,C_YTM_TJ,C_PRICE_TJ,D_YTM,D_PRICE,BOND_NAME_ABBR,SECURITY_INNER_CODE,IS_CULLING,RANK1,A_DCQ_DQ,A_DCQ_XQ',
        'sortColumns':'TRADE_DATE',
        'sortTypes'	:'-1',
        'pageNumber':	'',
        'quoteColumns'	:'',
        'pageSize'	:1000,
        'pageNumber':1,
        'client':	'SW',#
        'filter':	f'''(SECUCODE="{SECUCODE}");(ISSUE_CODE="~")(SECUCODE="{SECUCODE}")(IS_CULLING="1")(TRADE_DATE>='{开始日期}')(TRADE_DATE<='{结束日期}')''',#
        }
        page=1
        结果列表=[]
        while True:
            表单['pageNumber']=page
            response=反复抓(表单)
            try:
                结果dict=response.json()
            except json.JSONDecodeError as e:
                print(response.text)
                print(f"解析JSON字符串出错： {e}")
                return 
            if not 结果dict['message']=='ok':     
                if not 结果dict['message']=='返回数据为空':
                    print('msg:',结果dict['message'],end=' ')
                return 结果dict['message']
            if 结果dict['result'] is None: 
                return #response
            if page==1:总页数=结果dict['result']['pages']
            结果列表.append(pd.DataFrame(结果dict['result']['data']))
            if page==总页数:break
            page+=1
        大结果=pd.concat(结果列表)
        return 大结果
    def 单债券舆情(self,SECUCODE,开始日期='2001-01-01',结束日期=今天):
        舆情表单={'reportName'	:'RPT_CUSTOM_BOND_REMIND_MERGE',
        'columns'	:'SECUCODE,NOTICE_DATE,SOURCE_URL,EVENT_TYPE_I,EVENT_TYPE_II,EVENT_TYPE_III,RISK_LEVEL,EVENT_SUMMARY,EVENT_DATE,MXID,EVENT_TYPE_CODEI,EVENT_TYPE_CODEII,EVENT_TYPE_CODEIII,EVENT_REASON,ISSUE_CODE,NEXT_STAGE_EVENT,BOND_NAME_ABBR',
        'sortColumns':'EVENT_DATE,NOTICE_DATE',
        'sortTypes'	:'-1,-1',
        'pageNumber':	'',
        'pageSize'	:'',
        'client':	'SW',
        'filter':	f'''(SECUCODE="{SECUCODE}")(EVENT_DATE>='{开始日期} 00:00:00')(EVENT_DATE<='{结束日期} 23:59:59')''',
        }
        结果DT=抓取(舆情表单)
        return 结果DT
    def 单债券的发行人财务(self,SECUCODE,开始日期='2001-01-01',结束日期=今天):
        财务表单={'reportName'	:'RPT_BOND_BS_INFO;RPT_BOND_ISSUE_FINANCE',
        'columns'	:'SECUCODE,@ISSUE_CODE;@ORG_CODE,REPORT_DATE,REPORT_TYPE,CURRENCY,TOTAL_ASSETS,MONETARYFUNDS,NET_ASSETS,TOTAL_LIABILITIES,DEBT_ASSET_RATIO,NETPROFIT,OPERATE_INCOME,OPERATE_PROFIT,EBITDA,EBITDAZSR,MPROFIT_OPERATEREVE,MAIN_INCOME_RATE,ROA,ROE_WEIGHT,NETCASH_OPERATE,NETCASH_INVEST,TOTAL_FINANCE,OPERATE_EBITDA,INVENTORY_TR,CURRENT_RATIO,SPEED_RATIO,INTEREST_DEBT,NET_DEBT,EBIT_INTEREST_EXPENSE,EBITDA_INTEREST_EXPENSE,REPORT_TYPE_CODE',
        'sortColumns':'REPORT_DATE',
        'sortTypes'	:'-1',
        'pageNumber':	'',
        'pageSize'	:'',
        'client':	'SW',
        'filter':	f'''(SECUCODE="{SECUCODE}");(ORG_CODE="~")(REPORT_DATE>='{开始日期}')(REPORT_DATE<='{结束日期}')''',
        }
        结果DT=抓取(财务表单)
        return 结果DT
#%%平台部分
class 平台类():
    def __init__(self):
        self.可下载方法=[mf for  mf in  平台类.__dict__.keys() if not mf.startswith('__')]
    def 平台财务(self,ISSUE_CODE,开始日期='2001-01-01',结束日期=今天):
        财务表单={'reportName'	:'RPT_BOND_BS_INFO;RPT_BOND_ISSUE_FINANCE',
        'columns'	:'SECUCODE,@ISSUE_CODE;@ORG_CODE,REPORT_DATE,REPORT_TYPE,CURRENCY,TOTAL_ASSETS,MONETARYFUNDS,NET_ASSETS,TOTAL_LIABILITIES,DEBT_ASSET_RATIO,NETPROFIT,OPERATE_INCOME,OPERATE_PROFIT,EBITDA,EBITDAZSR,MPROFIT_OPERATEREVE,MAIN_INCOME_RATE,ROA,ROE_WEIGHT,NETCASH_OPERATE,NETCASH_INVEST,TOTAL_FINANCE,OPERATE_EBITDA,INVENTORY_TR,CURRENT_RATIO,SPEED_RATIO,INTEREST_DEBT,NET_DEBT,EBIT_INTEREST_EXPENSE,EBITDA_INTEREST_EXPENSE,REPORT_TYPE_CODE',
        'sortColumns':'REPORT_DATE',
        'sortTypes'	:'-1',
        'pageNumber':	'',
        'pageSize'	:'' ,
        'client':	'SW',
        'filter':	f''';(ORG_CODE="{ISSUE_CODE}")(REPORT_DATE>='{开始日期} 00:00:00')(REPORT_DATE<='{结束日期} 23:59:59')''',
        }
        结果DT=抓取(财务表单)
        return 结果DT
    def 平台舆情(self,ISSUE_CODE,开始日期='2001-01-01',结束日期=今天):
        舆情表单={'reportName'	:'RPT_CUSTOM_BOND_REMIND_MERGE',
        'columns'	:'SECUCODE,NOTICE_DATE,SOURCE_URL,EVENT_TYPE_I,EVENT_TYPE_II,EVENT_TYPE_III,RISK_LEVEL,EVENT_SUMMARY,EVENT_DATE,MXID,EVENT_TYPE_CODEI,EVENT_TYPE_CODEII,EVENT_TYPE_CODEIII,EVENT_REASON,ISSUE_CODE,NEXT_STAGE_EVENT,BOND_NAME_ABBR',
        'sortColumns':'EVENT_DATE,NOTICE_DATE',
        'sortTypes'	:'-1,-1',
        'pageNumber':	'',
        'pageSize'	:'',
        'client':	'SW',
        'filter':  f'''(ISSUE_CODE="{ISSUE_CODE}")(EVENT_DATE>='{开始日期} 00:00:00')(EVENT_DATE<='{结束日期} 23:59:59')''',
        }
        结果DT=抓取(舆情表单)
        return 结果DT
    def 平台发债(self,ISSUE_CODE,开始日期='2001-01-01',结束日期=今天):#发行人所有债券
        表单={'reportName': 'RPT_BOND_BS_SAMEISSUER',
        'columns': '''ISSUE_CODE,CURRENCY,CREDIT_SUBJECT_NAME,IS_BOND_TYPE,SECURITY_NAME,SECUCODE,BOND_NAME_ABBR,SECURITY_TYPE,ISSUE_NAME,RAISE_WAY,ISSUE_DATE,VALUE_DATE,EXPIRE_DATE,ISSUE_SCALE,BOND_EXPIRE,REMAIN_DAY,RN,LISTING_PLACE,INTEREST_RATE_TYPE,FXCKLL,SPECIAL_CLAUSE,PARTY_NAME,VICE_PARTY_NAME,GUARANTEE,CHECK_STATUS,SECUCODE_RN,STATE''',
            'quoteColumns': '',
        'filter': '(ISSUE_CODE	="%s")(SECUCODE_RN=1))'%(ISSUE_CODE),
        'client': 'SW'}
        结果DT=抓取(表单)
        return 结果DT
# %%

if __name__=='__main_1_':
    债券类a=债券类()
    aa=债券类a.单债券的发行人财务('012103193.IB',开始日期='2022-01-01',结束日期='2024-08-02')
    #display(aa)
if __name__=='__main__':
    平台类a=平台类()
    aa=平台类a.平台发债('10000506',开始日期='2022-01-01',结束日期='2023-01-02')
    #display(aa)
# %%
if __name__=='__main__':
    板块名单类a=板块名单类()
    aa=板块名单类a.下载()