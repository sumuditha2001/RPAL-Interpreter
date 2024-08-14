from DataStructures import *

binary_operations=["+", "-", "/", "*", "**", "eq", "ne", "gr", "ge", "le",">", "<", ">=", "<=", "or", "&", "aug", "ls"]
unary_operations=[ "neg", "not"]
default_functions=["Conc","Stern","Stem","Order","Null","Isfunction","Istuple","Istruthvalue","Isinteger","Isstring","Isdummy","Print"]

def is_binary_operation(op):
    '''Check if the operator is a binary operation'''
    return op.value in binary_operations

def is_unary_operation(op):
    '''Check if the operator is a unary operation'''
    return op.value in unary_operations

def is_default_function(op):
    '''Check if the operator is a default function'''
    return op.value in default_functions

def is_int_operation(op):
    '''Check if the operator is an integer operation'''
    return op in ["+", "-", "*", "/", "**", "eq", "ne", "gr", "ge", "le", ">", "<", ">=", "<=","ls"]

def apply_binary_operation(op, left, right):
    '''Apply the binary operation to the left and right operands. Here all values are returnd as string values. Types are assigned in the cse_machine'''
    if op.value == "+":
        return str(left + right)
    elif op.value == "-":
        return str(left - right)
    elif op.value == "*":
        return str(left * right)
    elif op.value == "/":
        if right == 0:
            raise Exception("Division by zero")
        return str(left / right)
    elif op.value == "**":
        return str(left ** right)
    elif op.value == "eq":
        return str(left == right)
    elif op.value == "ne":
        return str(left != right)
    elif op.value == "gr":
        return str(left > right)
    elif op.value == "ge":
        return str(left >= right)
    elif op.value == "le":
        return str(left <= right)
    elif op.value == ">":
        return str(left > right)
    elif op.value == "<":
        return str(left < right)
    elif op.value == ">=":
        return str(left >= right)
    elif op.value == "<=":
        return str(left <= right)
    elif op.value == "or":
        return str(left or right)
    elif op.value == "&":
        return str(left and right)
    elif op.value == "aug":
        new_tuple=()
        if left.value !="nil":  # if left is an empty tuple no need to iterate
            for i in left.value:
                new_tuple+=(i,)
        new_tuple+=(right,)
        return new_tuple
    elif op.value == "ls":
        return str(left < right)
    else:
        raise Exception("Unknown binary operator: " + op.value)
    
def apply_unary_operation(op, operand):
    if op.value == "neg":
        return str(-operand)
    elif op.value == "not":
        if operand == "true":
            return "false"
        elif operand == "false":
            return "true"
    else:
        print(f"unknown operation    {op.value}")

def apply_default_function(op, operand):
    if op.value == "Print":
        if isinstance(operand,tuple_value):   # this is for printing tuples            
            new_tuple=()
            for i in operand.value:
                if isinstance(i, int_value):
                    i.value=int(i.value)  # convert the integer values to int
                new_tuple+=(i.value,)
            print(new_tuple)
        else:
            print(operand.value)    
        return operand
    elif op.value == "Isstring":
        return str(isinstance(operand, string_value))
    elif op.value == "Isinteger":
        return str(isinstance(operand, int_value))
    elif op.value == "Istruthvalue":
        if not isinstance(operand,id):  # in our implementation all truth values are stored as id objects
            return "False"
        elif operand.value =="true" or operand.value=="false" :
            return "True"
        else:
            return "False"
    elif op.value == "Isfunction":
            return str(operand.value in default_functions)  
    elif op.value == "Isdummy":
        if isinstance(operand, id) and operand.value=="dummy":
            return "True"
        else:
            return "False"
    elif op.value == "Null":  # check if the tuple is empty or not
        return str(operand.value=="nil")
    elif op.value == "Istuple":
        return str(isinstance(operand, tuple_value) or operand.value=="nil")
    elif op.value == "Order":
        if operand.value=="nil":
            return "0"
        else:
            return str(len(operand.value))
    elif op.value == "Stern":
        return str(operand.value[1:])
    elif op.value == "Stem":
        return str(operand.value[0])

    


