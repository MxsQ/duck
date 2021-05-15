import numpy as np
import pandas as pd
import utils.fileUtils as fus
import utils.format as fm
from config.combindConfig import CombindConfig as Config
import datetime
import traceback
import os
import sys

# 确定table位置
def inTable(targetColumn, columnDirt):
    tableIndex = 0
    for key in columnDirt:
        for column in columnDirt[key]:
            if (column == targetColumn):
                return tableIndex
        tableIndex = tableIndex + 1
    return -1


# 所有标题栏
def tableColumnsMap(tableNames, tables):
    columnNameDict = {}
    index = 0
    while index < len(tables):
        columnNameDict[tableNames[index]] = tables[index].columns.values.tolist()
        index = index + 1
    return columnNameDict

# 输出print到指定文件
def tryWritePrintToFile():
    json = fus.getIndexFileJson()
    isWriteToFile = json['debug']
    if isWriteToFile:
        outputFile = fus.getWorkDirPath() + fus.sperator() + "runtime" + fus.sperator() + "error.txt"
        if os.path.exists(outputFile):
            os.remove(outputFile)
        class Logger(object):
            def __init__(self, filename="info.log"):
                self.terminal = sys.stdout
                self.log = open(filename, "a")

            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)

            def flush(self):
                pass
        path = os.path.abspath(os.path.dirname(__file__))
        type = sys.getfilesystemencoding()
        sys.stdout = Logger(outputFile)
        


def work():
    ruleFiles = fus.getWorkFiles()
    print("所有合并规则文件：")

    for filePath in ruleFiles:
        config = Config(filePath)
        tables = fus.getExcel(config.excelFullName)
        tables = list(map(lambda t: fm.removeUnuseCharaters(t), tables))
        columnNameDict = tableColumnsMap(config.excelName, tables)
        newTableColunmIndex = config.getNewTableCloumnList()
        print(newTableColunmIndex)
        print(columnNameDict)

        tableIndex = 0
        # 做过滤

        while tableIndex < len(tables):
            print("---------> 过滤第" + str(tableIndex) + "表：")
            curTable = config.filt(tables[tableIndex], tableIndex)
            tables[tableIndex] = curTable
            tableIndex = tableIndex + 1
            print()
            print()

        # 表都过滤完了，开始找到对应的列
        outTableSize = len(tables[0])
        curTableIndex = 0
        realColumnFromIndex = 1

        print("开始合并")
        outData = []
        for index, headerRow in tables[0].iterrows():
            curData = []
            # 找到对应的row
            bindRow = tables[1]
            for filt in config.filters:
                bindRow = filt.getBinderRow(headerRow, bindRow)
            if (len(bindRow) < 0):
                continue
        
            for j, r in bindRow.iterrows():
            ## 没关系，这里只有一个长度
                bindRow = r

            ## 开始合并
            for key in config.outTableCuloumn:
                formColunmName = ''
                if ':' in config.outTableCuloumn[key]:
                    formColunmName = config.outTableCuloumn[key].split(":")[realColumnFromIndex]
                else:
                    formColunmName = config.outTableCuloumn[key]

                if config.byFormula(key) is False:
                    # print("??????")
                    # 如果不需要通过算式能得到
                    targetColumnName = config.unmaskColounmName(formColunmName)
                    targetRowIndex = inTable(targetColumnName, columnNameDict)
                    targerRow = headerRow
                    if targetRowIndex == 0:
                        targerRow = headerRow
                    elif targetRowIndex == 1:
                        targerRow = bindRow
                    curData.append(targerRow[targetColumnName])
                else:
                    # 从算式中得到
                    formulaResult = config.getFormulaResult(headerRow, bindRow, key, columnNameDict)
                    curData.append(formulaResult)
                    pass
            print("第", index, "数据", curData)
            outData.append(curData)

        putDataFrame = pd.DataFrame(outData, columns=newTableColunmIndex)
        print()
        print("✈️✈️✈️✈️✈️✈️✈️✈️✈️最终表格✈️✈️✈️✈️✈️✈️✈️✈️✈️")
        print(putDataFrame)
        print("\n")
        fus.outExcel(putDataFrame, config.outputTableName)  


if __name__ == '__main__':
   
    
    try:
        tryWritePrintToFile()
        work()
    except Exception as e:
        print(traceback.format_exc())
        # now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # errorPath = fus.getWorkDirPath() + fus.sperator() + "error" + fus.sperator() + now_time
        # errorFile = open(errorPath + ".txt", mode='w')
        # errorFile.write(traceback.format_exc())
            
        