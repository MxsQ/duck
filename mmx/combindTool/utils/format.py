import utils.fileUtils as fileUtils
import pandas as pd

# 移除无效的字符
def removeUnuseCharaters(dataFrame):
    def pressCharater(word):
        if isinstance(word, str):
            return word.strip()
        else:
            return word

    column = dataFrame.columns
    for columnName in column:
        dataFrame[columnName] = dataFrame[columnName].map(lambda s: pressCharater(s))
    return dataFrame


# 所有排序的key
def fullSortRuleKeys(sortsRuls):
    rules = sortsRuls.split(':')
    keys = []
    index = 0
    leftIndex = 0

    while index < len(rules):
        if rules[index] == '':
            index = index + 1
            continue

        key = rules[index].split(',')[0]
        i = leftIndex
        while i <= leftIndex:
            keys.append(key)
            i = i + 1
        
        index = index + 1
    
    return keys


# 排序
def sortsby(data, sortsRuls):
    index = 0
    leftIndex = 0
    transferData = []
    dataLen = len(data)

    while index < len(sortsRuls):
        if sortsRuls[index] == '':
            index = index + 1
            if index <= dataLen - 1:
                continue
        curRuls = sortsRuls[index].split(",")
        column = curRuls[0]
        if curRuls[1] == 'down':
            sor = False
        else:
            sor = True

        i = leftIndex
        while i <= index:
            frame = data[i].sort_values(axis=0, ascending=sor, by=[column])
            transferData.append(frame)
            i=i+1
    
        index = index + 1
        leftIndex = index

    return transferData

# 筛选-合并条件
# @bonds 不同的数据范围
def filterByBindCondition(datas, sortsRuls, bonds):
    index = 0
    leftIndex = 0
    transferData = []
    dataLen = len(datas)

    while index < len(sortsRuls):
        if sortsRuls[index] == '':
            index = index + 1
            if index <= dataLen - 1:
                continue
        curRuls = sortsRuls[index].split(",")
        column = curRuls[0]

        i = leftIndex
        while i <= index:
            condition = datas[index][column].unique()[0:bonds]
            frame = datas[i]
            frame = frame[frame[column].isin(condition)]
            transferData.append(frame)
            i = i + 1
    
        index = index + 1
        leftIndex = index
    
    return transferData


# 获取筛选范围内的dataFrame
def getDataByBond(datas, sortsRuls, dividingLine):
    dataLen = len(datas)
    transferData = []
    index = 0
    while index < dataLen:
        frame = datas[index]
        condition = frame[sortsRuls[index]].unique()[dividingLine: dividingLine + 1]
        frame = frame[frame[sortsRuls[index]].isin(condition)]
        index = index + 1
        print(frame)
        # frame(frame[sortsRuls[index]].isin)

# 筛选条件
def filterByFunction(datas, combindRule, filterRule):
    if len(filterRule) == 0:
        return datas
    funKey = ""
    ruleValues = []
    for key in filterRule[0]:
        funKey = key
        ruleValues = filterRule[0][key]

    def theFilter(rule, ruleMatch):
        for r in ruleMatch:
            if rule.__contains__(r):
                return True
        return False
    
    realConbindRuld = list(filter(lambda rule: theFilter(rule, ruleValues), combindRule))
    
    if len(realConbindRuld) == 0:
        return datas
    
    
    def fullRull(rule):
        curPosition = 0
        lefPosition = 0
        stubs = rule.split(":")
        fr = ""
        while curPosition < len(stubs):
            if stubs[curPosition] == "":
                curPosition = curPosition + 1
                continue
            while lefPosition <= curPosition:
                fr = fr + stubs[curPosition] + ":"
                lefPosition = lefPosition + 1
            curPosition = curPosition + 1

        fr = fr[0: len(fr) - 1]
        return fr
    
    realConbindRuld = list(map(lambda rule: fullRull(rule), realConbindRuld))
   

   
    print(realConbindRuld)
    
    # changeLen = len(changePosition)
    # index = 0
    # leftIndex = 0
    # newTables = []
    # invalideRow = []


    