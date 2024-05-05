#%%
import requests,json,os,time,sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
pool = ThreadPoolExecutor(max_workers=16)
等待秒数=0.1
from datetime import datetime, timedelta
import pandas as pd
import urllib.parse
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()

def N天列表(n):
     return pd.date_range(end=今天,periods=n).strftime("%Y-%m-%d").to_list()

今天 = time.strftime("%Y-%m-%d",time.localtime(time.time()))
def 真的今天():
     return time.strftime("%Y-%m-%d",time.localtime(time.time()))

#%%
import CH抓取配置,CH抓取源定义
前置文件夹=CH抓取配置.目标数据文件夹

位置分配=f'''
位置存储:
{前置文件夹}
    /板块成分
        名单
    /违约
    /债券主体
        行情，新闻
    /平台主体
        发债，财务，新闻
'''

板块名单类a=CH抓取源定义.板块名单类()
违约类a=CH抓取源定义.违约类()
对应类a=CH抓取源定义.对应类()
平台类a=CH抓取源定义.平台类()
债券类a=CH抓取源定义.债券类()
print(板块名单类a.__class__,'方法如下',[mf for mf in 板块名单类a.__dir__() if not mf.startswith('__')])
print(平台类a.__class__,'方法如下',[mf for mf in 平台类a.__dir__() if not mf.startswith('__')])
print(债券类a.__class__,'方法如下',[mf for mf in 债券类a.__dir__() if not mf.startswith('__')])
#%% #前两个
def 板块名单下载(需要的表单,是否删除旧文件=True):
    try:
        方法=getattr(板块名单类a,需要的表单)
    except:
        print('方法输入错误',板块名单类a.__class__,'方法如下',[mf for mf in 板块名单类a.__dir__() if not mf.startswith('__')])
        sys.exit()
    文件夹=os.path.join(前置文件夹,'板块成分')
    文件名z=需要的表单+'%s.xlsx'%今天
    文件名=os.path.join(文件夹,文件名z)
    os.makedirs(文件夹,exist_ok=True)
    DT=方法()
    DT.to_excel(文件名)
    print(需要的表单,'成功保存到',文件名)
    if 是否删除旧文件:
        过往文件lt=[wjm for wjm in os.listdir(文件夹) if wjm.startswith(需要的表单) and (wjm !=文件名z)]
        for 过往文件 in 过往文件lt:
            os.remove(os.path.join(文件夹,过往文件))
            print(过往文件,end='删除 ')
    return DT
        
def 违约(是否删除旧文件=True):
    DT=违约类a.违约下载()
    文件夹=os.path.join(前置文件夹,'违约')
    文件名z='违约%s.xlsx'%今天
    文件名=os.path.join(文件夹,文件名z)
    os.makedirs(文件夹,exist_ok=True)
    DT.to_excel(文件名)
    print('违约 成功保存到',文件名)
    if 是否删除旧文件:
        过往文件lt=[wjm for wjm in os.listdir(文件夹) if wjm.startswith('违约') and (wjm !=文件名z)]
        for 过往文件 in 过往文件lt:
            os.remove(os.path.join(文件夹,过往文件))
            print(过往文件,end='删除 ')
    return DT

#%%平台
def 平台名单获取(是否城投=False):
    文件夹=os.path.join(前置文件夹,'板块成分')
    lt=['全部发行人融资统计', '城投发行人融资统计']
    if 是否城投:需要的表单=lt[1]
    else:需要的表单=lt[0]
    过往文件lt=[wjmq for wjmq in os.listdir(文件夹) if wjmq.startswith(需要的表单) ]
    过往文件lt.sort()
    if len(过往文件lt)>0:
        DT=pd.read_excel(os.path.join(文件夹,过往文件lt[-1]),usecols=['ISSUE_CODE'],dtype='str')
    else:
        DT=板块名单下载(需要的表单)
    return DT['ISSUE_CODE']



def 平台名单下载(需要的表单,是否城投=False,几日内不更新=30):
    方法=getattr(平台类a,需要的表单)
    平台名单=平台名单获取(是否城投=是否城投)
    目标文件夹=os.path.join(前置文件夹,'平台',需要的表单)
    os.makedirs(目标文件夹,exist_ok=True)
    已有结果=pd.DataFrame((os.path.splitext(x)[0].split('更新于') for x in  os.listdir(目标文件夹)),columns=['代码','后缀'])
    时间=已有结果.后缀.str.replace('数据为空','',regex=False).astype('datetime64')
    这几天结果=set(已有结果[(pd.to_datetime(今天)-时间).dt.days<几日内不更新].代码)
    目标名单=set(平台名单) -这几天结果
    def 内置保存(发行人代码):
        DF=方法(发行人代码)
        数据为空=''
        if type(DF) ==str:
            if DF=='返回数据为空':
                数据为空=DF[2:]
                DF= pd.DataFrame()
            else:   DF=None
        if DF is None:
            print()
            print(发行人代码,end=' fail ')
            return
        过往文件lt=[os.path.join(目标文件夹,x[0]+'更新于'+x[1] +'.csv')for id,  x in (已有结果[已有结果.代码==发行人代码]).iterrows()]
        DF.to_csv(os.path.join(目标文件夹,发行人代码+'更新于'+今天+数据为空+'.csv'))

        for 过往文件 in 过往文件lt:os.remove(过往文件)    
        time.sleep(等待秒数)
    re=list(tqdm(pool.map(内置保存, 目标名单),total=len(目标名单),desc=目标文件夹))

#%%债券
def 债券名单下载(需要的表单,是否城投=False,几日内不更新=30):
    方法=getattr(债券类a,需要的表单)
    债券名单=平台名单获取(是否城投=是否城投)
    发债文件夹=os.path.join(前置文件夹,'平台','平台发债')
    发债信息lt=pd.Series(os.listdir(发债文件夹))
    已有发债结果=pd.DataFrame((os.path.splitext(x)[0].split('更新于') for x in  os.listdir(发债文件夹 ) ),columns=['代码','后缀'])
    目标更新主体=已有发债结果[已有发债结果['代码'].isin(债券名单)]
    def 单平台所有指定(发行人代码):
        目标文件=发债信息lt[发债信息lt.str.startswith(发行人代码)]
        if len(目标文件)>0:
            if '数据为空' in 目标文件.iloc[0]:return
            目标文件名=os.path.join(发债文件夹,目标文件.iloc[0])
        else :return
        try:
            旗下所有债券=set(pd.read_csv(目标文件名,usecols=['SECUCODE'],dtype=str)['SECUCODE'] )	
        except pd.errors.EmptyDataError as e: return
        if len(旗下所有债券)==0:return
        存储文件夹=os.path.join(前置文件夹,'债券',需要的表单,发行人代码)
        os.makedirs(存储文件夹,exist_ok=True)
        已有结果=pd.DataFrame((os.path.splitext(x)[0].split('更新于') for x in  os.listdir(存储文件夹)),columns=['代码','后缀'])
        时间=已有结果.后缀.str.replace('数据为空','',regex=False).astype('datetime64')
        这几天结果=set(已有结果[(pd.to_datetime(今天)-时间).dt.days<几日内不更新].代码)
        目标名单=set(旗下所有债券) -这几天结果
        for 债券代码 in 目标名单:
            DF=方法(债券代码)
            数据为空=''
            if type(DF) ==str:
                if DF=='返回数据为空':
                    数据为空=DF[2:]
                    DF= pd.DataFrame()
                else:
                    print(DF,end=' ')   
                    DF=None
            if DF is None:
                print(债券代码,end=' fail ')
                continue
            DF.to_csv(os.path.join(存储文件夹,债券代码+'更新于'+今天+数据为空+'.csv'))
            过往文件lt=已有结果[已有结果['代码']==债券代码].copy()
            过往文件lt=过往文件lt['代码']+'更新于'+过往文件lt['代码']+'.csv'
            for 过往文件 in 过往文件lt:os.remove(os.path.join(存储文件夹,过往文件)) 
            time.sleep(等待秒数)
        #re=list(pool.map(内置保存, 目标名单))
    '''for 发行人代码 in tqdm(目标更新主体['代码'],desc=需要的表单):
        单平台所有指定(发行人代码)'''
    re=list(tqdm(pool.map(单平台所有指定, 目标更新主体['代码']),total=len(目标更新主体['代码']),desc=需要的表单))

#%%
if __name__=='__main__':

    
    平台需要的表单=['平台舆情','平台财务',  '平台发债']
    for bd in 平台需要的表单:
        平台名单下载(bd,是否城投=False,几日内不更新=30)
        ''''''
# %%
'''if __name__=='__main__':
    债券需要的表单=['单债券行情', '单债券舆情']#['单债券舆情']#
    for bd in 债券需要的表单:
        债券名单下载(bd,是否城投=False,几日内不更新=30)'''


# %%