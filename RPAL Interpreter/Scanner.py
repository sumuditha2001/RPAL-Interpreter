# Writing a Scanner for recognizing tokens in rpal language

from DataStructures import token

# Set of token types
T_id = 'IDENTIFIER'
T_int = 'INTEGER'
T_op = 'OPERATOR'
T_str = 'STRING'
T_space = 'DELETE'
T_comment = 'DELETE'
T_lpun = '('
T_rpun = ')'
T_semi = ';'
T_comma = ','

# Set of characters, digits and operators
Letter = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
Digit = '0123456789'
Operator = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', '\'', '?']


    
def scan(input_file):
    with open(input_file, 'r') as file:
        input = file.read()
        input=input+"\n"    # Adding a new line at the end of the file for the scanner to recognize the last token
            
    Tokens = []
    while input:
        current = input[0]
        input = input[1:]
        # IDENTIFIER
        if current in Letter:
            word = current
            while input and (input[0] in Letter or input[0] in Digit or input[0] == '_'):
                word += input[0]
                input = input[1:]
            t = token(T_id, word)
            Tokens.append(t)
        
        # INTEGER
        elif current in Digit:
            number = current
            while input and input[0] in Digit:
                number += input[0]
                input = input[1:]
            t = token(T_int, number)
            Tokens.append(t)
        
        # STRING
        elif current == "'":
            string = ''
            while input and (input[0] in ['\\','(',')',';',',',' '] or input[0] in Letter or input[0] in Digit or input[0] in Operator) or input[0] == "'":
                if input[0] == "'":
                    t = token(T_str, string)
                    Tokens.append(t)
                    input = input[1:]
                    break
                if input[0] == '\\':
                    string += input[0]
                    input = input[1:]
                    if input[0] in ('t','n','\\','"'):
                        string += input[0]
                        input = input[1:]
                    else:
                        print('Invalid string'+string+input[0])
                string += input[0]
                input = input[1:]
            else:
                print('Invalid string'+string+input[0])
        
        # SPACE
        elif current in [' ','\n','\t']:
            space = current
            while input and input[0] in [' ','\n','\t']:
                space += input[0]
                input = input[1:]
            t = token(T_space, space)
            # Tokens.append(t)
            
        # COMMENT
        elif current == '/' and input[0] == '/':
            input = input[1:]
            comment = input[0]
            while input and (input[0] in ['"','(',')',';',',','\\',' ','\t'] or input[0] in Letter or input[0] in Digit or input[0] in Operator) or input[0] == '\n':
                if input[0] == '\n':
                    t = token(T_comment, comment)
                    # Tokens.append(t)
                    break
                comment += input[0]
                input = input[1:]
            else:
                print('Invalid comment'+comment+input[0])
                
        # OPERATOR
        elif current in Operator:
            op = current
            while input and input[0] in Operator:
                op += input[0]
                input = input[1:]
            t = token(T_op, op)
            Tokens.append(t)
                
        # PUNCTUATION
        elif current == '(':
            t = token(T_lpun, current)
            Tokens.append(t)
        elif current == ')':
            t = token(T_rpun, current)
            Tokens.append(t)
        elif current == ';':
            t = token(T_semi, current)
            Tokens.append(t)
        elif current == ',':
            t = token(T_comma, current)
            Tokens.append(t)
        else:
            print('Invalid character'+current)
            
    return Tokens   # Returns the list of tokens
            

