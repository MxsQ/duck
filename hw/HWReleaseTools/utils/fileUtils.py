import os
import json

isWindos = os.name.strip() == 'nt'
# tSperator = "\\" if isWindos else '/'
tSperator = os.sep


# 文件分隔符
def sperator():
    return tSperator

# 根据入口文件，获取数据文件路径
def getDataFileDir():
    entry_file_path = os.path.abspath(os.path.dirname(__file__))
    print('program path is :' + entry_file_path)
    splitWord = "" + sperator()
    fileItems = entry_file_path.split(sperator())
    dirPath = ''

    i = 0
    while i < (len(fileItems) - 2):
        if isWindos:
            if i == 0:
                dirPath =fileItems[i] + sperator()
            else:
                dirPath = dirPath + sperator() + fileItems[i]
        else:
            dirPath = dirPath + sperator() + fileItems[i]
        i = i + 1
    
    dirPath = dirPath + sperator() + "data"

    return dirPath

# 获取数据文件路径
def getDataFilePathByName(fileName):
    path = getDataFileDir() + sperator() + fileName
    return path

# 获取账户表扩展名
def getAccountExt(fileName):
    configPath = getDataFilePathByName(fileName)
    f = open(configPath, "rb")
    fJson = json.load(f, strict=False)
    ext = fJson['account-extention']
    return ext

# 获取转换表扩展名
def getConverExt(fileName):
    configPath = getDataFilePathByName(fileName)
    f = open(configPath, "rb")
    fJson = json.load(f, strict=False)
    ext = fJson['conver-extention']
    return ext

# 获取筛选条件，国家
def getContryConditionForFilt(fileName):
    configPath = getDataFilePathByName(fileName)
    f = open(configPath, "rb")
    fJson = json.load(f, strict=False)
    contries = fJson['filt-contries']
    return contries[0]

# 获取筛选条件，中文名
def getContryConditionEnForFit(contryies, cn2enDirt):
    condition = []
    for name in contryies:
        condition.append(cn2enDirt[name])
    return condition

# 获取中英文国家名
def getContryNameTransferDirt(fileName):
    configPath = getDataFilePathByName(fileName)
    f = open(configPath, "rb")
    fJson = json.load(f, strict=False)
    namesJson = fJson['cn-to-en']
    return namesJson[0]


# 输出excel
def outExcel(dataFrame, fileName):
    filePath = getDataFileDir() + sperator() + "out" + sperator() + fileName
    dataFrame.to_excel(filePath)
    print('make ' + fileName + ' done!  path is ' + filePath)


