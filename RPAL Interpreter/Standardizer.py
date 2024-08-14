# Convert Abstract Syntax Tree to Standardized Tree

from DataStructures import node

def extract_string(string):
    '''Split the string by colon and get the second part.for example, if the input is "IDENTIFIER : Temp", it will return "IDENTIFIER" and "Temp"'''
    extracted_string = string.split(":")[-1].strip()
    extracted_type = string.split(":")[0].strip()
    return extracted_type,extracted_string

def standardize_tree(Node):
    '''Main function of Standardizer. Standardize the tree by applying the following rules:'''
    if len(Node.children) > 0:
        for i in range(len(Node.children)):
            # Call standardize_tree recursively
            standardize_tree(Node.children[i])
    # Standardize the node after children are standardized ( Depth First Mannner )
    standardize_node(Node)
    return Node
    
def standardize_node(Node):
    '''Standardize the node by applying the following rules:'''
    if Node.value == "let":
        standardize_let(Node)
    if Node.value == "where":
        standardize_where(Node)
    if Node.value == "function_form":
        standardize_function_form(Node)
    if Node.value == "lambda" and len(Node.children) > 2:
        standardize_multi_parameters_function(Node)
    if Node.value == "within":
        standardize_within(Node)
    if Node.value == "@":
        standardize_at(Node)
    if Node.value == "and":
        standardize_and(Node)
    if Node.value == "rec":
        standardize_rec(Node)

def standardize_let(Node):
    '''Standardize the Let Node '''
    # Check for Errors
    if len(Node.children) != 2:
        print("Error: Expected 2 children in Let Node")
        return
    if Node.children[0].value != "=":
        print("Error: Expected '=' in left child of Let Node")
        return
    
    E = Node.children[0].children[1]
    P = Node.children[1]
    
    Node.children[1] = E
    Node.children[0].children[1] = P
    
    Node.value = "gamma"
    Node.children[0].value = "lambda"

def standardize_where(Node):
    '''Standardize the Where Node'''
    # Check for Errors
    if len(Node.children) != 2:
        print("Error: Expected 2 children in Where Node")
        return
    if Node.children[1].value != "=":
        print("Error: Expected '=' in right child of Where Node")
        return
    
    E = Node.children[1].children[1]
    P = Node.children[0]
    X = Node.children[1].children[0]
    
    Node.children[0]=node("lambda")
    Node.children[0].children.append(X)
    Node.children[0].children.append(P)
    Node.children[1]= E
    
    Node.value = "gamma"

def standardize_function_form(Node):
    '''Standardize the Function Form Node'''
    # Check for Errors
    if len(Node.children) < 3:
        print("Error: Expected at least 3 children in Function Form Node")
        return
    
    P=Node.children[0]
    E=Node.children[-1]
    i=1
    variables=[]
    while i < len(Node.children)-1:
        variables.append(Node.children[i])
        i +=1

    Node.value="="
    Node.children=[]
    Node.children.append(P)

    temp=Node

    for i in range(len(variables)):
        temp.children.append(node("lambda"))
        temp.children[1].children.append(variables[i])
        temp=temp.children[-1]

    temp.children.append(E)
    Node=temp



def standardize_multi_parameters_function(Node):
    '''Standardize the Lambda Node with multiple parameters'''
    if len(Node.children) <2:
        print("Error: Expected at least 2 children in Lambda Node")
        return
    
    E=Node.children[-1]
    i=0
    variables=[]
    while i<len(Node.children)-1:
        variables.append(Node.children[i])
        i +=1

    Node.children=[]
    Node.children.append(variables[0])
    temp=Node
    i=1
    while i< (len(variables)):
        temp.children.append(node("lambda"))
        temp.children[-1].children.append(variables[i])
        temp=temp.children[-1]
        i +=1
    temp.children.append(E)

def standardize_within(Node):
    '''Standardize the Within Node'''
    if(len(Node.children) !=2):
        print("within node should only have 2 children")
        return
    if(Node.children[0].value !="=" or Node.children[1].value !="="):
        print("within node should have 2 '=' nodes as it's children" )
        return
    
    x1=Node.children[0].children[0]
    e1=Node.children[0].children[1]
    x2=Node.children[1].children[0]
    e2=Node.children[1].children[1]

    Node.value="="
    Node.children=[]
    Node.children.append(x2)
    Node.children.append(node("gamma"))
    Node.children[1].children.append(node("lamda"))
    Node.children[1].children.append(e1)
    Node.children[1].children[0].children.append(x1)
    Node.children[1].children[0].children.append(e2)



def standardize_at(Node):
    '''Standardize the @ Node'''
    if (len(Node.children) != 3):
        print ("@ node should have exactly 3 children")
        return
    
    E1=Node.children[0]
    N=Node.children[1]
    E2=Node.children[2]

    Node.value="gamma"
    Node.children=[]
    Node.children.append(node("gamma"))
    Node.children.append(E2)
    Node.children[0].children.append(N)
    Node.children[0].children.append(E1)

def standardize_and(Node):
    '''Standardize the And Node'''
    if (len(Node.children) <2):
        print (" and node should have at least 2 children")
        return
    
    for child in Node.children:
        if child.value != "=":
            print (" each child of the and node should be '=' node ")
            return
        
    var_list=[]
    E_list=[]

    for child in Node.children:
        var_list.append(child.children[0])
        E_list.append(child.children[1])

    Node.value="="
    Node.children=[]
    Node.children.append(node(","))
    Node.children.append(node("tau"))
    Node.children[0].children=var_list
    Node.children[1].children=E_list
    



def standardize_rec(Node):
    '''Standardize the Recursion Node'''
    if (len(Node.children) != 1):
        print("rec node should have exactly 1 children")
        return
    if (Node.children[0].value != "="):
        print("The child of rec node should be '=' node")
        return
    x=Node.children[0].children[0]
    E=Node.children[0].children[1]
    Node.value="="
    Node.children=[]
    Node.children.append(x)
    Node.children.append(node("gamma"))
    Node.children[1].children.append(node("Y_star : Y"))
    Node.children[1].children.append(node("lambda"))
    Node.children[1].children[1].children.append(x)
    Node.children[1].children[1].children.append(E)




# Unnecessary functions ( tau, unary_op, binary_op, comma) are commented out

# def standardize_tau(Node):
#     if len(Node.children) < 2:
#         print("Error: Expected at least 2 children in Tau Node")
#         return
#     expression_list =[]
#     for i in range(len(Node.children)):
#         expression_list.append(Node.children[i])

#     Node.value="gamma"
#     Node.children=[]
#     Node.children.append(node("gamma"))
#     Node.children.append(expression_list[-1])
#     Node.children[0].children.append(node("aug"))

#     i=1
#     temp=Node.children[0]
#     while i<len(expression_list):
#         temp.children.append(node("gamma"))
#         temp.children[1].children.append(node("gamma"))
#         temp.children[1].children.append(expression_list[-1-i])
#         temp.children[1].children[0].children.append(node("aug"))
#         temp=temp.children[1].children[0]
#         i +=1
#     temp.children.append(node("nil"))


# def standardize_unary_op(Node):
#     if (len(Node.children) !=1):
#         print("unary operations should only have one child")
#         return

#     uop=Node.value
#     E=Node.children[0]
#     Node.value="gamma"
#     Node.children=[]
#     Node.children.append(node(uop))
#     Node.children.append(E)

# def standardize_binary_op(Node):
#     if(len(Node.children) != 2):
#         print(f"Binary operation {Node.value} node should have exactly 2 children")
#         return
    
#     op=Node.value
#     E1=Node.children[0]
#     E2=Node.children[1]

#     Node.value="gamma"
#     Node.children=[]
#     Node.children.append(node("gamma"))
#     Node.children.append(E2)
#     Node.children[0].children.append(node(op))
#     Node.children[0].children.append(E1)


# def standardize_comma(Node):
#     if(len(Node.children) != 2):
#         print("comma node should have exactly 2 children")
#         return
#     if(Node.children[0].value != ","):
#         print("first child of comma node should be a comma node")
#         return
    
#     print("entered comma")
#     var_list=[]
#     for child in Node.children[0].children:
#         var_list.append(child)
    
#     E=Node.children[1]

#     Node.children=[]
#     Node.children.append(node("IDENTIFIER : Temp"))
#     Node.children.append(node("gamma"))
#     Node.children[1].children.append(node("lamda"))
#     Node.children[1].children.append(node("gamma"))
#     Node.children[1].children[0].append(var_list[-1])
#     Node.children[1].children[1].append(node("IDENTIFIER : Temp"))
#     Node.children[1].children[1].append(node("IDENTIFIER : " + str(len(var_list))))

#     temp=Node.children[1].children[0]
#     for i in range(len(var_list)-1):
#         temp.append(node("gamma"))
#         temp.children[1].children.append(node("lambda"))
#         temp.children[1].children.append(node("gamma"))
#         temp.children[1].children[0].children.append(var_list[i])
#         temp.children[1].children[1].children.append(node("IDENTIFIER : Temp"))
#         temp.children[1].children[1].children.append(node("IDENTIFIER : " + str(len(var_list)-(i+1))))
#         temp=temp.children[1].children[0]
    
#     temp.children.append(E)