# Description: This file contains the data structures used in the interpreter

def extract_string(string):
    '''Split the string by colon.for example, if the input is "IDENTIFIER : Temp", it will return "IDENTIFIER" and "Temp"'''
    extracted_string = string.split(":")[-1].strip()
    extracted_type = string.split(":")[0].strip()
    return extracted_type,extracted_string


# Class token is used to represent the tokens in the input file
class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

# Class node is used to represent the nodes in the AST and ST         
class node:
    def __init__(self,value):
        self.value = value
        self.children = []


def print_tree(root, level=0):
    '''Print the tree in a readable format'''
    if root is not None:
        result=extract_string(str(root.value))
        if result[0] == result[1]:
            if result[0] == "nil":
                print("." * (level * 1) + '<nil>')
            elif result[0] == "true":
                print("." * (level * 1) + '<true>')
            elif result[0] == "false":
                print("." * (level * 1) + '<false>')
            elif result[0] == "dummy":
                print("." * (level * 1) + '<dummy>')
            else:
                print("." * (level * 1) + str(root.value))
        elif result[0] == "IDENTIFIER":
            print("." * (level * 1) + '<ID:'+result[1]+'>')
        elif result[0] == "STRING":
            print("." * (level * 1) + '<STR:'+result[1]+'>')
        elif result[0] == "INTEGER":
            print("." * (level * 1) + '<INT:'+result[1]+'>')
        for child in root.children:
            print_tree(child, level + 1)

# Class stack is used to represent the control structures,Stack 
class stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def top(self):
        return self.items[-1]
    def push(self,value):
        self.items.append(value)
    def pop(self):
        if self.isEmpty():
            print('Stack is empty')
            return
        return self.items.pop()
    


# The following classes are used to represent the different types of objects used when evaluating the control structures
class id:
    def __init__(self, value):
        self.value= value
        
class string_value:
    def __init__(self, value):
        self.value= value

class int_value:
    def __init__(self, value):
        self.value= value

class gamma:
    def __init__(self, index):
        self.index=0   
        
class Lambda:
    def __init__(self, index , var_list, E):
        self.index = index
        self.var_list = var_list
        self.E = E

class delta:
    def __init__(self, index ):
        self.index=index

class tau:
    def __init__(self, index ):
        self.index=index

class y_star:
    def __init__(self, value ):
        self.value=value

class eta:
    def __init__(self, index,var_list,E): 
        self.index=index
        self.var_list=var_list
        self.E=E

class tuple_value:
    def __init__(self, value):
        self.value=value

class environment:
    def __init__(self, index, value, parent):
        self.index=index
        self.parent=parent
        self.value=value
