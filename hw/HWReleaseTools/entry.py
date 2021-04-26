#coding=utf-8 
import numpy as np
import pandas as pd
import utils.fileUtils as fileUtils
import utils.dataFrameFormatUtils as dfUtils




if __name__ == '__main__':

    contryNameDirt = fileUtils.getContryNameTransferDirt()
    contriesCondition = fileUtils.getContryConditionForFilt()
    contriesConditionInEn = fileUtils.getContryConditionEnForFit(contriesCondition, contryNameDirt)
    accountExt = fileUtils.getAccountExt()
    converExt = fileUtils.getConverExt()

    # 账户报表
    accountFilePath = fileUtils.getDataFilePathByName('accountStatements.' + accountExt)
    print('get accountStatements fils from' + accountFilePath)
    if accountExt == 'xlsx':
        accountData = pd.read_excel(accountFilePath)
    else:
        accountData = pd.read_csv(accountFilePath, encoding='gbk')
    print(accountData)
    accountData = accountData[accountData['国家/地区'].isin(contriesCondition)]
    dfUtils.removeUnuseCharaters(accountData)
    dfUtils.formatDate(accountData, "时间")
    
    dateCondition = accountData['时间'].drop_duplicates()
    dateCondition = dateCondition.sort_values(ascending=False)
    dateCondition = dateCondition[0:1]
    accountData = accountData[accountData['时间'].isin(dateCondition)]
    # #accountData = accountData.sort_values(axis=0, ascending=False, by=['时间'])

    print(accountData[0:])
    print()

    # 数据报表
    conversionFilePath = fileUtils.getDataFilePathByName('conversionStatements.' + converExt)
    print('get conversionStatements fils from' + conversionFilePath)
    if converExt == 'xlsx':
        conversionData = pd.read_excel(conversionFilePath)
    else:
        conversionData = pd.read_csv(conversionFilePath, encoding='gbk')
    dfUtils.removeUnuseCharaters(conversionData)
    dfUtils.formatDate(conversionData, 'Date')
    conversionData = conversionData[conversionData['Date'].isin(dateCondition)]
    conversionData = conversionData[conversionData['Country/Region'].isin(contriesConditionInEn)]

    print(conversionData[0:])

    # putSeries = []
    putDatas = []
    # 投放数据表索引
    putDataIndex = ['日期', '国家', '花费', '下载数', 'CPD(下载)', '展示量',
    'CPM', '点击量', 'CPC', '点击率', '激活（华为统计)', '下载激活转化率（总计自然）',
    '收益', 'ROI', '变现展示量', 'ECPM', '活跃用户', '人均观看次数', '填充率', '广告请求次数', '展示率']
    regionList = accountData['国家/地区'].drop_duplicates()
    for region in regionList:
        aForm = accountData.loc[accountData['国家/地区'] == region]
        cForm = conversionData.loc[conversionData['Country/Region'] == contryNameDirt[region]]

        cost = aForm['花费'].values[0]
        tRevenue = cForm['Estimated total revenue (USD)'].values[0]
        roi = round(tRevenue / cost * 100, 2)

        # print(aForm['点击率'].values[0])

        outputData = [
            aForm['时间'].values[0], # 日期
            region,  # 国家
            '$' + str(cost), # 花费
            aForm['下载量'].values[0], # 下载数
            '$' + str(aForm['下载成本'].values[0]),# CPD(下载)
            aForm['曝光量'].values[0], # 展示量 
            '$' + str(aForm['千次展示均价'].values[0]), # CPM 
            aForm['点击量'].values[0], # 点击量 
            aForm['点击均价'].values[0],# CPC 
            str(aForm['点击率'].values[0]), # 点击率
            aForm['激活量（HMS）'].values[0],# 激活
            'null', # 自然转化率
            '$' + str(tRevenue), # 收益
            str(roi) + '%', # ROI
            cForm['Impressions'].values[0], # 变现展示量
            '$' + str(cForm['RPM (USD)'].values[0]),# ECPM
            'null', # 活跃用户
            'null',# 人均观看次数
            cForm['Fill rate%'].values[0],# 填充率
            cForm['Ad requests'].values[0],# 广告请求次数
            cForm['Impression rate%'].values[0]# 展示率
        ]
        # curSeries = pd.Series(data=outputData, index=putDataIndex)
        putDatas.append(outputData)
        # putSeries.append(curSeries)

    putDataFrame = pd.DataFrame(putDatas, columns=putDataIndex)
    print(putDataFrame)
    fileUtils.outExcel(putDataFrame, '新投放数据.xlsx')

