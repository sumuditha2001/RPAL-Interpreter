from DataStructures import *

def extract_string(string):
    '''Split the string by colon.for example, if the input is "IDENTIFIER : Temp", it will return "IDENTIFIER" and "Temp"'''
    extracted_string = string.split(":")[-1].strip()
    extracted_type = string.split(":")[0].strip()
    return extracted_type,extracted_string

def CS (ST):
    '''Flatten the tree and return the control structures as a list of stacks. Each stack represents a control structure. The first stack in the list is the initial control structure. '''
    control_structures=[]
    current_cs=stack()
    Stack=stack()
    control_structures.append(current_cs)
    tree_flattener(ST,control_structures,current_cs)
    return control_structures


def tree_flattener(Node,control_structures,current_cs):
    if (Node.value == "lambda"):
        flattener_lambda(Node,control_structures,current_cs)

    elif (Node.value == "->"):
        flattener_arrow(Node,control_structures,current_cs)

    elif (Node.value == "tau"):
        flattener_tau(Node,control_structures,current_cs)

    else:
        if (Node.value == "gamma") or Node.value in ("or" , "&" , "gr" , "ge" , "ls" , "le" , "eq" , "ne" , "+" , "-" , "*" , "/" , "**", "not" , "neg","aug","true","false","nil","dummy"):
            if Node.value == "gamma":
                current_cs.push(gamma(0))   # gamma object with 0 arguments
            else:
                current_cs.push(id(Node.value))  # operators,truth values nil and dummmy are pushed as id objects
        else:
            category,value=extract_string(str(Node.value))
            if (category == "INTEGER"):
                current_cs.push(int_value(value))   # integer values are pushed as int_value objects
            elif (category == "IDENTIFIER"):
                current_cs.push(id(value))    # identifiers are pushed as id objects
            elif (category == "Y_star"):
                current_cs.push(y_star(value))    # Y_star values are pushed as y_star objects which helps in recursion
            elif(category == "STRING"):
                current_cs.push(string_value(value))    # string values are pushed as string_value objects
    for child in Node.children:     # recursively call the flattener for each child of the node
            tree_flattener(child,control_structures,current_cs)

def flattener_lambda(Node,control_structures,current_cs):
    '''Flatten the Lambda node'''
    if (Node.children[0].value == ","):   # if the lambda node has multiple parameters
        var_list=[]
        for child in Node.children[0].children:   # extract the variables  to a list
            var_list.append(child.value.value)
        string=",".join(var_list)                  # convert the list to a string with comma separated values
        Node.children[0].value="IDENTIFIER : "+string    # change the value of the node as a identifier with the string
        Node.children[0].children=[]
    
    category,value=extract_string(str(Node.children[0].value))
    lamda=Lambda(len(control_structures),value,-1)  # create a lambda object with the next index of the control structures list and the variable list
    current_cs.push(lamda)   # push the lambda object to the current control structure

    new_cs=stack()          # create a new control structure
    control_structures.append(new_cs)

    for child in Node.children[1:]:  # recursively call the flattener for each child of the node
        tree_flattener(child,control_structures,new_cs)
    
    Node.children=[]  # seperate from the right child of the lambda node
    
def flattener_arrow(Node,control_structures,current_cs):
    '''Flatten the If node'''

    delta_then=delta(len(control_structures))  # create a delta object to be pushed when the condition is true, with the next index of the control structures list
    current_cs.push(delta_then)
    then_cs=stack()
    control_structures.append(then_cs)
    tree_flattener(Node.children[1],control_structures,then_cs)  # recursively call the flattener for the then part of the arrow node
    
    delta_else=delta(len(control_structures))  # create a delta object to be pushed when the condition is false, with the next index of the control structures list
    current_cs.push(delta_else)
    else_cs=stack()
    control_structures.append(else_cs)
    tree_flattener(Node.children[2],control_structures,else_cs)  # recursively call the flattener for the else part of the arrow node

    current_cs.push(id("beta"))  # push the id object with beta value to identify the arrow when evaluating
    tree_flattener(Node.children[0],control_structures,current_cs)  # recursively call the flattener for the condition of the arrow node
    Node.children=[]   # seperate from the children of the arrow node

def flattener_tau(Node,control_structures,current_cs):
    '''Flatten the tau node'''

    tau_object=tau(len(Node.children))   # create a tau object with the number of children of the tau node  
    current_cs.push(tau_object)
    for child in Node.children:     # recursively call the flattener for each child of the node
        tree_flattener(child,control_structures,current_cs)
    Node.children=[]  # seperate from the children of the tau node






    

    
