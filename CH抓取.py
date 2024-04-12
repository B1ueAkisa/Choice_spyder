#%%

import CH抓取保存设定
import requests,json,os,time,sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import datetime
import pandas as pd
import urllib.parse
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()

# %%
#CH抓取保存设定.板块名单下载('全部发行人融资统计')
CH抓取保存设定.板块名单下载('城投发行人融资统计',是否删除旧文件=False)
# %%
