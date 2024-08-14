from DataStructures import *
from applicator import *
import tree_flattener

cur_env_index=0   # global variable to keep track of the next environment index

def extract_environment(control):
    '''Extract the current environment object from the control stack'''
    result_env=None
    for element in control.items:  # iterate through the control and return the right environment object from the control stack
        if (not isinstance(element,environment)):
            continue
        else:
            result_env=element
    
    return result_env

def lookup(current_element,current_environment,environment_list):
    '''Lookup the value of the current element in the environment tree'''

    if current_element.value in current_environment.value:
        return current_environment.value[current_element.value]
    else:
        if current_environment.parent == None:  # if the it is in the primitive environment
            raise Exception(f"Undeclared Identifier : {current_element.value}")  # raise an exception if the value is not found in the environment tree
        else:
            return lookup(current_element,environment_list[current_environment.parent],environment_list) # recursively call the lookup function with the parent of the current environment
 

def evaluate (structures):
    '''Evaluate the control structures. This function takes the control structures as input and returns the stack after evaluation'''

    Stack=stack()               # Initialize the control,stack, and environment 
    environment_list={}
    control=stack()
    control_structures=structures

    primitive_environment=environment(0,{},None)  # create the primitive environment and push tothe control and the stack
    environment_list[0]=primitive_environment
    Stack.push(primitive_environment)
    control.push(primitive_environment)

    control.items.extend(control_structures[0].items)   # push the first control structure to the control stack as separate elements

    while not control.isEmpty():  # iterate through the control stack until it is empty

        current_element=control.pop()

        if isinstance(current_element,id):
            if (not is_binary_operation(current_element)) and (not is_unary_operation(current_element)) and current_element.value != "beta" and (current_element.value not in ["nil","dummy","true","false"] and (not is_default_function(current_element)) ): 
                # this if block is to check if the current element is a predifined function or a binary or unary operation or "nil","dummy","true","false" or beta
                rule_1(current_element,Stack,environment_list,control)

            elif current_element.value == "beta":
                # this block is to check if the current element is beta to evaluate the if-then-else statement
                rule_8(current_element,Stack,environment_list,control,control_structures)

            elif is_default_function(current_element) or current_element.value in ["nil","true","false","dummy"]:
                # this block is to check if the current element is a predefined function or "nil","true","false","dummy"
                Stack.push(current_element)  # push the predefined value to the stack

            elif is_binary_operation(current_element):
                # this block is to check if the current element is a binary operation
                rule_6(current_element,Stack,environment_list,control)

            elif is_unary_operation(current_element):
                # this block is to check if the current element is a unary operation
                rule_7(current_element,Stack,environment_list,control)

        elif isinstance(current_element,int_value):
            # this block is to check if the current element is an integer value
            Stack.push(current_element)  # if it is just push it to the stack

        elif isinstance(current_element,string_value):
            # this block is to check if the current element is a string value
            Stack.push(current_element) # if it is just push it to the stack

        elif isinstance(current_element,tau):
            # this block is to check if the current element is a tau object
            rule_9(current_element,Stack,environment_list,control)
            
        elif isinstance(current_element,Lambda):
            # this block is to check if the current element is a lambda object
            rule_2(current_element,Stack,environment_list,control)

        elif isinstance(current_element,environment):
            # this block is to check if the current element is an environment object
            rule_5(current_element,Stack,environment_list,control)

        elif isinstance(current_element,y_star):
            # this block is to check if the current element is a y_star object which helps in recursion
            Stack.push(current_element) # if it is just push it to the stack

        elif isinstance(current_element,gamma):
            # this block is to check if the current element is a gamma object
            first_element=Stack.pop()
            second_element=Stack.pop()

            if isinstance(first_element,y_star):
                rule_12(second_element,Stack,environment_list,control)

            elif isinstance(first_element,eta):
                Stack.push(second_element)
                rule_13(first_element,Stack,environment_list,control)

            elif isinstance(first_element,Lambda):
                Stack.push(second_element)
                var_list=first_element.var_list.split(",")    # split the variable list of the lambda object

                if len(var_list) >1:  # checks whether the lambda object has multiple parameters
                    rule_11(first_element,Stack,environment_list,control,control_structures,var_list)

                else:
                    rule_4(first_element,Stack,environment_list,control,control_structures,var_list)

            elif isinstance(first_element,tuple_value):
                Stack.push(second_element)
                rule_10(first_element,Stack,environment_list,control)

            elif is_default_function(first_element ):
                Stack.push(second_element)
                rule_3(first_element,Stack,environment_list,control)

    return Stack

            
def rule_1(current_element,Stack,environment_list,control):
    '''Rule 1: Lookup the value of the current element in the environment tree and push it to the stack'''

    current_environment=extract_environment(control)
    val=lookup(current_element,current_environment,environment_list) 
    Stack.push(val)

def rule_2(current_element,Stack,environment_list,control):
    '''Rule 2: assign the current environment index to the E value of lambda object which represents the environment and push the lambda object to the stack'''

    current_environment=extract_environment(control)   
    current_element.E=current_environment.index
    Stack.push(current_element)

def rule_3(current_element,Stack,environment_list,control):
    '''Rule 3: Apply the predefined functions on the operands and push the result to the stack'''
    
    if current_element.value != "Conc":  # Here conc is a special case which will pop 2 gammas from the control stack and apply the conc operation on 2 strings
        operand=Stack.pop()
        if current_element.value == "Print":
            result=apply_default_function(current_element,operand)
            Stack.push(operand)  # here the operand is pushed back to the stack again to follow the rule set until the cotrol stack is empty

        else:
            result=apply_default_function(current_element,operand)
            if(current_element.value in ["Isstring", "Istruthvalue", "Isfunction","Istuple","Isinteger","Isdummy","Null"]):
                # this block is to check if the predefined function will return truth values or not
                if result == "True":
                    Stack.push(id("true"))
                else:
                    Stack.push(id("false"))

            elif current_element.value == "Order":
                Stack.push(int_value(result))  # if the predefined function is order then the result is pushed as an integer value

            else:
                Stack.push(string_value(result)) # if the predefined function is not the case of above scenarios then the result is pushed as a string value

    else:
        left=Stack.pop()    
        right=Stack.pop()

        if not (isinstance(left,string_value) and isinstance(right,string_value)):
            raise Exception("Non-strings used in conc call")   # raise an exception if the operands are not strings   
        
        if not isinstance(control.pop(),gamma):
            print("error in rule 3 : conc should have 2 gamma objects to operate on strings")
            return  
        result=left.value + right.value
        Stack.push(string_value(result))


def rule_4(current_element,Stack,environment_list,control,control_structures,var_list):
    '''Rule 4: Create a new environment with the current environment as the parent and assign the variables to the memory of the environment and push the environment to the stack and the control '''
    global cur_env_index # global variable to keep track of the next environment index
    memory={}
    current_environment=extract_environment(control)  
    obj=Stack.pop()
    memory[var_list[0]]=obj   # assign the variable to the memory of the environment

    new_environment=environment(cur_env_index+1,memory,current_element.E)   # create a new environment object with the next index of the environment list and the memory
    environment_list[cur_env_index+1]=new_environment
    cur_env_index+=1
    Stack.push(new_environment)    # push the new environment to the stack
    control.push(new_environment)  # push the new environment to the control
    control.items.extend(control_structures[current_element.index].items) # push the control structure of the lambda object to the control stack as separate elements


def rule_5(current_element,Stack,environment_list,control):
    '''Rule 5: Pop the value and the environment from the stack and check if the current element and the environment are the same and push the value back to the stack'''

    value=Stack.pop()
    environment=Stack.pop()
    if current_element != environment:
        print("error in rule 5 environement missmatch")
        return
    Stack.push(value)

def rule_6(current_element,Stack,environment_list,control):
    '''Rule 6: Apply the binary operations on the operands and push the result to the stack'''

    left=Stack.pop()
    right=Stack.pop()

    if current_element.value == "aug":
        if not(isinstance(left,tuple_value) or (left.value == "nil")):
            raise Exception("Cannot augment a non tuple")
        result=apply_binary_operation(current_element,left,right)
        Stack.push(tuple_value(result))

    elif is_int_operation(current_element.value):
        # this block is to check if the binary operation is an integer operation
        if (not isinstance(left,int_value)) or (not isinstance(right,int_value)):
            raise Exception(f"Illegal Operands for  {current_element.value}")  # raise an exception if the operands are not integers    
        
        else:
            left=int(left.value)
            right=int(right.value)
            result=apply_binary_operation(current_element,left,right)

            if current_element.value in ["+", "-", "*", "/", "**"]:
                # this block is to check if the binary operation will output an int value
                Stack.push(int_value(result))

            else:
                # this block is to check if the binary operation will output a truth value
                if result == "True":
                    Stack.push(id("true"))
                else:
                    Stack.push(id("false"))
                    
    else:
        if (not (left.value=="true" or left.value== "false")) or (not (right.value=="true" or right.value== "false")):
            result= "False"   # if the operands are not boolean values then the result is false
    
        if left.value == "true" and right.value == "true":
            result=apply_binary_operation(current_element,True,True)

        elif left.value == "true" and right.value == "false":
            result=apply_binary_operation(current_element,True,False)

        elif left.value == "false" and right.value == "true":
            result=apply_binary_operation(current_element,False,True)

        else:
            result=apply_binary_operation(current_element,False,False)

        if result == "True":
            Stack.push(id("true"))

        else:
            Stack.push(id("false"))


def rule_7(current_element,Stack,environment_list,control):
    operand=Stack.pop()
    if (current_element.value == "neg"):
        if not isinstance(operand,int_value):   
            raise Exception("Illegal Operands for neg operation")  # raise an exception if the operand is not an integer
        operand=int(operand.value)
        result=apply_unary_operation(current_element,operand)
        Stack.push(int_value(result))

    else:
        if not (operand.value=="true" or operand.value== "false"):
            raise Exception("Non-boolean for 'not' application")
        result=apply_unary_operation(current_element,operand.value)
        Stack.push(id(result))

def rule_8(current_element,Stack,environment_list,control,control_structures):
    '''Rule 8: Evaluate the if-then-else statement and push the result to the control stack'''
    
    result=Stack.pop()  
    if (result.value != "true") and (result.value != "false"):
        print("error in rule 8  : at the top of the stack is not a boolean value")
        return 
    
    else:
        delta_else=control.pop()
        delta_then=control.pop()

        if ( not isinstance(delta_then,delta)) or (not isinstance(delta_else,delta)):
            print("error in rule 8 : delta then and delta else should be delta objects")
            return
        
        else:
            if result.value == "true":
                control.items.extend(control_structures[delta_then.index].items) # if the result is true then push the control structure of delta then to the control stack as separate elements
            else:
                control.items.extend(control_structures[delta_else.index].items) # if the result is false then push the control structure of delta else to the control stack as separate elements

def rule_9(current_element,Stack,environment_list,control):
    '''Rule 9: Pop the value from the stack and create a tuple object with the value and push it to the stack'''
    
    output_tuple=()
    for i in range(current_element.index):   # iterate through the index of the tau object and pop the values from the stack and create a tuple object
        value=Stack.pop()     
        output_tuple = output_tuple + (value,)
    Stack.push(tuple_value(output_tuple))

def rule_10(current_element,Stack,environment_list,control):
    '''Rule 10: Pop the index from the stack and select the value from the tuple object and push it to the stack'''
    index=Stack.pop()
    selected_val=current_element.value[int(index.value)-1]
    Stack.push(selected_val)

def rule_11(current_element,Stack,environment_list,control,control_structures,var_list):
    '''Rule 11: Create a new environment with the current environment as the parent and assign the variables to the memory of the environment and push the environment to the stack and the control '''
    global cur_env_index
    memory={}
    current_environment=extract_environment(control)
    obj=Stack.pop()

    if not isinstance(obj,tuple_value):
        print (" error : when assining nary functions stack top should be a tuple")
    else:
        i=0
        for var in var_list:
            memory[var]=obj.value[i]
            i+=1

    new_environment=environment(cur_env_index+1,memory,current_element.E) # create a new environment object with the next index of the environment list and the memory
    environment_list[cur_env_index+1]=new_environment
    cur_env_index+=1

    Stack.push(new_environment)  # push the new environment to the stack
    control.push(new_environment)  # push the new environment to the control
    control.items.extend(control_structures[current_element.index].items) # push the control structure of the lambda object to the control stack as separate elements


def rule_12(current_element,Stack,environment_list,control):
    '''Rule 12: Create an eta object with the current element as the lambda object and push it to the stack'''

    if not isinstance(current_element,Lambda):
        print("error in rule 12 : top of the stack should be lamda object")
        return
    
    else:
        eta_object=eta(current_element.index,current_element.var_list,current_element.E)  # create an eta object with the same parameters of the lambda object
        Stack.push(eta_object)

def rule_13(current_element,Stack,environment_list,control):
    '''Rule 13: Create a lambda object with same parameters of the eta object and push it to the stack'''

    lambda_object=Lambda(current_element.index,current_element.var_list,current_element.E)
    Stack.push(current_element)  # push the eta object back to the stack
    Stack.push(lambda_object)  # push the lambda object to the stack
    control.push(gamma(0)) # push a gamma object to the control stack
    control.push(gamma(0)) # push a gamma object to the control stack

    


