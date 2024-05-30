#%%

import CH抓取保存设定
import requests,json,os,time,sys 
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta
import pandas as pd
import urllib.parse
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()
#%%
print('开始，现在是',datetime.now().strftime('%Y年%m月%d号，%H点%M分%S秒'))
CH抓取保存设定.全部下载()
print('完成，现在是',datetime.now().strftime('%Y年%m月%d号，%H点%M分%S秒'))
# %%
# nohup /home/tongjisem/anaconda3/envs/mzb/bin/python /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.py >  /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.log &
# crontab -e
# 每周更新
# 1 0 * * 0   /home/tongjisem/anaconda3/envs/mzb/bin/python /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.py >  /home/tongjisem/Mzb/IFCH解包综合/5-CH解包/Choice_spyder/CH抓取.log &