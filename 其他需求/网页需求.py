import requests,json
import pandas as pd


def 机构席位追踪(跨度='近一月'):
    跨={"近一月":'01', "近三月":'02', "近六月":'03', "近一年":'04'}
    if not 跨度 in 跨.keys():
        print('跨度错误')
        return 
    跨度str=跨[跨度]
    url='https://datacenter-web.eastmoney.com/api/data/v1/get?'
    表单={
    'callback': 'jQuery112301118753618504218_1714627428368',
    'sortColumns': 'ONLIST_TIMES,SECURITY_CODE',
    'sortTypes': '-1,1',
    'pageSize': '50',
    'pageNumber': 1,
    'reportName': 'RPT_ORGANIZATION_SEATNEW',
    'columns': 'ALL',
    'source': 'WEB',
    'client': 'WEB',
    'filter': f'(STATISTICSCYCLE="{跨度str}")',}
    page=1
    结果列表=[]
    while True:
            表单['pageNumber']=page
            response = requests.get(url,params=表单,timeout=500, verify=False)#cookies=cookies,
            response.close()
            txxx=response.text
            txxx=txxx.replace('jQuery112301118753618504218_1714627428368(','').strip(');')
            try:
                结果dict=json.loads(txxx)
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
a=机构席位追踪()
a