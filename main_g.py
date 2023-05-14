import nltk
from nltk.tree import Tree
import sys 
import random

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    NP -> Det N | N | PropN | Adj NP | NP PP
    VP -> Vi | Vt  | Vbar NP | Vbar NP PP | Adv VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt
    AdvP -> Adv P
    PP -> P NP
    Det -> 'a' | 'an' | 'the' | 'every'| 'some' | 'any'
    P -> 'with' | 'in' | 'on' | 'to' | 'without' | 'from'
    Conj -> 'and' | 'or' | 'but'


    N -> 'boy' | 'student' | 'girl' | 'class' | 'book' | 'teacher'
    PropN -> 'john' | 'mary'
    Adj -> 'eager' | 'smart'
    Vi -> 'walks' | 'passed' 
    Vt -> 'sees' | 'teaches'
    Adv -> 'eagerly' | 'well'
    
""")

sentences = [ 'John sees Mary', 'A student walks', 'Some girl sees every boy','Every eager student passed']


# sentence = random.choice(sentences)
sentence = sentences[0]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    print(parse_tree)

#pretty_print

parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if not parse_trees:
    print("No parse tree found.")
for parse_tree in parse_trees:
    parse_tree.pretty_print()

#select the verb for the sentence 'john sees mary' 
print(parse_tree[1,0])
#select the subject for the sentence 'john sees mary'
print(parse_tree[0])
#select the determiner for sentence 'A student walks'
sentence = sentences[1]
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
for parse_tree in parse_trees:
    parse_tree.pretty_print()
print(parse_tree[0,0])
print('\n' )

#practice iterating
for subtree in parse_tree.subtrees(): 
    print(subtree)
print('\n' )
for pos in parse_tree.treepositions(): 
    print(pos)
print('\n')
for pos in parse_tree.treepositions(order="leaves"):
    print(pos)
print('\n')
for pos in parse_tree.treepositions(order="postorder"):
  print(pos)
print('\n')

# Define a function that takes a parse tree, and returns the position of the verb (i.e., a tuple).
#  If your grammar follows the textbook closely, then the position of the verb will depend on
#  whether it is a transitive or intransitive verb (i.e., depending on the presence/absence of a Vbar node).

def get_verb_tuple(tree):
    # test
    pass

#Define a function that takes a position in the parse tree (i.e., a tuple like (0, 1, 1)) and returns the 
# position of the parent node ((0, 1) in this case), or None if it has no parent.
def get_parent_node(child_tuple): 
    if len(child_tuple) >= 1: 
        parent_node = child_tuple[:-1]
        return parent_node
    else: 
        return None

#Define a function that takes a parse tree, and returns the position of the subject DP.
def get_position_subj (tree):
    pass

#Define a function that takes a parse tree, and returns the position of the object DP if one exists, and None otherwise
def get_position_obj (tree):
    if  'Vt' in parse_tree.subtrees()[0]: 
        obj =  parse_tree.subtres()[1,1,1]
        return obj
    else: 
        None 

sentence = sentences[0]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_trees = parser.parse(tokens)
if parse_tree in parse_trees:  
    print(parse_tree)
    print(get_position_obj(parse_tree))