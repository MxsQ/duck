import pandas as pd

class ConfigFilter():
    FUNC_INCLUDE = 'include'
    FUNC_MAX = 'head'
    FUNC_EXCLUDE = 'exclude'
    FUNC_MORE_THAN = 'moreThan'
    FUNC_LESS_THAN = 'lessThan'

    TABLE_HEADER = 0
    TABLE_STUB = 1

    def fullBindDirt(self, origin, product):
        index = 0
        # 不用考虑边间不一致的情况，上层自己做保证
        size = len(origin)
        while (index < size):
            self.bindDirt[origin[index]] = product[index]
            index = index + 1
        

    # 获取要做映射的条件
    def getReflctCondition(self, colummIndex):
        if colummIndex == self.TABLE_HEADER:
            return self.extra

        condition = []

        if len(self.reflect) == 0:
        ## 说明不需要映射
            self.fullBindDirt(self.extra, self.extra)
            return self.extra

        for key in self.extra:
            cond = self.reflect[key]
            condition.append(cond)
        self.fullBindDirt(self.extra, condition)
        return condition


    # 过滤包含
    def include(self, dataFrame, colummIndex):
        columnName = self.column[colummIndex]
        condition = self.getReflctCondition(colummIndex)
        return dataFrame[dataFrame[self.column[colummIndex]].isin(condition)]

    # 排他
    def exclude(self, dataFrame, colummIndex):
        columnName = self.column[colummIndex]
        condition = self.extra
        return dataFrame[~dataFrame[self.column[colummIndex]].isin(condition)]
    
    # 大于
    def moreThan(self, dataFrame, colummIndex):
        columnName = self.column[colummIndex] 
        condition = self.extra[0]
        return dataFrame[dataFrame[self.column[colummIndex]].astype(float) > float(condition)]

     # 小于
    def lessThan(self, dataFrame, colummIndex):
        columnName = self.column[colummIndex] 
        condition = self.extra[0]
        return dataFrame[dataFrame[self.column[colummIndex]].astype(float) < float(condition)]


    # 头部    
    def head(self, dataFrame, colummIndex):
        columName = self.column[colummIndex]
        frame = dataFrame.sort_values(by=columName, ascending=self.assending)

        if colummIndex == self.TABLE_HEADER:
            condition = frame[columName].unique()
            condition = condition[0: self.extra[0]]

            if len(self.ignoreChatWhenFilt) > 0:
                # 为下个表准备过滤条件
                for itemCondition in condition:
                    transferChar = itemCondition
                    for ignore in self.ignoreChatWhenFilt:
                        transferChar = transferChar.replace(ignore, "")
                    self.preCondition.append(transferChar)
                self.fullBindDirt(condition, self.preCondition)
            
            else:
                self.preCondition = condition
                self.fullBindDirt(condition, self.preCondition)

            frame = frame[frame[columName].isin(condition)]
           

        else:
            print("过滤条件")
            print(self.preCondition)
            frame[columName] = frame[columName].map(lambda word: str(word))
            frame = frame[frame[columName].isin(self.preCondition)]

        return frame

    # 过滤dataFrame
    def filt(self, dataFrame, colummIndex):
        if colummIndex != self.TABLE_HEADER:
            if self.workByHeanderTable :
                return dataFrame

        theFunction = self.filterFunctionMap[self.func]
        print("执行过滤方法 ", self.func, "只作用于第一张表=",self.workByHeanderTable, colummIndex)
        curDataframe = theFunction(dataFrame, colummIndex)
        return curDataframe

        # if self.func == self.FUNC_INCLUDE:
            # return self.include(dataFrame, colummIndex)


    def fullProperty(self, desc):
        if self.func == self.FUNC_INCLUDE:
            self.extra = desc['extra']
            for refl in desc['reflect']:
                kv = refl.split(':')
                self.reflect[kv[0]] = kv[1]
        
        elif self.func == self.FUNC_MAX:
            self.ignoreChatWhenFilt = desc['ignoreChatWhenFilt']
            self.extra = desc['extra']
            self.assending = desc['assending']
        
        elif self.func == self.FUNC_EXCLUDE:
            self.extra = desc['extra']

        elif self.func == self.FUNC_MORE_THAN:
            self.extra = desc['extra']

        elif self.func == self.FUNC_LESS_THAN:
            self.extra = desc['extra']


    # 获取 header table 在下一table找到的行
    def getBinderRow(self, headerRow, bindDataFrame):
        if self.workByHeanderTable:
        # 当前规则值作用于头表，因此找bind，从上一个bind结果找就好
            return bindDataFrame

        condition = []
        equalValue = headerRow[self.column[self.TABLE_HEADER]]
        columnName = self.column[self.TABLE_STUB]
        
        if equalValue in self.bindDirt :
            equalValue = self.bindDirt[equalValue]
        
        condition.append(equalValue)
        bindDataFrame = bindDataFrame[bindDataFrame[columnName].isin(condition)]
        
        return bindDataFrame

    def __init__(self, desc):  
    
        # 方法映射
        self.filterFunctionMap = {}
         # 标题栏
        self.column = []
        # 额外参数
        self.extra = []
        # 来自于前一张表的过滤条件
        self.preCondition = []
        # 合并时，做转换映射用的map
        self.bindDirt = {}
        
        # 映射关系
        self.reflect = {}
        # 过滤时忽略的字符
        self.ignoreChatWhenFilt = []

        # 只作用于头部列表的参数
        self.workByHeanderTable = False
        self.column = desc['column'].split(':')
        if len(self.column) == 1:
            print("<----->")
            self.workByHeanderTable = True
         # 方法名
        self.func = desc['func']
        self.fullProperty(desc)
        self.filterFunctionMap[self.FUNC_INCLUDE] = self.include
        self.filterFunctionMap[self.FUNC_MAX] = self.head
        self.filterFunctionMap[self.FUNC_EXCLUDE] = self.exclude
        self.filterFunctionMap[self.FUNC_MORE_THAN] = self.moreThan
        self.filterFunctionMap[self.FUNC_LESS_THAN] = self.lessThan
        
