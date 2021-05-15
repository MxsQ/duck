from utils.stack import Stack
import re as re

class Caculator():

    ArithmeticSymbol = ['+', '-', '*', '/']
    # 是否是数字的正则
    numberRule = "[0-9]+\.?[0-9]*"
    # 记录是数字的str
    numberList = []

    # 是不是记录的常量数字
    def isConstanNumber(self, s):
        return self.numberList.__contains__(s)

    # 判断是不是数字字符串
    def saveNumber(self, s):
        if re.match(self.numberRule, s, flags=0) is not None:
           self.numberList.append(s)


    # 判断是不是算数符号
    def isFormulaSamble(self, symbol):
        for s in self.ArithmeticSymbol:
            if symbol == s:
                return True
        return False


    # 判断是不是括号
    def isBrackets(self, symbol):
        if symbol == "(":
            return True
        if symbol == ")":
            return True
        return False

    
    # 比较算数符优先级
    def isHiherOrEqulaSamble(self, a, b):
        if a == '*':
            return True
        if a == '/':
            return True
        if b == '*':
            return False
        if b == '/':
            return False


    # 从str中转换出算式, list，中缀表达式
    def transfroFormula(self, rule):
        r = rule.replace(" ", "")
        # print("->>>", r)
        curIndex = 0
        size = len(r)
        leftIndex = 0
        factors = []

        while (curIndex < size):
            if self.isFormulaSamble(r[curIndex]) is True:
                # 不会出现计算符号在0处
                if leftIndex != curIndex:
                    factors.append(r[leftIndex : curIndex])
                factors.append(r[curIndex])
                curIndex = curIndex + 1
                leftIndex = curIndex
            elif self.isBrackets(r[curIndex]) is True:
                # 出现在0处特殊处理
                if curIndex == 0:
                    factors.append(r[curIndex])
                    curIndex = curIndex + 1
                    leftIndex = curIndex
                    continue
                if leftIndex != curIndex:
                    factors.append(r[leftIndex : curIndex])
                factors.append(r[curIndex])
                curIndex = curIndex + 1
                leftIndex = curIndex
            else:
                curIndex = curIndex + 1
        # 处理最后一个因素
        if curIndex - leftIndex > 1:
           factors.append(r[leftIndex:curIndex])
        # print("算式前 ", factors)
        return factors

    
    # 中缀表达式转前缀表达式, list
    def media2pre(self, rule):
        outPutStack = Stack()
        tmpStack = Stack()
        
        curIndex = len(rule) - 1
        print("the formula before", rule)
        while (curIndex >= 0):
            factor = rule[curIndex]
            # print("tmp ", tmpStack.stack)
            # print("out ", outPutStack.stack)
            # print(factor)
            # print()
            if factor == ')':
                # 右括号直接入tmp栈
                tmpStack.push(factor)
                curIndex = curIndex - 1
            elif self.isFormulaSamble(factor) is True:
                # 标点符号
                if tmpStack.isEmpty() is True:
                    tmpStack.push(factor)
                    curIndex = curIndex - 1
                elif tmpStack.peek() == ")":
                    tmpStack.push(factor)
                    curIndex = curIndex - 1
                elif self.isHiherOrEqulaSamble(factor, tmpStack.peek()) is True:
                    tmpStack.push(factor)
                    curIndex = curIndex - 1
                else:
                    outPutStack.push(tmpStack.pop())
                    continue
            elif factor == '(':
                # 左括号
                while tmpStack.peek() != ')':
                    outPutStack.push(tmpStack.pop())
                tmpStack.pop()
                curIndex = curIndex - 1
            else:
                # 操作数：
                outPutStack.push(factor)
                curIndex = curIndex - 1
        
        # print("tmp ", tmpStack.stack)
        # print("out ", outPutStack.stack)

        while tmpStack.isEmpty() is False:
            outPutStack.push(tmpStack.pop())

        newRule = []
        while (outPutStack.isEmpty() is False):
            newRule.append(outPutStack.pop())

        for i in newRule:
            self.saveNumber(i)

        print("the formula end", newRule)
        print()

        return newRule

    def operater(self, obj1, obj2, symble, retain):
        a = float(obj1)
        b = float(obj2)
        if symble == '+':
            return a + b
        if symble == '-':
            return a - b
        if symble == '*':
            return round(a * b, retain)
        if symble == '/':
            return round(a / b, retain)
        

    # 前缀表达式计算
    def workByPre(self, factors, retain):
        tmpStack = Stack()
        # print("???", factors)
        while len(factors) > 0:
            f = factors.pop()
            if self.isFormulaSamble(f) is False:
                tmpStack.push(f)
            else:
                tmpStack.push(self.operater(tmpStack.pop(), tmpStack.pop(), f, retain))
        return tmpStack.pop()


    def __init__(self):
        pass