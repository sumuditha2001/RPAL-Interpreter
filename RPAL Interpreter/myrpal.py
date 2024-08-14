import Scanner
import Parser
import tree_flattener
from cse_machine import evaluate
from Standardizer import standardize_tree
from DataStructures import *
import sys

def main1(input_file):
    tokens = Scanner.scan(input_file)
    AST = Parser.parse(tokens)
    print_tree(AST)
    ST=standardize_tree(AST)
    control_structures=tree_flattener.CS(ST)
    answer=evaluate(control_structures)

def main2(input_file):
    tokens = Scanner.scan(input_file)
    AST = Parser.parse(tokens)
    ST=standardize_tree(AST)
    control_structures=tree_flattener.CS(ST)
    answer=evaluate(control_structures)


if len(sys.argv)>2:
    if sys.argv[1]=="-ast":
        main1(sys.argv[2])
    else:
        print("Invalid command")
else:
    main2(sys.argv[1])