#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[15]:


#!/usr/bin/env python
# coding: utf-8

# In[36]:


#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import shutil
import os
import re
import numpy as np
import configparser
import time
import tkinter as tk
from tkinter import messagebox

total_mode_list = ['NT','HT','LT']
new_ub_list_HSD = []
new_lb_list_HSD = []
new_ub_list_LSD = []
new_lb_list_LSD = []
# Get current time to append to the filename
current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
# 获取当前时间用于日志文件命名
log_file = fr"D:\XLScript\PAT_LOG-XL008-FT2-{current_time}.txt" 
# 打开日志文件用于写入
with open(log_file, 'w') as log:
    # csv_name_rules = ['CLA5411S_','FT1']
    # mode_list = ['NT']
    log.write('PAT log:\n')
    # target_col_list = ['IO_NTest-INN_N','IO_NTest-INP_N','IO_NTest-STANDBY_N','IO_NTest-FAULT_N',
    # 'IO_NTest-MUTE_N','IO_NTest-SDA_N','IO_NTest-SCL_N','IO_NTest-BSTN_N',
    # 'IO_NTest-BSTP_N','OUT_NTest-OUTN_IO','OUT_NTest-OUTP_IO','POWER_NTest-PVDD',
    # 'POWER_NTest-BYP','IO_PTest-FAULTZ_P','IO_PTest-MUTE_P','OUT_PTest-OUTN_IO',
    # 'OUT_PTest-OUTP_IO','POWER_PTest1-BYP','POWER_PTest2-BYP']
    pin_group_dict = {
    'IIS_PINS':['MCLK','SCLK','FSYNC','SDIN1','SDIN2'],
    'IIC_PINS':['SDA','SCL'],
    'DTBUS':['SDOUT','ADDR0','ADDR1','MUTE'],
    'ATBUS':['FAULT','WARN'],
    'BST_PINS':['BST_1M','BST_1P','BST_2M','BST_2P','BST_3M','BST_3P','BST_4M','BST_4P'],
    'OUT_PINS':['OUT_1P','OUT_1M','OUT_2P','OUT_2M','OUT_3P','OUT_3M','OUT_4P','OUT_4M'],
    'SCAN_PINS':['SDOUT','FSYNC','SDIN1','SDIN2','MCLK','MUTE','SCLK'],
    'TMU_PINS':['CD_Diag_TMU','ENABLE3_TMU','ENABLE2_TMU','ENABLE1_TMU','MUTE_TMU'],
    'EN_PINS':['ENABLE1','ENABLE2','ENABLE3'],
    'CP_PINS':['Vddcp','Cpump1','Cpump2'],
    'VddCP':['Vddcp']
    }
    
    
    csv_name_rules = ['CLD801','FT1']

    csv_name_rules1 = ['CCD12079','FT1']
    mode_list = ['HT']
    
    target_col_list = ['Leakage_test_HSD-OUT_1P','Leakage_test_HSD-OUT_1M','Leakage_test_HSD-OUT_2P','Leakage_test_HSD-OUT_2M',
                       'Leakage_test_HSD-OUT_3P','Leakage_test_HSD-OUT_3M','Leakage_test_HSD-OUT_4P','Leakage_test_HSD-OUT_4M',
                       'Leakage_test_LSD-OUT_1P','Leakage_test_LSD-OUT_1M','Leakage_test_LSD-OUT_2P','Leakage_test_LSD-OUT_2M',
                       'Leakage_test_LSD-OUT_3P','Leakage_test_LSD-OUT_3M','Leakage_test_LSD-OUT_4P','Leakage_test_LSD-OUT_4M',
                       'VBAT_idle_current-VBAT_IO','PVDD_idle_current-PVDD_IO','DVDD_current-DVDD',
                       'PVDD_OV-PVDD_OV','PVDD_OV_HYS-PVDD_OV_HYS','PVDD_UV-PVDD_UV','PVDD_UV_HYS-PVDD_UV_HYS',
                       'VBAT_OV-VBAT_OV','VBAT_OV_HYS-VBAT_OV_HYS','VBAT_UV-VBAT_UV','VBAT_UV_HYS-VBAT_UV_HYS',
                       'GVDD_CHECK_AF-A5VSVR','VBG_AF-VBG_AF','LDO_V_AF-D1e8SVR','VDDCP_V_AF-VddCP',
                       'PVDD_ISD-PVDD_IO','BG_4uA_AF-BG_4uA_AF',
                        'Res_test_BF-RES_OUT1P_BF', 'Res_test_BF-RES_OUT1M_BF',
                        'Res_test_BF-RES_OUT2P_BF', 'Res_test_BF-RES_OUT2M_BF',                                                                                                   
                        'Res_test_BF-RES_OUT3P_BF','Res_test_BF-RES_OUT3M_BF',                                                    
                        'Res_test_BF-RES_OUT4P_BF', 'Res_test_BF-RES_OUT4M_BF', 
                        'Res_test_BF-RES_SDA_BF',  
                        'Res_test_BF-RES_SDA_BF', 
                        'Res_test_BF-RES_SCL_BF',
                        'Res_test_BF-RES_SCLK_BF','Res_test_BF-RES_FSYNC_BF','Res_test_BF-RES_SDIN1_BF',
                        'Res_test_BF-RES_SDIN2_BF','Res_test_BF-RES_CPump1_BF','Res_test_BF-RES_CPump2_BF',
                        'Res_test_BF-RES_VDDCP_BF','Res_test_BF-RES_ENABLE1_BF','Res_test_BF-RES_ENABLE2_BF',
                        'Res_test_BF-RES_ENABLE3_BF','Res_test_BF-RES_MUTE_BF',	'Res_test_BF-RES_CD_Diag_BF',
                        'Res_test_BF-RES_PVDD_IO_BF','Res_test_BF-RES_D1e8SVR_BF','Res_test_BF-RES_A5VSVR_BF',
                        'Res_test_AF-RES_OUT1P_AF', 'Res_test_AF-RES_OUT1M_AF',
                        'Res_test_AF-RES_OUT2P_AF', 
                        'Res_test_AF-RES_OUT2M_AF', 
                        'Res_test_AF-RES_OUT3P_AF','Res_test_AF-RES_OUT3M_AF',
                        'Res_test_AF-RES_OUT4P_AF', 'Res_test_AF-RES_OUT4M_AF', 
                        'Res_test_AF-RES_SDA_AF', 
                        'Res_test_AF-RES_SCL_AF',
                        'Res_test_AF-RES_SCLK_AF','Res_test_AF-RES_FSYNC_AF','Res_test_AF-RES_SDIN1_AF',
                        'Res_test_AF-RES_SDIN2_AF','Res_test_AF-RES_CPump1_AF','Res_test_AF-RES_CPump2_AF',
                        'Res_test_AF-RES_VDDCP_AF','Res_test_AF-RES_ENABLE1_AF','Res_test_AF-RES_ENABLE2_AF',
                        'Res_test_AF-RES_ENABLE3_AF','Res_test_AF-RES_MUTE_AF',	'Res_test_AF-RES_CD_Diag_AF',
                        'Res_test_AF-RES_PVDD_IO_AF','Res_test_AF-RES_D1e8SVR_AF','Res_test_AF-RES_A5VSVR_AF',
                        'Res_test_DEL-RES_OUT1P_DEL', 'Res_test_DEL-RES_OUT1M_DEL','Res_test_DEL-RES_OUT2P_DEL', 
                        'Res_test_DEL-RES_OUT2M_DEL', 'Res_test_DEL-RES_OUT3P_DEL', 'Res_test_DEL-RES_OUT3M_DEL',
                        'Res_test_DEL-RES_OUT4P_DEL', 
                        'Res_test_DEL-RES_OUT4M_DEL','Res_test_DEL-RES_SDA_DEL', 'Res_test_DEL-RES_SCL_DEL',
                        'Res_test_DEL-RES_SCLK_DEL','Res_test_DEL-RES_FSYNC_DEL','Res_test_DEL-RES_SDIN1_DEL',
                        'Res_test_DEL-RES_SDIN2_DEL','Res_test_DEL-RES_CPump1_DEL','Res_test_DEL-RES_CPump2_DEL',
                        'Res_test_DEL-RES_VDDCP_DEL','Res_test_DEL-RES_ENABLE1_DEL','Res_test_DEL-RES_ENABLE2_DEL',
                        'Res_test_DEL-RES_ENABLE3_DEL','Res_test_DEL-RES_MUTE_DEL',	'Res_test_DEL-RES_CD_Diag_DEL',
                        'Res_test_DEL-RES_PVDD_IO_DEL','Res_test_DEL-RES_D1e8SVR_DEL','Res_test_DEL-RES_A5VSVR_DEL',
                        'Res_test_DEL-RES_OUT1P_DEL',  
                         'Res_test_DEL-RES_OUT1M_DEL',  
                         'Res_test_DEL-RES_OUT2P_DEL',  
                         'Res_test_DEL-RES_OUT2M_DEL' ]
    
    def get_static_func1(data_list,col):
        return static_list
    
    def mean_max_func1(static_list,col):
        new_lb = sat[col][0]
        new_ub = sat[col][1]
        new_mean = static_list[0]
        print(f'#######col -{new_lb}')
        print(f'#######col -{new_ub}')
        print(f'#######col -{new_mean}')
        old_mean = (sat[col][1] + sat[col][0])/2
        if('Leakage_test' in col ):
            if(abs(new_mean-old_mean)> (abs(sat[col][1] - sat[col][0])) * 0.5):
                if(new_mean < old_mean):
                    new_mean = old_mean - ((abs(sat[col][1] - sat[col][0])) * 0.5)
                    print(f'{col}新数据偏离旧数据百分之二十且中心值下偏\n')
                    log.write(f'{col}: The new data deviates from the old data by twenty percent and the central value is lower.\n')
                else:
                    new_mean = old_mean + ((abs(sat[col][1] - sat[col][0])) * 0.5)
                    print(f'{col}新数据偏离旧数据百分之二十且中心值上偏\n')
                    log.write(f'{col}: The new data deviates from the old data by twenty percent and the central value is biased upwards.\n')  

        else:
            if(abs(new_mean-old_mean)> (abs(sat[col][1] - sat[col][0])) * 0.5):
                if(new_mean < old_mean):
                    new_mean = old_mean - ((abs(sat[col][1] - sat[col][0])) * 0.5)
                    print(f'{col}新数据偏离旧数据百分之十且中心值下偏\n')
                    log.write(f'{col}: The new data deviates from the old data by twenty percent and the central value is lower.\n')
                else:
                    new_mean = old_mean + ((abs(sat[col][1] - sat[col][0])) * 0.5)
                    print(f'{col}新数据偏离旧数据百分之十且中心值上偏\n')
                    log.write(f'{col}: The new data deviates from the old data by twenty percent and the central value is biased upwards.\n')     
        if('PVDD_ISD' not in col and 'rePVDD_ISD' not in col and 'Leakage_test' not in col  and 'VBG_AF' not in col 
           and 'Rdson' not in col and 'REIO_Pins' not in col and 'REDPS_POWER_L' not in col and 'Res_test' not in col ):
            if (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,2)
                new_ub = round(new_mean + sat[col][4] * 3,2)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')
        elif('REIO_Pins' in col):
            old_weight = abs((sat[col][1] - sat[col][0])/2);
            print(f'{col} weight {old_weight} mv')
            new_lb = round(new_mean - old_weight,2);
            new_ub = round(new_mean + old_weight,2);
            print(f'{col}Central value has shifted')
            log.write(f'{col}: Central value has shifted')
        elif('REDPS_POWER_L'  in col):
            old_weight = abs((sat[col][1] - sat[col][0])/2);
            print(f'{col} weight {old_weight} mv')
            new_lb = round(new_mean - old_weight,2);
            new_ub = round(new_mean + old_weight,2);
            print(f'{col}Central value has shifted')
            log.write(f'{col}: Central value has shifted')
        elif('BG_4uA' in col):
            if (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            # elif (sat[col][4] * 7.8) <= sat[col][1] - sat[col][0]:
            #     new_lb = round(new_mean - sat[col][4] * 3.9,2)
            #     new_ub = round(new_mean + sat[col][4] * 3.9,2)
            #     print(f'{col}使用3.9σ\n')
            #     log.write(f'{col}: use3.9σ\n')
            else:
                old_weight = abs((sat[col][1] - sat[col][0])/2);
                print(f'{col} weight {old_weight} uA')
                new_lb = round(new_mean - old_weight,2);
                new_ub = round(new_mean + old_weight,2);
                print(f'{col}Central value has shifted')
                log.write(f'{col}: Central value has shifted')                
        elif('PVDD_ISD'  in col):
            if (sat[col][4] * 18) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 9,2)
                new_ub = round(new_mean + sat[col][4] * 9,2)
                print(f'{col}使用9σ\n')
                log.write(f'{col}: use9σ\n')
            elif (sat[col][4] * 16) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 8,2)
                new_ub = round(new_mean + sat[col][4] * 8,2)
                print(f'{col}使用8σ\n')
                log.write(f'{col}: use8σ\n')
            elif (sat[col][4] * 14) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7,2)
                new_ub = round(new_mean + sat[col][4] * 7,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,2)
                new_ub = round(new_mean + sat[col][4] * 3,2)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')
        elif('rePVDD_ISD'  in col):
            if (sat[col][4] * 18) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 9,2)
                new_ub = round(new_mean + sat[col][4] * 9,2)
                print(f'{col}使用9σ\n')
                log.write(f'{col}: use9σ\n')
            elif (sat[col][4] * 16) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 8,2)
                new_ub = round(new_mean + sat[col][4] * 8,2)
                print(f'{col}使用8σ\n')
                log.write(f'{col}: use8σ\n')
            elif (sat[col][4] * 14) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7,2)
                new_ub = round(new_mean + sat[col][4] * 7,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,2)
                new_ub = round(new_mean + sat[col][4] * 3,2)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')  
        elif('VBG_AF' in col):
            if (sat[col][4] * 18) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 9,3)
                new_ub = round(new_mean + sat[col][4] * 9,3)
                print(f'{col}使用9σ\n')
                log.write(f'{col}: use9σ\n')
            elif (sat[col][4] * 16) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 8,3)
                new_ub = round(new_mean + sat[col][4] * 8,3)
                print(f'{col}使用8σ\n')
                log.write(f'{col}: use8σ\n')
            elif (sat[col][4] * 14) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7,3)
                new_ub = round(new_mean + sat[col][4] * 7,3)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,3)
                new_ub = round(new_mean + sat[col][4] * 6,3)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,3)
                new_ub = round(new_mean + sat[col][4] * 5,3)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,3)
                new_ub = round(new_mean + sat[col][4] * 4,3)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,3)
                new_ub = round(new_mean + sat[col][4] * 3,3)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')
        elif('Leakage_test_HSD' in col):
            if (sat[col][4] * 18) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 9,2)
                new_ub = round(new_mean + sat[col][4] * 9,2)
                print(f'{col}使用9σ\n')
                log.write(f'{col}: use9σ\n')
            elif (sat[col][4] * 16) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 8,2)
                new_ub = round(new_mean + sat[col][4] * 8,2)
                print(f'{col}使用8σ\n')
                log.write(f'{col}: use8σ\n')
            elif (sat[col][4] * 15) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7.5,2)
                new_ub = round(new_mean + sat[col][4] * 7.5,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 14) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7,2)
                new_ub = round(new_mean + sat[col][4] * 7,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,2)
                new_ub = round(new_mean + sat[col][4] * 3,2)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')
            if  new_lb < -900 :
                new_lb = -900
            print(f'{col} ub:{new_ub},lb:{new_lb}\n')
            log.write(f'{col} ub:{new_ub},lb:{new_lb}\n')
            new_ub_list_HSD.append(new_ub)
            new_ub=max(new_ub_list_HSD)
            new_lb_list_HSD.append(new_lb)  
            new_lb=min(new_lb_list_HSD)
            print(f'{new_ub_list_HSD}\n')
            print(f'{new_lb_list_HSD}\n')
            log.write(f'{new_ub_list_HSD}\n')
            log.write(f'{new_lb_list_HSD}\n')
        elif('Leakage_test_LSD' in col):
            if (sat[col][4] * 18) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 9,2)
                new_ub = round(new_mean + sat[col][4] * 9,2)
                print(f'{col}使用9σ\n')
                log.write(f'{col}: use9σ\n')
            elif (sat[col][4] * 16) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 8,2)
                new_ub = round(new_mean + sat[col][4] * 8,2)
                print(f'{col}使用8σ\n')
                log.write(f'{col}: use8σ\n')
            elif (sat[col][4] * 15) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7.5,2)
                new_ub = round(new_mean + sat[col][4] * 7.5,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 14) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7,2)
                new_ub = round(new_mean + sat[col][4] * 7,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,2)
                new_ub = round(new_mean + sat[col][4] * 3,2)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')
            print(f'{col} ub:{new_ub},lb:{new_lb}\n')
            
            if  new_ub > 900 :
                new_ub = 900
            log.write(f'{col} ub:{new_ub},lb:{new_lb}\n')
            new_ub_list_LSD.append(new_ub)
            new_ub=max(new_ub_list_LSD)
            new_lb_list_LSD.append(new_lb)  
            new_lb=min(new_lb_list_LSD)
            print(f'{new_ub_list_LSD}\n')
            print(f'{new_lb_list_LSD}\n')
            log.write(f'{new_ub_list_LSD}\n')
            log.write(f'{new_lb_list_LSD}\n')
        elif('Rdson' in col):
            if (sat[col][4] * 15) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7.5,2)
                new_ub = round(new_mean + sat[col][4] * 7.5,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 14) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 7,2)
                new_ub = round(new_mean + sat[col][4] * 7,2)
                print(f'{col}使用7σ\n')
                log.write(f'{col}: use7σ\n')
            elif (sat[col][4] * 12) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 6,2)
                new_ub = round(new_mean + sat[col][4] * 6,2)
                print(f'{col}使用6σ\n')
                log.write(f'{col}: use6σ\n')
            elif (sat[col][4] * 10) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 5,2)
                new_ub = round(new_mean + sat[col][4] * 5,2)
                print(f'{col}使用5σ\n')
                log.write(f'{col}: use5σ\n')
            elif (sat[col][4] * 8) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 4,2)
                new_ub = round(new_mean + sat[col][4] * 4,2)
                print(f'{col}使用4σ\n')
                log.write(f'{col}: use4σ\n')
            elif (sat[col][4] * 6) <= sat[col][1] - sat[col][0]:
                new_lb = round(new_mean - sat[col][4] * 3,2)
                new_ub = round(new_mean + sat[col][4] * 3,2)
                print(f'{col}使用3σ\n')
                log.write(f'{col}: use3σ\n')

        elif('Res_test' in col):
            if(abs(new_mean-old_mean) <= (abs(sat[col][1] - sat[col][0])) * 0.3):
                new_lb = round((new_mean - (abs(sat[col][1] - sat[col][0]))/2),2)
                new_ub = round((new_mean + (abs(sat[col][1] - sat[col][0]))/2),2)
            else:
                new_lb = sat[col][0]
                new_ub = sat[col][1]


        else:
            new_lb = sat[col][0]
            new_ub = sat[col][1]
            print(f'{col}使用原limit\n')
            log.write(f'{col} use old limit\n')
        return new_lb,new_ub
        
    
    
    
    func_dict = {
    'DVDD_current-DVDD': [get_static_func1,mean_max_func1],
    'VBAT_idle_current-VBAT_IO':[get_static_func1,mean_max_func1],
    'PVDD_idle_current-PVDD_IO': [get_static_func1,mean_max_func1],
    'PVDD_OV-PVDD_OV': [get_static_func1,mean_max_func1],
    'PVDD_OV_HYS-PVDD_OV_HYS': [get_static_func1,mean_max_func1],
    'PVDD_UV-PVDD_UV': [get_static_func1,mean_max_func1],
    'PVDD_UV_HYS-PVDD_UV_HYS': [get_static_func1,mean_max_func1],
    'VBAT_OV-VBAT_OV': [get_static_func1,mean_max_func1],
    'VBAT_OV_HYS-VBAT_OV_HYS': [get_static_func1,mean_max_func1],
    'VBAT_UV-VBAT_UV': [get_static_func1,mean_max_func1],
    'VBAT_UV_HYS-VBAT_UV_HYS': [get_static_func1,mean_max_func1],
    'AVDD_CHECK_AF-AVDD': [get_static_func1,mean_max_func1],
    'GVDD_CHECK_AF-A5VSVR': [get_static_func1,mean_max_func1],
    'VBG_AF-VBG_AF': [get_static_func1,mean_max_func1],
    'VDDCP_V_AF-VddCP': [get_static_func1,mean_max_func1],
    'LDO_V_AF-D1e8SVR': [get_static_func1,mean_max_func1],
    'DLDO_V_AF-DLDO': [get_static_func1,mean_max_func1],
    'PVDD_ISD-PVDD_IO': [get_static_func1,mean_max_func1],
	'rePVDD_ISD-PVDD_IO': [get_static_func1,mean_max_func1],
    'VBAT_ISD-VBAT_IO': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_1P': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_1M': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_2P': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_2M': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_3P': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_3M': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_4P': [get_static_func1,mean_max_func1],
    'Leakage_test_HSD-OUT_4M': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_1P': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_1M': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_2P': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_2M': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_3P': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_3M': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_4P': [get_static_func1,mean_max_func1],
    'Leakage_test_LSD-OUT_4M': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT1P-Rdson_test_LSD_OUT1P': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT2P-Rdson_test_LSD_OUT2P': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT3P-Rdson_test_LSD_OUT3P': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT4P-Rdson_test_LSD_OUT4P': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT1M-Rdson_test_LSD_OUT1M': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT2M-Rdson_test_LSD_OUT2M': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT3M-Rdson_test_LSD_OUT3M': [get_static_func1,mean_max_func1],
	'Rdson_test_LSD_OUT4M-Rdson_test_LSD_OUT4M': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT1P-Rdson_test_HSD_OUT1P': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT2P-Rdson_test_HSD_OUT2P': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT3P-Rdson_test_HSD_OUT3P': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT4P-Rdson_test_HSD_OUT4P': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT1M-Rdson_test_HSD_OUT1M': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT2M-Rdson_test_HSD_OUT2M': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT3M-Rdson_test_HSD_OUT3M': [get_static_func1,mean_max_func1],
	'Rdson_test_HSD_OUT4M-Rdson_test_HSD_OUT4M': [get_static_func1,mean_max_func1],
	'BG_4uA_AF-BG_4uA_AF': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-D1e8SVR': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-SCLK': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-VddCP': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_1P': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_1M': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_2P': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_2M': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_3P': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_3M': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_4P': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-OUT_4M': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-CPump1': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-CPump2': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-CD_Diag': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-ENABLE3': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-ENABLE2': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-ENABLE1': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-MUTE': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-SCL': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-SDA': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-SDIN1': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-SDIN2': [get_static_func1,mean_max_func1],
    'REIO_Pins_PPMU-FSYNC': [get_static_func1,mean_max_func1],
    'REDPS_POWER_L-PVDD': [get_static_func1,mean_max_func1],
    'REDPS_POWER_L-A5VSVR': [get_static_func1,mean_max_func1],
    'Res_test_BF-RES_OUT1P_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_OUT1M_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_OUT2P_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_OUT2M_BF': [get_static_func1,mean_max_func1],   
    'Res_test_BF-RES_OUT3P_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_OUT3M_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_OUT4P_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_OUT4M_BF': [get_static_func1,mean_max_func1], 

    'Res_test_BF-RES_SDA_BF': [get_static_func1,mean_max_func1],      
    'Res_test_BF-RES_SCL_BF': [get_static_func1,mean_max_func1],      
    'Res_test_BF-RES_SCLK_BF': [get_static_func1,mean_max_func1],     
    'Res_test_BF-RES_FSYNC_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_SDIN1_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_SDIN2_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_CPump1_BF': [get_static_func1,mean_max_func1],   
    'Res_test_BF-RES_CPump2_BF': [get_static_func1,mean_max_func1],   
    'Res_test_BF-RES_VDDCP_BF': [get_static_func1,mean_max_func1],    
    'Res_test_BF-RES_ENABLE1_BF': [get_static_func1,mean_max_func1],  
    'Res_test_BF-RES_ENABLE2_BF': [get_static_func1,mean_max_func1],  
    'Res_test_BF-RES_ENABLE3_BF': [get_static_func1,mean_max_func1],  
    'Res_test_BF-RES_MUTE_BF': [get_static_func1,mean_max_func1],	    
    'Res_test_BF-RES_CD_Diag_BF': [get_static_func1,mean_max_func1],  
    'Res_test_BF-RES_PVDD_IO_BF': [get_static_func1,mean_max_func1],  
    'Res_test_BF-RES_D1e8SVR_BF': [get_static_func1,mean_max_func1],  
    'Res_test_BF-RES_A5VSVR_BF': [get_static_func1,mean_max_func1],   
    'Res_test_AF-RES_OUT1P_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_OUT1M_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_OUT2P_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_OUT2M_AF': [get_static_func1,mean_max_func1], 
    'Res_test_AF-RES_OUT3P_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_OUT3M_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_OUT4P_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_OUT4M_AF': [get_static_func1,mean_max_func1], 
    'Res_test_AF-RES_SDA_AF': [get_static_func1,mean_max_func1],      
    'Res_test_AF-RES_SCL_AF': [get_static_func1,mean_max_func1],      
    'Res_test_AF-RES_SCLK_AF': [get_static_func1,mean_max_func1],     
    'Res_test_AF-RES_FSYNC_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_SDIN1_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_SDIN2_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_CPump1_AF': [get_static_func1,mean_max_func1],   
    'Res_test_AF-RES_CPump2_AF': [get_static_func1,mean_max_func1],   
    'Res_test_AF-RES_VDDCP_AF': [get_static_func1,mean_max_func1],    
    'Res_test_AF-RES_ENABLE1_AF': [get_static_func1,mean_max_func1],  
    'Res_test_AF-RES_ENABLE2_AF': [get_static_func1,mean_max_func1],  
    'Res_test_AF-RES_ENABLE3_AF': [get_static_func1,mean_max_func1],  
    'Res_test_AF-RES_MUTE_AF': [get_static_func1,mean_max_func1],	    
    'Res_test_AF-RES_CD_Diag_AF': [get_static_func1,mean_max_func1],  
    'Res_test_AF-RES_PVDD_IO_AF': [get_static_func1,mean_max_func1],  
    'Res_test_AF-RES_D1e8SVR_AF': [get_static_func1,mean_max_func1],  
    'Res_test_AF-RES_A5VSVR_AF': [get_static_func1,mean_max_func1],   
    'Res_test_DEL-RES_OUT1P_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT1M_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT2P_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT2M_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT3P_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT3M_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT4P_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_OUT4M_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_SDA_DEL': [get_static_func1,mean_max_func1],    
    'Res_test_DEL-RES_SCL_DEL': [get_static_func1,mean_max_func1],    
    'Res_test_DEL-RES_SCLK_DEL': [get_static_func1,mean_max_func1],   
    'Res_test_DEL-RES_FSYNC_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_SDIN1_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_SDIN2_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_CPump1_DEL': [get_static_func1,mean_max_func1], 
    'Res_test_DEL-RES_CPump2_DEL': [get_static_func1,mean_max_func1], 
    'Res_test_DEL-RES_VDDCP_DEL': [get_static_func1,mean_max_func1],  
    'Res_test_DEL-RES_ENABLE1_DEL': [get_static_func1,mean_max_func1],
    'Res_test_DEL-RES_ENABLE2_DEL': [get_static_func1,mean_max_func1],
    'Res_test_DEL-RES_ENABLE3_DEL': [get_static_func1,mean_max_func1],
    'Res_test_DEL-RES_MUTE_DEL': [get_static_func1,mean_max_func1],	  
    'Res_test_DEL-RES_CD_Diag_DEL': [get_static_func1,mean_max_func1],
    'Res_test_DEL-RES_PVDD_IO_DEL': [get_static_func1,mean_max_func1],
    'Res_test_DEL-RES_D1e8SVR_DEL': [get_static_func1,mean_max_func1],
    'Res_test_DEL-RES_A5VSVR_DEL': [get_static_func1,mean_max_func1] 

    
    }
    
    
    sat = {}
    
    def get_static_dict(file_name):
        # file_name = FT1_file
        data = pd.read_csv(file_name,skiprows=29,sep=',')
        # data = pd.read_csv(file_name,sep=',')
        # split_data = data.iloc[:,4:]
        split_data = data.iloc[:,:]
        columns_names = []
        columns_name_dict = {}
        for key in list(split_data.columns[4:]):
            if "Unnamed" in key:
                columns_names.append(key)
                continue
            keys = key.split('.')
            new_key = keys[0]
            if new_key == split_data[key].loc[0]:
                new_list_name =  new_key + '-' + split_data[key].loc[0]
            else:
                new_list_name = new_key + '-' + split_data[key].loc[0]
            if new_list_name in columns_name_dict.keys():
                columns_name_dict[new_list_name] += 1
                new_list_name += '.' + str(columns_name_dict[new_list_name]-1)
            else:
                columns_name_dict[new_list_name] = 1
            columns_names.append(new_list_name)
        split_data.columns = ['Serial','Site','Bin','SBin'] + columns_names
        static_df = split_data
        #static_df = split_data[split_npdata['SBin'] == '1']
    
        # print(static_df.columns)
        # static_df.to_excel("test.xlsx")
        # os._exit()
        static_dict = {}
    
        for col in list(static_df.columns):
            if col not in target_col_list:
                continue
            # if 'Unnamed' in col or 'OTP_' in col:
            #     continue
            unit = static_df[col].iloc[3]
            old_max = round(float(static_df[col].iloc[1]),2)
            old_min = round(float(static_df[col].iloc[2]),2)
            test_df = static_df[col].iloc[4:]
    
            # df = pd.to_numeric(, errors='coerce')
        
            # mean_val = df.mean(skipna=True)
            # std_val = df.std(skipna=True)
            # static_dict[col] = [mean_val,std_val,old_min,old_max,unit.replace(' ','')]
    
            data_list = static_df[col].iloc[4:].dropna().tolist()
            data_list = [float(i) for i in data_list]
    
            # if 'MUTE' in col or 'FAULT' in col:
            # print(col,data_list,np.mean(data_list),np.std(data_list),unit)
            mean0 = sum(data_list) / len(data_list)
            # print(mean0, data_list)
        
            new_data_list = []
            for tmp in data_list:
                if tmp <= old_max and tmp >= old_min:
                    new_data_list.append(tmp)
                else:
                    pass
            try:
                mean1 = sum(new_data_list) / len(new_data_list)
            except:
                log.write(f"{col}: Some of the data in the original dataset deviate significantly from the mean value.\n")
                print("%s error , data std is too large, no data valid"%(col))
                str1=f"{col}s error , data std is too large, no data valid\n"
                log.write(str1)
                mean1 = mean0
    
            static_list = [mean1,mean0]
            new_mean_val = np.mean(new_data_list)
            new_std_val = np.std(new_data_list)
            sat[col] = [old_min,old_max,unit.replace(' ','')]+ [new_mean_val,new_std_val]
            # print(mean1, new_data_list)
            # if 'MUTE' in col or 'FAULT' in col:
            #     print(col,np.mean(data_list),np.std(data_list))
            #     print(col,np.mean(new_data_list),np.std(new_data_list))
    
            static_dict[col] = [old_min,old_max,unit.replace(' ','')] + static_list
        # print(static_dict)
        # os._exit()
        return static_dict
    
    
    
    def extract_input_params(s):
        # 使用正则表达式查找括号内的内容
        import regex  
        # match = re.search(r'\((.*?)\)', s)
        match = regex.findall(r'\((?:[^()]*|(?R))*\)', s)
        # last = re.findall(r'\((.*?)\)', s)[-1]
        # print(match.group())
        if match:
            return match[-1][1:-1]
        else:
            return None  # 如果没有找到匹配的内容，返回 None
    def extract_name(s):
        # 使用正则表达式查找括号内的内容
        
        match = re.search(r'\"(.*?)\"', s)
        # print(s)
        # print(match.group(1))
        if match:
            return match.group(1)  # 返回括号内的内容
        else:
            return None  # 如果没有找到匹配的内容，返回 None
            
    def extract_loop_name(s):
        # 使用正则表达式查找括号内的内容
        match = re.search(r'\((.*?)\)', s)
    
        if match:
            return match.group(1)  # 返回括号内的内容
        else:
            return None  # 如果没有找到匹配的内容，返回 None
    
    
    def get_program_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 打印读取的行
        
        is_cp = []
        is_qa = []
        temp_define = []
        judge_data = []
        judge_index = []
        judge_types = ['JUDGE_V_MLDPS','JUDGE_VARIABLE_MS','JUDGE_VARIABLE','JUDGE_V_PPMU','JUDGE_I_PMU','JUDGE_V_PMU','JUDGE_I_MLDPS']
        
        for index,line in enumerate(lines):
            for judge_type in judge_types:
                if judge_type in line:
                    judge_data.append(line)
                    judge_index.append(index)
                    break
        
        
        normal_dict = {}
        name_cnt_dict = {}
        for index, judge_line in enumerate(judge_data):
            content = extract_input_params(judge_line)
            # print(judge_line,content)
            content = [i.strip() for i in content.split(',') ]# 输出：这是括号内的内容
            # print(content)
            if "JUDGE_I_PMU" in judge_line or "JUDGE_V_PMU" in judge_line:
                low_th = content[1]
                high_th = content[2]
                name = "pmu_setting"
                name2 = ''  
            elif "JUDGE_V_MLDPS" in judge_line  or "JUDGE_V_PPMU" in judge_line:
                low_th = content[-3]
                high_th = content[-2]
                name = content[-1]
                
                name2 = [ i.replace(' ','')   for i in content[0].split('+')] 
            elif "JUDGE_I_MLDPS" in judge_line :
                low_th = content[1]
                high_th = content[2]
                name = 'mS'
                name2 = [ i.replace(' ','')   for i in content[0].split('+')] 
            elif "JUDGE_VARIABLE_MS" in judge_line or "JUDGE_VARIABLE" in judge_line :
                
                low_th = content[-3]
                high_th = content[-2]
                name = 'uS'
                if 'log_msg' in content[-1]:
                    continue
                if extract_name(content[-1]) != None:
                    name2 = [extract_name(content[-1])]
                else:
                    print("invalid name",content[-1])
                    continue
            else:
                low_th = content[-3]
                high_th = content[-2]
                name = content[-1]
                name2 = [ i.replace(' ','')   for i in content[0].split('+')]   
    
    
            
            if 'mS' in name or 'uS' in name :
                ii = 1
                while(1):
                    name_line = lines[judge_index[index]-ii]
                    if "DATALOG_MSG" in name_line:
                        # print("!!!!!!!!!!!!!!!!!!!",name_line)
                        test_name = extract_name(name_line)  
                        # print("after name = ",name)
                        break
                    ii = ii + 1
    
                # print("!!!!!!!!!!!!!!!!!!!",name2)
                for single_name in name2:
                    if single_name == '' :
                        name = test_name
                    else:
                        name = test_name + '-' + single_name  # single_name + '-' + test_name 
                    if name in normal_dict.keys():
                        name_cnt_dict[name] += 1
                        name = name + '.' + str(name_cnt_dict[name]-1)
                        # print("same name1 ",name,judge_index[index])
                        normal_dict[name] = [low_th,high_th,judge_index[index]]
                    else:
                        name_cnt_dict[name] = 1
                        normal_dict[name] = [low_th,high_th,judge_index[index]]
            elif name == 'pmu_setting':
                ii = 1
                while(1):
                    name_line = lines[judge_index[index]-ii]
                    if "PARAL_INC" in name_line:
                        # test_name = extract_name(name_line) 
                        loop_name = extract_loop_name(name_line)
                        # print("after name = ",name)
                        break
                    ii = ii + 1
                ii = 1
                while(1):
                    name_line = lines[judge_index[index]-ii]
                    if "DATALOG_MSG" in name_line:
                        # print(test_name)
                        test_name = extract_name(name_line)  
                        # print("after name = ",name)
                        break
                    ii = ii + 1
    
                # if loop_name == "OUT_PINS":
                #     name2 = ['OUTN_IO','OUTP_IO']
                # else:
                #     name2 = ['PVDD_IO']
                if loop_name in pin_group_dict.keys():
                    name2 = pin_group_dict[loop_name]
                else:
                    if '+' in loop_name:
                        name2_list = loop_name.split('+')
                        name2 = [i.replace(' ','') for i in name2_list]
                    else:
                        name2 = [loop_name]
                
                print(test_name,name2,loop_name)
                for single_name in name2:
                    if single_name == '':
                        name = test_name
                    else:
                        name = test_name + '-' +  single_name 
                    if name in normal_dict.keys():
                        name_cnt_dict[name] += 1
                        name = name + '.' + str(name_cnt_dict[name]-1)
                        # print("same name1 ",name,judge_index[index])
                        normal_dict[name] = [low_th,high_th,judge_index[index]]
                    else:
                        name_cnt_dict[name] = 1
                        normal_dict[name] = [low_th,high_th,judge_index[index]]
            else:
                name = extract_name(name)
                if name == None:
                    print("invalid line = ",judge_line.strip())
                    str1=f"invalid line ={judge_line.strip()}\n"
                    log.write(str1)
                else:
                    # print(name,low_th,high_th)
                    if name in normal_dict.keys():
                        name_cnt_dict[name] += 1
                        name = name + '.' + str(name_cnt_dict[name]-1)
                        # print("same name2 ",name,judge_index[index])
                        normal_dict[name] = [low_th,high_th,judge_index[index]]
                    else:
                        name_cnt_dict[name] = 1
                        normal_dict[name] = [low_th,high_th,judge_index[index]]
        return normal_dict
    
    
    
    
    def get_old_line_data(origin_data):
        old_th_low = origin_data
        old_th_low = old_th_low.split(' ')
    
        old_data = []
        temp_mode = []
        data_unit = None
        for t in old_th_low:
            data,unit = extract_unit(t)
            if unit != None:
                old_data.append(data)
                data_unit = unit
            else:                
                if t in ['HT','LT','NT']:
                    temp_mode.append(t)
        return old_data,temp_mode,data_unit
    
    
    def extract_coefficients(s):
        # 使用正则表达式查找所有系数
        # pattern = r'([+-]?\d+\.\d+)([A-Za-z]+)'
        global total_mode_list
        s = s.replace(' ','')
        pattern = r'([+-]?\d+\.?\d*)([A-Za-z]*)\s*\*\s*([A-Za-z]+)'
        matches = re.findall(pattern, s)
        coefficients = {}
        for match in matches:
            value = match[0]
            unit = match[1]
            var = match[2]
            coefficients[var] = round(float(value),2)
    
        for mode in total_mode_list:
            if mode not in coefficients.keys():
                coefficients[mode] = 0
        return coefficients,unit
    
    def extract_unit(s):
        # 使用正则表达式查找单位
        match = re.search(r'([-+]?\d*\.?\d+)([A-Za-z]*)', s)
        if match:
            return {'HT':round(float(match.group(1)),2),'NT':round(float(match.group(1)),2),'LT':round(float(match.group(1)),2)},match.group(2)  # 返回单位部分
        else:
            return None,None  # 如果没有找到匹配的内容，返回 None
    
    def get_new_line(origin_data,new_data,data_keys):
        try:
            old_data,unit = extract_coefficients(origin_data)
        except:
            old_data,unit = extract_unit(origin_data)
    
        tmp_str = ""
        if len(new_data) == 1:
            data = new_data[0]
            if data == None:
                tmp_str += "%s%s"%(str(old_data['NT']),unit)
            else:
                tmp_str += "%s%s"%(str(data),unit)
        else:            
            for index,key in enumerate(data_keys):
                if new_data[index] == None:
                    data = float(old_data[key])   
                else:
                    data = new_data[index]
                if index == 0:
                    tmp_str += "%s%s * %s "%(str(data),unit,key)
                else:
                    if data >= 0:
                        tmp_str += "+ %s%s * %s "%(str(data),unit,key)
                    else:
                        tmp_str += "- %s%s * %s "%(str(abs(data)),unit,key)
        
    
        return tmp_str
    
    
    
    import sys
    
    
    os.chdir('D:/tpfolder')
    
    
    
    
    
    
    
    folder_list = []
    for filename in os.listdir('./'):
        # 获取文件的完整路径
        file_path = os.path.join('./', filename)
        if os.path.isdir(file_path):
            folder_list.append(file_path)
    
    if len(folder_list) > 1:
        messagebox.showinfo("ERROR", "存在多个程序文件夹，请检查目录")
        log.write("ERROR", "存在多个程序文件夹，请检查目录\n")
        os._exit()
    
    file_path_list = []
    for filename in os.listdir('./'):
        if filename.endswith('.csv'):
            file_path_list.append(filename)
    
    
    program_path = ''
    pln_test = ''
    for filename in os.listdir(folder_list[0]):
        if filename.endswith('.pln'):
            program_path = os.path.join(folder_list[0],filename)
            pln_test = filename
    
    
    output_program_path = program_path
    
    
    
    
    # print(program_path)
    # os._exit()
    
    if len(file_path_list) >= 2:
        print(file_path_list)
        messagebox.showinfo("ERROR", "文件夹中存在多个csv文件")
        log.write("ERROR", "文件夹中存在多个csv文件\n")
        os._exit()
    
    is_csv_valid = False
    rule = csv_name_rules[0];
    rule1 = csv_name_rules[1];
    if rule in file_path_list[0] and rule1 in file_path_list[0]:
        is_csv_valid = True
        
    rule = csv_name_rules1[0];
    rule1 = csv_name_rules1[1];
    if rule in file_path_list[0] and rule1 in file_path_list[0]:
        is_csv_valid = True


    if is_csv_valid == False:
        print("csv name is invalid")
        messagebox.showinfo("ERROR", "CSV名字不符合预设规范，请检查")
        log.write("ERROR", "CSV名字不符合预设规范，请检查\n")
        os._exit()
    source_path = file_path_list[0]
    destination_folder = r"D:\XLScript"
    
    # Get the filename and extension
    filename, file_extension = os.path.splitext(os.path.basename(source_path))
    
    # Create the new filename with the current time
    new_filename = f"PAT_{filename}_{current_time}{file_extension}"
    
    # Define the full destination path with the new filename
    destination_path = os.path.join(r'D:\XLScript', new_filename)
    
    # Copy the file
    shutil.copy(source_path, destination_path)
    print(f"copied to: {destination_path}")
        
    with open(file_path_list[0], 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        csv_pln_name = lines[5].strip()
        csv_pln_name = csv_pln_name.split('\\')[-1]
        if csv_pln_name != pln_test:
            messagebox.showinfo("ERROR", "CSV内pln名字和pln程序不符合\npln = %s  \ncsv = %s"%(pln_test,csv_pln_name))
            log.write(f"ERROR, CSV内pln名字和pln程序不符合\n")
            log.write(f'pln = {pln_test}\n')
            log.write(f'csv ={csv_pln_name}\n')
            os._exit()
        
        print("start working ")
        log.write("start working\n")
        log.write(f"The PLN of this revision is: {program_path}\n")
        log.write(f"The csv used this time is: {str(file_path_list[0])}\n")
        print(program_path)
        print(file_path_list)
        
        data_dict_list = []
        for filepath in file_path_list:
            data_dict_list.append(get_static_dict(filepath))
        #print(data_dict_list)
        
        print("\n\n ################ load chip data done ################# \n\n")
        log.write("\n\n ################ load chip data done ################# \n\n")
        program_dict = get_program_data(program_path)   
        print("\n\n ################ load program done ################# \n\n")
        log.write("\n\n ################ load program done ################# \n\n")
        
        
        change_dict = {}
        pln_data_match_check = False
        
        for target_col in target_col_list:
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!><>\n')
            # print(target_col)
            if target_col in program_dict.keys():
                new_data = [[],[],[]]
        
                for index, data_dict in enumerate(data_dict_list):
                    if target_col in data_dict.keys():
                        mode = mode_list[index]
                        low_th = program_dict[target_col][0]
                        try:
                            low_th_dict,unit = extract_coefficients(low_th)
                        except:
                            low_th_dict,unit = extract_unit(low_th)
                        high_th = program_dict[target_col][1]
                        try:
                            high_th_dict,unit = extract_coefficients(high_th)
                        except:
                            high_th_dict,unit = extract_unit(high_th)
                        
                        
                        print(low_th_dict[mode],data_dict[target_col][0],high_th_dict[mode],data_dict[target_col][1],unit,data_dict[target_col][2])
                        if low_th_dict[mode] == (data_dict[target_col][0]) and high_th_dict[mode] == (data_dict[target_col][1]) and unit == data_dict[target_col][2]:
                            print( data_dict[target_col])
                            print('\n')
                            static_list = data_dict[target_col][3:]
        
                            new_lb,new_ub = func_dict[target_col][1](static_list,target_col)
                            print(f'{target_col}上限{new_ub},下限{new_lb}')
        
        
                            new_data[0].append(new_lb)
                            new_data[1].append(new_ub)
                            new_data[2].append(mode)
                            print(new_data)
                        else:
                            # print(target_col,data_dict.keys())
                            # print(target_col in data_dict.keys())
                            pln_data_match_check = True
                            log.write(f"{target_col}The upper and lower limits and units in the PLN and CSV are not the same.\n")
                            print("col = %s fail, because UB & LB is not same. Program data: " % target_col,low_th_dict[mode],high_th_dict[mode],unit,"chip data: ",data_dict[target_col][0],data_dict[target_col][1],data_dict[target_col][2])   
                            str1=f"col = {target_col} fail, because UB & LB is not same. Program data: {low_th_dict[mode]},{high_th_dict[mode]},{unit},{data_dict[target_col][0]},chip data: {data_dict[target_col][1]},{data_dict[target_col][2]}\n"
                            log.write(str1)
                    else:  
                        pass
        
                for tmp_mode in total_mode_list:
                    if tmp_mode in new_data[2]:
                        pass
                    else:
                        new_data[0].append(None)
                        new_data[1].append(None)
                        new_data[2].append(tmp_mode)
                change_dict[target_col] = new_data
                print(f'#########{target_col},{change_dict[target_col]}')
                print("change finish ",target_col)
                str1=f"limit {target_col}Successfully found and did format unification in PLN，change finish={target_col}\n"
                log.write(str1)
                if 'Leakage_test_HSD' in target_col:
                    base_col = target_col
                    target_col = base_col.replace('Leakage_test_HSD','Final_Leakage_test_HSD')
                    try:
                        for index, data_dict in enumerate(data_dict_list):
                            if target_col in data_dict.keys():
                                mode = mode_list[index]
                                low_th = program_dict[target_col][0]
                                try:
                                    low_th_dict,unit = extract_coefficients(low_th)
                                except:
                                    low_th_dict,unit = extract_unit(low_th)
                                high_th = program_dict[target_col][1]
                                try:
                                    high_th_dict,unit = extract_coefficients(high_th)
                                except:
                                    high_th_dict,unit = extract_unit(high_th)
                                
                                
                                print(low_th_dict[mode],data_dict[target_col][0],high_th_dict[mode],data_dict[target_col][1],unit,data_dict[target_col][2])
                                if low_th_dict[mode] == (data_dict[target_col][0]) and high_th_dict[mode] == (data_dict[target_col][1]) and unit == data_dict[target_col][2]:
                                    static_list = data_dict[target_col][3:]
                                    new_ub,new_lb = func_dict[target_col][1](static_list,target_col)
                                    print(f'{target_col}上限{new_ub},下限{new_lb}')
        
        
                                    new_data[0].append(new_lb)
                                    new_data[1].append(new_ub)
                                    new_data[2].append(mode)
                                    print(new_data)
                                else:
                                    # print(target_col,data_dict.keys())
                                    # print(target_col in data_dict.keys())
                                    pln_data_match_check = True
                                    print("col = %s fail, because UB & LB is not same. Program data: " % target_col,low_th_dict[mode],high_th_dict[mode],unit,"chip data: ",data_dict[target_col][0],data_dict[target_col][1],data_dict[target_col][2])   
                            else:  
                                pass
        
                        for tmp_mode in total_mode_list:
                            if tmp_mode in new_data[2]:
                                pass
                            else:
                                new_data[0].append(None)
                                new_data[1].append(None)
                                new_data[2].append(tmp_mode)
                        change_dict[target_col] = new_data
                        print("change finish ",target_col)
                    except:
                        print("no col exist ",target_col)
        
                    target_col = base_col.replace('Leakage_test_HSD','RELeakage_test_HSD')
                    try:
                        for index, data_dict in enumerate(data_dict_list):
                            if target_col in data_dict.keys():
                                mode = mode_list[index]
                                low_th = program_dict[target_col][0]
                                try:
                                    low_th_dict,unit = extract_coefficients(low_th)
                                except:
                                    low_th_dict,unit = extract_unit(low_th)
                                high_th = program_dict[target_col][1]
                                try:
                                    high_th_dict,unit = extract_coefficients(high_th)
                                except:
                                    high_th_dict,unit = extract_unit(high_th)
                                
                                
                                print(low_th_dict[mode],data_dict[target_col][0],high_th_dict[mode],data_dict[target_col][1],unit,data_dict[target_col][2])
                                if low_th_dict[mode] == (data_dict[target_col][0]) and high_th_dict[mode] == (data_dict[target_col][1]) and unit == data_dict[target_col][2]:
                                    static_list = data_dict[target_col][3:]
                                    new_ub,new_lb = func_dict[target_col][1](static_list,target_col)
                                    print(f'{target_col}上限{new_ub},下限{new_lb}')
        
        
                                    new_data[0].append(new_lb)
                                    new_data[1].append(new_ub)
                                    new_data[2].append(mode)
                                    print(new_data)
                                else:
                                    # print(target_col,data_dict.keys())
                                    # print(target_col in data_dict.keys())
                                    pln_data_match_check = True
                                    print("col = %s fail, because UB & LB is not same. Program data: " % target_col,low_th_dict[mode],high_th_dict[mode],unit,"chip data: ",data_dict[target_col][0],data_dict[target_col][1],data_dict[target_col][2])   
                            else:  
                                pass
        
                        for tmp_mode in total_mode_list:
                            if tmp_mode in new_data[2]:
                                pass
                            else:
                                new_data[0].append(None)
                                new_data[1].append(None)
                                new_data[2].append(tmp_mode)
                        change_dict[target_col] = new_data
                        print("change finish ",target_col)
                    except:
                        print("no col exist ",target_col)

                if 'Leakage_test_LSD' in target_col:
                    base_col = target_col
                    target_col = base_col.replace('Leakage_test_LSD','Final_Leakage_test_LSD')
                    try:
                        for index, data_dict in enumerate(data_dict_list):
                            if target_col in data_dict.keys():
                                mode = mode_list[index]
                                low_th = program_dict[target_col][0]
                                try:
                                    low_th_dict,unit = extract_coefficients(low_th)
                                except:
                                    low_th_dict,unit = extract_unit(low_th)
                                high_th = program_dict[target_col][1]
                                try:
                                    high_th_dict,unit = extract_coefficients(high_th)
                                except:
                                    high_th_dict,unit = extract_unit(high_th)
                                
                                
                                print(low_th_dict[mode],data_dict[target_col][0],high_th_dict[mode],data_dict[target_col][1],unit,data_dict[target_col][2])
                                if low_th_dict[mode] == (data_dict[target_col][0]) and high_th_dict[mode] == (data_dict[target_col][1]) and unit == data_dict[target_col][2]:
                                    static_list = data_dict[target_col][3:]
                                    new_ub,new_lb = func_dict[target_col][1](static_list,target_col)
                                    print(f'{target_col}上限{new_ub},下限{new_lb}')
        
        
                                    new_data[0].append(new_lb)
                                    new_data[1].append(new_ub)
                                    new_data[2].append(mode)
                                    print(new_data)
                                else:
                                    # print(target_col,data_dict.keys())
                                    # print(target_col in data_dict.keys())
                                    pln_data_match_check = True
                                    print("col = %s fail, because UB & LB is not same. Program data: " % target_col,low_th_dict[mode],high_th_dict[mode],unit,"chip data: ",data_dict[target_col][0],data_dict[target_col][1],data_dict[target_col][2])   
                            else:  
                                pass
        
                        for tmp_mode in total_mode_list:
                            if tmp_mode in new_data[2]:
                                pass
                            else:
                                new_data[0].append(None)
                                new_data[1].append(None)
                                new_data[2].append(tmp_mode)
                        change_dict[target_col] = new_data
                        print("change finish ",target_col)
                    except:
                        print("no col exist ",target_col)
        
                    target_col = base_col.replace('Leakage_test_LSD','RELeakage_test_LSD')
                    try:
                        for index, data_dict in enumerate(data_dict_list):
                            if target_col in data_dict.keys():
                                mode = mode_list[index]
                                low_th = program_dict[target_col][0]
                                try:
                                    low_th_dict,unit = extract_coefficients(low_th)
                                except:
                                    low_th_dict,unit = extract_unit(low_th)
                                high_th = program_dict[target_col][1]
                                try:
                                    high_th_dict,unit = extract_coefficients(high_th)
                                except:
                                    high_th_dict,unit = extract_unit(high_th)
                                
                                
                                print(low_th_dict[mode],data_dict[target_col][0],high_th_dict[mode],data_dict[target_col][1],unit,data_dict[target_col][2])
                                if low_th_dict[mode] == (data_dict[target_col][0]) and high_th_dict[mode] == (data_dict[target_col][1]) and unit == data_dict[target_col][2]:
                                    static_list = data_dict[target_col][3:]
                                    new_ub,new_lb = func_dict[target_col][1](static_list,target_col)
                                    print(f'{target_col}上限{new_ub},下限{new_lb}')
        
        
                                    new_data[0].append(new_lb)
                                    new_data[1].append(new_ub)
                                    new_data[2].append(mode)
                                    print(new_data)
                                else:
                                    # print(target_col,data_dict.keys())
                                    # print(target_col in data_dict.keys())
                                    pln_data_match_check = True
                                    print("col = %s fail, because UB & LB is not same. Program data: " % target_col,low_th_dict[mode],high_th_dict[mode],unit,"chip data: ",data_dict[target_col][0],data_dict[target_col][1],data_dict[target_col][2])   
                            else:  
                                pass
        
                        for tmp_mode in total_mode_list:
                            if tmp_mode in new_data[2]:
                                pass
                            else:
                                new_data[0].append(None)
                                new_data[1].append(None)
                                new_data[2].append(tmp_mode)
                        change_dict[target_col] = new_data
                        print("change finish ",target_col)
                    except:
                        print("no col exist ",target_col)     
        
            else:
                print("program not contain ",target_col)
                str1=f"program not contain ={target_col}\n"
                log.write(str1)
        if pln_data_match_check:
            messagebox.showinfo("ERROR", "PLN内上下阈值与CSV内上下阈值或者单位不同，请检查数据")
            log.write("ERROR", "PLN内上下阈值与CSV内上下阈值或者单位不同，请检查数据\n")
            os._exit()
        
        
        print("\n\n ################ new data generation done ################# \n\n")
        log.write("\n\n ################ new data generation done ################# \n\n")
        # print(data_dict_list[0].keys())
        # print('IO_NTest-INN_N' in change_dict.keys())
        
        with open(program_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        
        with open(program_path, 'r', encoding='utf-8') as file:
            lines2 = file.readlines()


        
        tmp_line_change = {}
        for key in change_dict.keys():
            
            
            origin_data = program_dict[key]
            thd_low = get_new_line(origin_data[0],change_dict[key][0],change_dict[key][2])
            thd_high = get_new_line(origin_data[1],change_dict[key][1],change_dict[key][2])
            line_index = origin_data[2]
            print("key = ",key)
            str1=f'key = {key}\n'
            log.write(str1)
            # print("old: %-40s , new: %-40s   mean = %f mean1 = %f"%(origin_data[0],thd_low,data_dict_list[0][key][0],data_dict_list[0][key][1]))
            # print("old: %-40s , new: %-40s"%(origin_data[1],thd_high))
            print("edit line = ",line_index)
            print("\n")
            old_line = lines[line_index]
            print("old line: \n",old_line)
            str1=f"old line: \n{old_line}\n"
            log.write(str1)
            old_line_split = old_line.split(',')
            if 'JUDGE_VARIABLE' in old_line and 'JUDGE_VARIABLE_MS' not in old_line:
                old_line_split[2] = thd_low
                old_line_split[3] = thd_high
            elif 'JUDGE_VARIABLE_MS' in old_line:
                old_line_split[1] = thd_low
                old_line_split[2] = thd_high
            else:
                old_line_split[1] = thd_low
                old_line_split[2] = thd_high
            old_line = ','.join(old_line_split)
            tmp_line_change[line_index] = old_line


          
  

        

            
            
            # lines[line_index] = old_line
            print("new line: \n",old_line)
            str1=f"new line: \n{old_line}\n"
            log.write(str1)
        
            print("\n\n")
        for key in tmp_line_change.keys():
            lines[key] = tmp_line_change[key]

        
        with open(output_program_path, 'w', encoding='utf-8') as file:
            for item in lines:
                file.write(f"{item}") 
        with open(output_program_path.replace('.pln','_old.txt'), 'w', encoding='utf-8') as file:
            for item in lines2:
                file.write(f"{item}") 
        
        
        # return 
        ######### chroma auto-compile####################
        bianyi_log=''
        path1=output_program_path
        path2 = 'D:/tpfolder'
        # 使用 os.path.join 组合路径
        path3 = os.path.join(path2, os.path.basename(os.path.dirname(path1)))
        path4 = os.path.join(path3, os.path.basename(path1))
        path5= fr"D:\XLScript\\{os.path.basename(path1)}"
        path6=path5.replace('.pln',f'{current_time}_PAT.pln')
        path7=path6.replace('.pln','_old.txt')
        # 打印结果
        print("path3:", path3)
        print("path4:", path4)
        with open(path6, 'w', encoding='utf-8') as file:
            for item in lines:
                file.write(f"{item}") 
        with open(path7, 'w', encoding='utf-8') as file:
            for item in lines2:
                file.write(f"{item}") 
        os.chdir(path3)
        bianyi = os.popen('plncmp.exe '+path4)
        bianyi_log=str(bianyi.read())
        print(bianyi.read())
        print(bianyi_log)
        if 'Pln File compile successful .....' in str(bianyi_log):
            print(f'{path4}compile successful.')
            str1=f'{path4}compile successful.\n'
            log.write(str1)
        else:
            print(f'{path4} compile not successful')
            messagebox.showinfo("ERROR", f'The {path4} file was not successfully compiled.') 
            str1="ERROR", f'The {path4} file was not successfully compiled.\n'
            log.write(str1)
        
        
    # In[ ]:
        
# 保持终端窗口打开
os.system('pause')

    
    




# In[ ]:






# In[ ]:






# In[ ]:




