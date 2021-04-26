import utils.fileUtils as fileUtils

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
        
# 格式化时间
def formatDate(dataFrame, column):
    def format(date):
        # d = date
        # if isinstance(date, int):
        d = str(date)
        d = d.replace('-', '')
        year = d[0:4]
        mouth = fileUtils.sperator() + d[4:6]
        day = fileUtils.sperator() + d[6:8]
        d = year + mouth + day
        return d

    dataFrame[column] = dataFrame[column].map(lambda s: format(s))
        