import nltk
from nltk.tree import Tree
import sys 
import random

grammar = nltk.CFG.fromstring("""
    S -> DP VP
    DP -> Det NP | NP | DP Conj DP
    NP -> N | PropN | Adj NP | NP PP
    VP -> Vi | Vt  | Vbar DP | Vbar DP PP | Adv VP | VP Adv | VP Conj VP | V AdvP
    Vbar -> Vi | Vt
    AdvP -> Adv P
    PP -> P DP
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
############################################################################################################
############################################################################################################
#           ASSIGNMENT 2 
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

#get parent node 

def get_parent_node(child_tuple): 
    if len(child_tuple) >= 1: 
        parent_node = child_tuple[:-1]
        return parent_node
    else: 
        return None

#get verb tuple 
def get_verb_tuple(tree):
    for node in tree.treepositions(order="leaves"):
        if tree[get_parent_node(node)].label() in ["Vi", "Vt"]:
            return node

verb = get_verb_tuple(parse_tree) #calling the get verb 
print(parse_tree.pretty_print())
print(verb)



# #Define a function that takes a parse tree, and returns the position of the subject DP.
def get_subj_pos(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree): #Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] != VP_pos and tree[node].label() == "DP":
                return node

dp = get_subj_pos(parse_tree)
print(dp)


#Define a function that takes a parse tree, and returns the position of the object DP if one exists, and None otherwise
def get_object_pos(tree):
    VP_pos = (-1,)
    for node in tree.treepositions(order="preorder"):
        if isinstance(tree[node], nltk.Tree): #Check if node has children
            if tree[node].label() == "VP":
                VP_pos = node
            if node[:len(VP_pos)] == VP_pos and tree[node].label() == "DP":
                return node

sentence = sentences[0]
parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)                                  
tokens = sentence.lower().split()
parse_tree = list(parser.parse(tokens))[0]
parse_tree.pretty_print()
obj = get_object_pos(parse_tree)
print(obj)

############################################################################################################
############################################################################################################
#       ASSIGNMENT 3 
translations = { 'John sees Mary' : 'SEES(j,m)', 
 'A student walks': ' ', 
 'Some girl sees every boy': 'all y some x [(GIRL(x) ∧ BOY(y)) → SEES(x, y))]',
 'Every eager student passed'}



############################################################################################################
############################################################################################################
#       ASSIGNMENT 4
lexicon = {
    'every': 'all x [P(x) -> Q(x)]',
    'john' : 'j',
    'mary' : 'm',
    'some' : 'exists x [P(x) AND Q(x)]',
    'girl' : 'lambda x GIRL(x)',
    'boy' : 'labda x <BOY(x)>',
    'a' : "idk yet",
    'eager': "idk yet " ,
    'student': 'lambda x <STUDENT(x)>',
    'passed': 'lambda x <SLEEP(x)>',
    'walk': 'lambda x <WALK(x)>', 
}

