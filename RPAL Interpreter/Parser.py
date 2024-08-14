# Writing a parser for the rpal language

from DataStructures import node
from DataStructures import stack


Keywords = ["let", "fn", "in", "where", "aug", "or", "not", "true", "false", "nil", "dummy", "within",
            "and", "rec", "gr", "ge", "ls", "le", "eq", "ne"]

def is_keyword(value):
    ''' Check whether value is a keyword or not '''
    if value in ["in", "where", ".", "aug", "and", "or", "&", "not", "gr", "ge", "ls", "le", "eq", "ne", "+", "-", "*", "/", "**", "@", "within", "=", "rec", "let", "fn"]:
        return True
    else:
        return False


def Build(s,n,Stack):
    ''' Build the Tree node with given number of Children '''
    if n==0:
        Stack.push(node(s))
    else:
        p = node(s)
        children = []
        while n>0:
            children.append(Stack.pop())
            n -= 1
        while children:
            p.children.append(children.pop())
        Stack.push(p)

        
def Check(s,Tokens):
    ''' Consume a token if it matches with the given string '''
    if Tokens and s==Tokens[0].value:
        Tokens.pop(0)
    else:
        if Tokens:
            print("Error in Read "+str(s)+" != "+str(Tokens[0].value))
        else:
            print("Error in Read "+str(s)+" and Tokens is empty")


# Expressions

def E(Tokens,Stack):
    ''' The starting point of the parser '''
    if Tokens and (Tokens[0].value=='let'):
        Check('let',Tokens)
        D(Tokens,Stack)
        Check('in',Tokens)
        E(Tokens,Stack)
        Build('let',2,Stack)
    elif Tokens and (Tokens[0].value=='fn'):
        Check('fn',Tokens)
        n = 1
        while Tokens and Tokens[0].value != '.':
            Vb(Tokens,Stack)
            n += 1
        Check('.',Tokens)
        E(Tokens,Stack)
        Build('lambda',n,Stack)
    else:
        Ew(Tokens,Stack)

    # Return the final node
    return Stack
 
 
def Ew(Tokens,Stack):
    T(Tokens,Stack)
    if Tokens and (Tokens[0].value=='where'):
        Check('where',Tokens)
        Dr(Tokens,Stack)
        Build('where',2,Stack)


# Tuple Expressions

def T(Tokens,Stack):
    Ta(Tokens,Stack)
    n = 1
    if Tokens and (Tokens[0].value==','):
        while Tokens and Tokens[0].value == ',':
            Check(',',Tokens)
            Ta(Tokens,Stack)
            n += 1
        Build('tau',n,Stack)


def Ta(Tokens,Stack):
    Tc(Tokens,Stack)
    while Tokens and (Tokens[0].value=='aug'):
        Check('aug',Tokens)
        Tc(Tokens,Stack)
        Build('aug',2,Stack)


def Tc(Tokens,Stack):
    B(Tokens,Stack)
    if Tokens and (Tokens[0].value=='->'):
        Check('->',Tokens)
        Tc(Tokens,Stack)
        Check('|',Tokens)
        Tc(Tokens,Stack)
        Build('->',3,Stack)


# Boolean Expressions

def B(Tokens,Stack):
    Bt(Tokens,Stack)
    if Tokens and (Tokens[0].value=='or'):
        n = 1
        while Tokens and (Tokens[0].value=='or'):
            Check('or',Tokens)
            Bt(Tokens,Stack)
            n += 1
        Build('or',n,Stack)
        
def Bt(Tokens,Stack):
    Bs(Tokens,Stack)
    if Tokens and (Tokens[0].value=='&'):
        n = 1
        while Tokens and Tokens[0].value=='&':
            Check('&',Tokens)
            Bs(Tokens,Stack)
            n += 1
        Build('&',n,Stack)
        
def Bs(Tokens,Stack):
    if Tokens and (Tokens[0].value == 'not'):
        Check('not',Tokens)
        Bp(Tokens,Stack)
        Build('not',1,Stack)
    else:
        Bp(Tokens,Stack)

def Bp(Tokens,Stack):
    A(Tokens,Stack)
    if Tokens and (Tokens[0].value == 'gr' or Tokens[0].value == '>'):
        Check(Tokens[0].value,Tokens)
        A(Tokens,Stack)
        Build('gr',2,Stack)
    elif Tokens and (Tokens[0].value == 'ge' or Tokens[0].value == '>='):
        Check(Tokens[0].value,Tokens)
        A(Tokens,Stack)
        Build('ge',2,Stack)
    elif Tokens and (Tokens[0].value == 'ls' or Tokens[0].value == '<'):
        Check(Tokens[0].value,Tokens)
        A(Tokens,Stack)
        Build('ls',2,Stack)
    elif Tokens and (Tokens[0].value == 'le' or Tokens[0].value == '<='):
        Check(Tokens[0].value,Tokens)
        A(Tokens,Stack)
        Build('le',2,Stack)
    elif Tokens and (Tokens[0].value == 'eq' or Tokens[0].value == '=='):
        Check(Tokens[0].value,Tokens)
        A(Tokens,Stack)
        Build('eq',2,Stack)
    elif Tokens and (Tokens[0].value == 'ne' or Tokens[0].value == '!='):
        Check(Tokens[0].value,Tokens)
        A(Tokens,Stack)
        Build('ne',2,Stack)


# Arithmetic Expressions

def A(Tokens,Stack):
    if Tokens and (Tokens[0].value == '+'):
        Check('+',Tokens)
        At(Tokens,Stack)
        while Tokens and (Tokens[0].value == '+' or Tokens[0].value == '-'):
            if (Tokens[0].value == '+'):
                Check('+',Tokens)
                At(Tokens,Stack)
                Build('+',2,Stack)
            else:
                Check('-',Tokens)
                At(Tokens,Stack)
                Build('-',2,Stack)
    elif Tokens and (Tokens[0].value == '-'):
        Check('-',Tokens)
        At(Tokens,Stack)
        Build('neg',1,Stack)
        while Tokens and (Tokens[0].value == '+' or Tokens[0].value == '-'):
            if (Tokens[0].value == '+'):
                Check('+',Tokens)
                At(Tokens,Stack)
                Build('+',2,Stack)
            else:
                Check('-',Tokens)
                At(Tokens,Stack)
                Build('-',2,Stack)
    else:
        At(Tokens,Stack)
        while Tokens and (Tokens[0].value == '+' or Tokens[0].value == '-'):
            if (Tokens[0].value == '+'):
                Check('+',Tokens)
                At(Tokens,Stack)
                Build('+',2,Stack)
            else:
                Check('-',Tokens)
                At(Tokens,Stack)
                Build('-',2,Stack)
            
def At(Tokens,Stack):
    Af(Tokens,Stack)
    while Tokens and (Tokens[0].value == '*' or Tokens[0].value == '/'):
        if (Tokens[0].value == '*'):
            Check('*',Tokens)
            Af(Tokens,Stack)
            Build('*',2,Stack)
        else:
            Check('/',Tokens)
            Af(Tokens,Stack)
            Build('/',2,Stack)
            
def Af(Tokens,Stack):
    Ap(Tokens,Stack)
    if Tokens and (Tokens[0].value == '**'):
        Check('**',Tokens)
        Af(Tokens,Stack)
        Build('**',2,Stack)
        
def Ap(Tokens,Stack):
    R(Tokens,Stack)
    while Tokens and (Tokens[0].value == '@'):
        Check('@',Tokens)
        if Tokens and (Tokens[0].type == 'IDENTIFIER'):
            Build(Tokens[0],0,Stack)
            Check(Tokens[0].value,Tokens)
        else:
            print("Error in Ap, got "+Tokens[0].type+" - "+Tokens[0].value)
        R(Tokens,Stack)
        Build('@',3,Stack)


# Rators and Rands

def R(Tokens,Stack):
    Rn(Tokens,Stack)
    while Tokens and ((Tokens[0].type == 'IDENTIFIER' or Tokens[0].type == 'INTEGER' or Tokens[0].type == 'STRING' or Tokens[0].value in ('true','false','nil','dummy','(')) and (not(is_keyword(Tokens[0].value)))):
        Rn(Tokens,Stack)
        Build('gamma',2,Stack)
        
def Rn(Tokens,Stack):
    if Tokens:
        if (Tokens[0].type == 'INTEGER'):
            Build(Tokens[0],0,Stack)
            Check(Tokens[0].value,Tokens)
        elif (Tokens[0].type == 'STRING'):
            Build(Tokens[0],0,Stack)
            Check(Tokens[0].value,Tokens)
        elif (Tokens[0].value == 'true'):
            Build('true',0,Stack)
            Check('true',Tokens)
        elif (Tokens[0].value == 'false'):
            Build('false',0,Stack)
            Check('false',Tokens)
        elif (Tokens[0].value == 'nil'):
            Build('nil',0,Stack)
            Check('nil',Tokens)
        elif (Tokens[0].value == 'dummy'):
            Build('dummy',0,Stack)
            Check('dummy',Tokens)
        elif (Tokens[0].value == '('):
            Check('(',Tokens)
            E(Tokens,Stack)
            Check(')',Tokens)
        elif (Tokens[0].type == 'IDENTIFIER'):
            Build(Tokens[0],0,Stack)
            Check(Tokens[0].value,Tokens)

        else:
            print("Error in Rn, got "+Tokens[0].type+" - "+Tokens[0].value)


# Definitions

def D(Tokens,Stack):
    Da(Tokens,Stack)
    if Tokens and (Tokens[0].value == 'within'):
        Check('within',Tokens)
        D(Tokens,Stack)
        Build('within',2,Stack)

def Da(Tokens,Stack):
    Dr(Tokens,Stack)
    if Tokens and (Tokens[0].value == 'and'):
        n = 1
        while Tokens and (Tokens[0].value == 'and'):
            Check('and',Tokens)
            Dr(Tokens,Stack)
            n += 1
        Build('and',n,Stack)

def Dr(Tokens,Stack):
    if Tokens and (Tokens[0].value == 'rec'):
        Check('rec',Tokens)
        Db(Tokens,Stack)
        Build('rec',1,Stack)
    else:
        Db(Tokens,Stack)
        
def Db(Tokens,Stack):
    if Tokens and (Tokens[0].type == 'IDENTIFIER'):
        if len(Tokens)>1 and (Tokens[1].type == 'IDENTIFIER' or Tokens[1].value == '('):
            Build(Tokens[0],0,Stack)
            Check(Tokens[0].value,Tokens)
            n = 1
            while Tokens and (Tokens[0].value == '(' or Tokens[0].type == 'IDENTIFIER'):
                Vb(Tokens,Stack)
                n += 1
            Check('=',Tokens)
            E(Tokens,Stack)
            Build('function_form',n+1,Stack)
        else:
            Vl(Tokens,Stack)
            Check('=',Tokens)
            E(Tokens,Stack)
            Build('=',2,Stack)
    elif Tokens and (Tokens[0].value == '('):
        Check('(',Tokens)
        D(Tokens,Stack)
        Check(')',Tokens)
    else:
        print("Error in Db, got "+Tokens[0].type+" - "+Tokens[0].value)


# Variables

def Vb(Tokens,Stack):
    if Tokens and (Tokens[0].type == 'IDENTIFIER'):
        Build(Tokens[0],0,Stack)
        Check(Tokens[0].value,Tokens)
    elif Tokens and (Tokens[0].value == '('):
        if len(Tokens)>1 and (Tokens[1].value == ')'):
            Check('(',Tokens)
            Check(')',Tokens)
            Build('()',0,Stack)
        else:
            Check('(',Tokens)
            Vl(Tokens,Stack)
            Check(')',Tokens)
    else:
        print("Error in Vb, got "+Tokens[0].type+" - "+Tokens[0].value)

def Vl(Tokens,Stack):
    if Tokens and (Tokens[0].type == 'IDENTIFIER'):
        Build(Tokens[0],0,Stack)
        Check(Tokens[0].value,Tokens)
        n = 1
        while Tokens and (Tokens[0].value == ','):
            Check(',',Tokens)
            Build(Tokens[0],0,Stack)
            Check(Tokens[0].value,Tokens)
            n += 1
        if n>1:
            Build(',',n,Stack)
    else:
        print("Error in Vl, got "+Tokens[0].type+" - "+Tokens[0].value)
    

# Main Function in Parser
def parse(Tokens):
    ''' Parse the Tokens and return the AST'''
    Stack = stack()
    E(Tokens,Stack)
    return Stack.pop()
