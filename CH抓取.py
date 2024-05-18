#%%

import CH抓取保存设定
import requests,json,os,time,sys,datetime 
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import datetime
import pandas as pd
import urllib.parse
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()
#%%
print('今天是',datetime.date.today().strftime("%Y-%m-%d"))
CH抓取保存设定.全部下载()
# %%
# nohup /home/tongjisem/anaconda3/envs/mzb/bin/python /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.py >  /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.log &
# crontab -e
# 每周更新
# 1 0 * * 0  nohup /home/tongjisem/anaconda3/envs/mzb/bin/python /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.py >  /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.log &