import os
import json
import pandas as pd

# 文件分隔符
def sperator():
    return tSperator


# 工作文件夹
def getWorkDirPath():
    entry_file_path = os.path.abspath(os.path.dirname(__file__))
    print('program path is :' + entry_file_path)
    fileItems = entry_file_path.split(sperator())
    dirPath = ''

    i = 0
    print('is window = ' + str(isWindos))
    while i < (len(fileItems) - 2):
        if isWindos:
            if i == 0:
                dirPath =fileItems[i] + sperator()
            else:
                dirPath = dirPath + sperator() + fileItems[i]
        else:
            if fileItems[i] != "":
                dirPath = dirPath + sperator() + fileItems[i]
        i = i + 1
    
    dirPath = dirPath + sperator() + "data"

    print("work dir is " + dirPath)
    return dirPath

isWindos = os.name.strip() == 'nt'
tSperator = os.sep
workDirPath = getWorkDirPath()

def getFileName(filePath):
    fileName = filePath
    if sperator() in filePath:
        pathItems = filePath.split(sperator())
        fileName = pathItems[len(pathItems) - 1]
    
    if "." in fileName:
        return fileName.split('.')[0]



# 所有配置文件
def getWorkFiles():
    indexFilePath = workDirPath + sperator() + "config" + sperator() + "index.json"
    f = open(indexFilePath, "rb")
    fJson = json.load(f, strict=False)
    fileNames = fJson['ruleFiles']

    filePaths = []
    for name in fileNames:
        filePaths.append(workDirPath + sperator() + "config" + sperator() + name)

    return filePaths

def getIndexFileJson():
    indexFilePath = workDirPath + sperator() + "config" + sperator() + "index.json"
    f = open(indexFilePath, "rb")
    return json.load(f, strict=False)

# 获取配置文件json
def getRulesJson(filePath):
    f = open(filePath, "rb")
    fJson = json.load(f, strict=False)
    return fJson

# 读取excel
def getExcel(fileNames):
    datas = []
    for name in fileNames:
        filePath = workDirPath + sperator() + name
        if name.__contains__('.xlsx'):
            datas.append(pd.read_excel(filePath))
        elif name.__contains__(".csv"):
            try:
                datas.append(pd.read_csv(filePath, encoding='gbk'))
            except:
                datas.append(pd.read_csv(filePath, encoding='utf-8'))

    return datas

# 输出excel
def outExcel(dataFrame, fileName):
    filePath = getWorkDirPath() + sperator() + "out" + sperator() + fileName + '.xlsx'
    dataFrame.to_excel(filePath)
    print('make table' + fileName + ' done!  path is ' + filePath)