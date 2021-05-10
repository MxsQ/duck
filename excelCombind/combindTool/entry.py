#coding=utf-8 
import numpy as np
import pandas as pd
import utils.fileUtils as fus
import utils.format as fm
import json


def getColumnNames(datas):
    colunms = []
    for d in datas:
       colunms.append(d.columns.values)

    return colunms

# 列表栏别名
def getColumnNickNameMap(nickNameJson):
    nickNames = {}
    matchList = nickNameJson['renameColumn'][0]
    for key in matchList:
        curMap = {}
        # print(key)
        for rule in matchList[key]:
            match = rule.split(':')
            curMap[match[1]] = match[0]
        nickNames[key] = curMap
    
    return nickNames     


# 移除无效字符
def removeInvalidSpan(tables):
    index = 0
    newTable = []
    while index < len(tables):
        t = tables[index]
        t = fm.removeUnuseCharaters(t)
        newTable.append(t)
        index = index + 1
    return t


if __name__ == '__main__':
    # 所有合并规则文件
    ruleFiles = fus.getWorkFiles()
    print("所有合并规则文件：")
    print(ruleFiles)

    for filePath in ruleFiles:
        configJson = fus.getRulesJson(filePath)
        # 所有表
        tables = fus.getExcel(configJson['excel'])

        # # 排序
        sorts = configJson['sorts'].split(":")
        tables = fm.sortsby(tables, sorts)

        # 合并范围
        bonds = configJson['bonds']
        tables = fm. filterByBindCondition(tables, sorts, bonds)

        # 所有标题栏名
        allColumnNames = getColumnNames(tables)
        # 所有标题别名
        allNickNames = getColumnNickNameMap(configJson)
        # sort的标题栏名
        allSortKeys = fm.fullSortRuleKeys(configJson['sorts'])
        # 所有表名
        tableNames = []
        for name in allNickNames:
            tableNames.append(name)

        # 移除表格中的无效字符
        removeInvalidSpan(tables)
        # 筛选条件
        fm.filterByFunction(tables, configJson['combindByRule'], configJson['filter'])

        # fm.getDataByBond(tables, allSortKeys, 0)

        

        # print(allNickNames)

        