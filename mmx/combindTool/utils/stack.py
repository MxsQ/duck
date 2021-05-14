class Stack():

    def __init__(self):
        self.stack = []
        self.size = 0

    def pop(self):
        if self.size != 0:
            self.size = self.size - 1
            return self.stack.pop()
        else:
            return ''

    def push(self, value):
        self.size = self.size + 1
        self.stack.append(value)
    
    def peek(self):
        return self.stack[self.size - 1]
        
    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False
    
    
