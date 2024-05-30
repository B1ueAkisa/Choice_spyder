#%%
import requests,json,os,time,sys,re
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
pool = ThreadPoolExecutor(max_workers=16,)
等待秒数=0.1
from datetime import datetime, timedelta

import pandas as pd
import urllib.parse
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()


今天 = datetime.now().strftime("%Y-%m-%d")
def N天列表(n):
    return pd.date_range(end=今天,periods=n).strftime("%Y-%m-%d").to_list()
def 真的今天(): return datetime.now().strftime("%Y-%m-%d")

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

class 其他数据处理():
    def 处理合并(DF,过往文件1):
        if  DF.empty : 
            return (过往文件1 if 过往文件1 is not None else pd.DataFrame())
        最终DF=pd.concat([DF,过往文件1],ignore_index=True)
        最终DF.drop_duplicates(inplace=True)
        最终DF.reset_index(drop=True,inplace=True)
        return 最终DF
    
#%% #前两个

class 板块名单(CH抓取源定义.板块名单类):
    def __init__(self) -> None:
        super().__init__()
        #print(f' {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}') 

    def 下载(self,需要的表单,是否删除旧文件=True):
        try:
            方法=getattr(self,需要的表单)
        except:
            print(f' 方法输入错误, {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
            sys.exit()
        文件夹=os.path.join(前置文件夹,'板块成分')
        文件名z=需要的表单+'%s.xlsx'%今天
        文件名=os.path.join(文件夹,文件名z)
        if os.path.exists(文件名):
            print(f'{文件名} 存在，跳过下载')
            return #pd.read_excel(文件名,engine='xlsxwriter')
        os.makedirs(文件夹,exist_ok=True)
        
        DT=方法()
        DT.to_excel(文件名)
        print(需要的表单,'成功保存到',文件名)
        if 是否删除旧文件:
            过往文件lt=[wjm for wjm in os.listdir(文件夹) if wjm.startswith(需要的表单) and (wjm !=文件名z)]
            for 过往文件 in 过往文件lt:
                os.remove(os.path.join(文件夹,过往文件))
                print(过往文件,'删除 ')
        return DT
    
    def 平台名单获取(self,是否城投=False):
        文件夹=os.path.join(前置文件夹,'板块成分')
        os.makedirs(文件夹,exist_ok=True)
        lt=['全部发行人融资统计', '城投发行人融资统计']
        if 是否城投:需要的表单=lt[1]
        else:需要的表单=lt[0]
        过往文件lt=[wjmq for wjmq in os.listdir(文件夹) if wjmq.startswith(需要的表单) ]
        过往文件lt.sort()
        列名='ISSUE_CODE'
        if len(过往文件lt)>0:
            DT=pd.read_excel(os.path.join(文件夹,过往文件lt[-1]),usecols=[列名],dtype='str')
        else:
            DT=self.下载(需要的表单)
        return DT[列名]

class 违约下载(CH抓取源定义.违约类):
    def __init__(self) -> None:
        super().__init__()
        #print(f' {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
    def 下载(self,需要的表单,是否删除旧文件=True):
        try:
            方法=getattr(self,需要的表单)
        except:
            print(f' 方法输入错误, {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
            sys.exit()
        文件夹=os.path.join(前置文件夹,'违约')
        文件名z=需要的表单+'%s.xlsx'%今天
        文件名=os.path.join(文件夹,文件名z)
        if os.path.exists(文件名):
            print(f'{文件名} 存在，跳过下载')
            return 
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



#%% 平台

class 平台为主体下载(CH抓取源定义.平台类,板块名单):
    def __init__(self) -> None:
        super().__init__()
        #print(f' {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
    def 下载(self,需要的表单,是否城投=False,几日内不更新=30):
        try:
            方法=getattr(self,需要的表单)
        except:
            print(f' 方法输入错误, {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
            sys.exit()
        板块名单a1=板块名单()
        平台名单=板块名单a1.平台名单获取(是否城投=是否城投)
        del 板块名单a1
        目标文件夹=os.path.join(前置文件夹,'平台',需要的表单)
        os.makedirs(目标文件夹,exist_ok=True)
        已有结果=pd.DataFrame((os.path.splitext(x)[0].split('更新于') for x in  os.listdir(目标文件夹)),columns=['代码','后缀'])
        时间=已有结果.后缀.str.replace('数据为空','',regex=False).astype('datetime64[ns]')
        这几天结果=set(已有结果[(pd.to_datetime(今天)-时间).dt.days<几日内不更新].代码)
        目标名单=set(平台名单) -这几天结果
        
        def 内置保存(发行人代码):
            过往文件dt=已有结果[已有结果['代码']==发行人代码].copy()
            过往文件lt=过往文件dt['代码']+'更新于'+过往文件dt['后缀']+'.csv'
            if  re.search('舆情|行情', 需要的表单) and len(过往文件lt)>0:
                过往文件1名=过往文件lt.values[0]
                if '数据为空' in 过往文件1名:    过往文件1=None
                else:
                    过往文件1=pd.read_csv(os.path.join(目标文件夹,过往文件1名),index_col=0,dtype=str)
                    if 过往文件1.empty:过往文件1=None
                过往文件1更新日期=过往文件dt['后缀'].iloc[0][:10]
                DF=方法(发行人代码,开始日期=过往文件1更新日期)
            else:  DF=方法(发行人代码);过往文件1=None
            if type(DF) ==str:
                if DF=='返回数据为空':   DF= pd.DataFrame()
                else:  print(DF); DF=None
            if DF is None:
                print(发行人代码,end=' fail ')
                #return
            else:
                最终DF=其他数据处理.处理合并(DF,过往文件1)
                数据为空=('数据为空' if 最终DF.empty else '')              
                最终DF.to_csv(os.path.join(目标文件夹,发行人代码+'更新于'+今天+数据为空+'.csv'))
                for 过往文件 in 过往文件lt:os.remove(os.path.join(目标文件夹,过往文件)) 
               
            time.sleep(等待秒数)
        res=list(tqdm(pool.map(内置保存, 目标名单,chunksize=20),total=len(目标名单),mininterval=50,desc=目标文件夹))
        
#%%债券
class 债券为主体下载(CH抓取源定义.债券类,板块名单):
    def __init__(self) -> None:
        super().__init__()
        #print(f' {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
    def 下载(self,需要的表单,是否城投=False,几日内不更新=30):
        try:
            方法=getattr(self,需要的表单)
        except:
            print(f' 方法输入错误, {self.__class__.__name__} 的 可下载方法有： {self.可下载方法}')
            sys.exit()
        板块名单a1=板块名单()
        债券名单=板块名单a1.平台名单获取(是否城投=是否城投)
        del 板块名单a1
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
            时间=已有结果.后缀.str.replace('数据为空','',regex=False).astype('datetime64[ns]')
            这几天结果=set(已有结果[(pd.to_datetime(今天)-时间).dt.days<几日内不更新].代码)
            目标名单=set(旗下所有债券) -这几天结果   
            def 内置保存(债券代码):
                过往文件dt=已有结果[已有结果['代码']==债券代码].copy()
                过往文件lt=过往文件dt['代码']+'更新于'+过往文件dt['后缀']+'.csv'
                
                if  re.search('舆情|行情', 需要的表单) and len(过往文件lt)>0 :
                    过往文件1名=过往文件lt.values[0]
                    if '数据为空' in 过往文件1名:过往文件1=None
                    else:
                        过往文件1=pd.read_csv(os.path.join(存储文件夹,过往文件1名),index_col=0,dtype=str)
                        if 过往文件1.shape[0]==0:过往文件1=None
                    过往文件1更新日期=过往文件dt['后缀'].iloc[0][:10]
                    DF=方法(债券代码,开始日期=过往文件1更新日期)
                else:  DF=方法(债券代码);过往文件1=None
                if type(DF) ==str:
                    if DF=='返回数据为空':
                        DF= pd.DataFrame()
                    else:  print(DF); DF=None
                if DF is None:
                    print(债券代码,end=' fail ')
                else:
                    最终DF=其他数据处理.处理合并(DF,过往文件1)
                    数据为空=('数据为空' if 最终DF.empty else '')              
                    最终DF.to_csv(os.path.join(存储文件夹,债券代码+'更新于'+今天+数据为空+'.csv'))
                    for 过往文件 in 过往文件lt:os.remove(os.path.join(存储文件夹,过往文件)) 
                    time.sleep(等待秒数)
            for 债券代码 in 目标名单:
                内置保存(债券代码)
        res=list(tqdm(pool.map(单平台所有指定, 目标更新主体['代码'],chunksize=20),total=len(目标更新主体['代码']),mininterval=50,desc=需要的表单))


#%%

板块名单a=板块名单()
违约下载a=违约下载()
平台为主体下载a=平台为主体下载()
债券为主体下载a=债券为主体下载()
for 实例 in [板块名单a,违约下载a,平台为主体下载a,债券为主体下载a]:
    print(f' {实例.__class__.__name__} 的 可下载方法有： {实例.可下载方法}')
#%%


def 全部下载():
    for 实例 in [板块名单a,违约下载a,平台为主体下载a,债券为主体下载a]:
        for 方法 in 实例.可下载方法:
            方法变量名表=实例.下载.__code__.co_varnames
            输入变量kwargs={}
            if '几日内不更新' in 方法变量名表:
                输入变量kwargs['几日内不更新']=(3 if re.search('舆情|行情|发债', 方法) else 60)
            实例.下载(方法,**输入变量kwargs)
            print('现在是',datetime.now().strftime('%Y年%m月%d号，%H点%M分%S秒'))
    
#%%


if __name__=='1__main__':
    名单lt=['全部发行人融资统计', '城投发行人融资统计']
    #for bd in 名单lt: 板块名单a.下载(bd,)
    #for bd in 违约下载a.可下载方法:违约下载a.下载(bd,)
    #for 方法 in 平台为主体下载a.可下载方法:平台为主体下载a.下载(方法)
    for 方法 in 债券为主体下载a.可下载方法:债券为主体下载a.下载(方法)
if __name__=='__main__':
    平台为主体下载a.下载('平台舆情',几日内不更新=3)
# %%