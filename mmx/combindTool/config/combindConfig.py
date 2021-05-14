import utils.fileUtils as fus
import utils.format as fm
from config.filter import ConfigFilter as Filter
from utils.stack import Stack
from utils.caculator import Caculator

class CombindConfig():

    # 过滤条件
    def createFilter(self, filters):
        print()
        for filt in filters:
            curFilter = Filter(filt)
            self.filters.append(curFilter)
            print("创建过滤条件：")
            for attr in curFilter.__dict__.items():
                print(attr)
            # print(curFilter.__dict__.items())
            print()


    # 输出的表标题
    def getNewTableCloumnList(self):
        columnList = list(self.outTableCuloumn.keys())
        return columnList

   
    # 输出的单元格是算式，转换
    def transferFormula(self):
        for key in self.outTableCuloumn:
            slot = self.outTableCuloumn[key].split(":")
            if len(slot) > 2:
            # 说明是算式
                self.formulaDirt[key] = self.caculator.media2pre(self.caculator.transfroFormula(slot[1]))
                self.columnSymbloDirt[key] = slot[0]


    # 重命名的column
    def getRenameDict(self, jsonObject):
        originMap = jsonObject["renameColumn"][0]
        targerMap = {}
        for key in originMap:
            itemDirt = {}
            for rule in originMap[key]:
                slot = rule.split(":")
                itemDirt[slot[1]] = slot[0]
            targerMap[key] = itemDirt
        return targerMap

    # 获取真正的column名，因为可能被重命名过
    def unmaskColounmName(self, conlumnName):
        if len(self.renameDirt) == 0:
            return conlumnName
        for key in self.renameDirt:
            if conlumnName in self.renameDirt[key]:
                return self.renameDirt[key][conlumnName]
        return conlumnName

    # 过滤
    def filt(self, dataFrame, tableIndex):
        frame = dataFrame
        count = 0
        for filter in self.filters:
            print("第" + str(count) + "次过滤: ")
            frame = filter.filt(frame, tableIndex)
            count = count + 1
            print(frame)

        return frame

    # 是否通过算式得到
    def byFormula(self, outColumnName):
        return outColumnName in self.formulaDirt

    # 从公式拿到数据
    def getFormulaResult(self, headerRow, nextRow, outCoulnName, tableColumnNameDir):
        if outCoulnName in self.formulaDirt is False:
            return "null"
        formulaRule = self.formulaDirt[outCoulnName]
        # 替换其中的值
        index = 0
        size = len(formulaRule)
        factors = []
        while index < size:
            f = formulaRule[index]
            if self.caculator.isFormulaSamble(f):
            # 运算符的处理
                factors.append(f)

            elif self.caculator.isConstanNumber(f) is False:
                ## 替换不是数字常量的值
                realColumnName = self.unmaskColounmName(f)
                targerRow = headerRow
                if tableColumnNameDir[self.excelName[0]].__contains__(realColumnName) is False:
                    targerRow = nextRow
                # print("column name",realColumnName)
                # print('header row', tableColumnNameDir[self.excelName[0]])
                
                factors.append(targerRow[realColumnName])
            else:
                factors.append(f)
            index = index + 1
        
        return self.columnSymbloDirt[outCoulnName] + str(self.caculator.workByPre(factors))  
                

    def __init__(self, configFile):
        # excel名
        self.excelName = []
        # excel全名
        self.excelFullName = []
        # 过滤条件
        self.filters = []

        jsonObject = fus.getRulesJson(configFile)
        
        excelName = jsonObject['excel']
        # 所有表名
        self.excelFullName = excelName
        self.excelName = list(map(lambda fileName: fileName.split('.')[0], excelName))
        print("excel名: ")
        print(excelName)
        
        # 输出的表名
        self.outputTableName = jsonObject['newExcelName']
        self.createFilter(jsonObject['filter'])
        
        # 输出的表名和公式
        self.outTableCuloumn = jsonObject['realColumn'][0]
        # 重命名的标题
        self.renameDirt = self.getRenameDict(jsonObject)
        print("重命名信息:")
        print(self.renameDirt)
        print()
        # 新表中哪些栏来自于计算
        self.formulaDirt = {}
        # 新表的单元格的符号，如果来自于公式的话
        self.columnSymbloDirt = {}
        # 处理运算的辅助器
        self.caculator = Caculator()
        # 记录新表中哪些栏来源于计算
        self.caculateFormatDict = {}
        self.transferFormula()
        print("算式:")
        print(self.formulaDirt)
        print()
